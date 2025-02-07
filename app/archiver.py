import asyncio
from aiogram import Bot
from aiogram.types import URLInputFile, InputMediaDocument
from app.settings import env, logger


async def send_files(bot: Bot, chat_id: int):
    """Send multiple files as media groups to a chat, handling Telegram's 10-file limit."""
    total_files = len(env.links)
    success, errors = 0, 0

    await bot.send_message(
        chat_id, text=f"🚀 Starting file transfer\n📁 Total files: {total_files}"
    )

    media_groups = []
    media_batch = []

    for name, url in env.links.items():
        try:
            media_batch.append(
                InputMediaDocument(
                    media=URLInputFile(url, filename=f"{name}.zip", timeout=15)
                )
            )
            if len(media_batch) == 10:
                media_groups.append(media_batch)
                media_batch = []
        except Exception as e:
            logger.error(f"❌ Failed to prepare {name}: {e}")
            errors += 1

    if media_batch:
        media_groups.append(media_batch)

    for group in media_groups:
        try:
            await bot.send_media_group(chat_id, group)
            success += len(group)
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"❌ Failed to send media group: {e}")
            errors += len(group)

    await bot.send_message(
        chat_id, text=f"📊 Transfer Report:\n✅ Success: {success}\n❌ Failed: {errors}"
    )
    return success


async def main():
    """Initialize the bot and send files sequentially to all configured chats."""
    try:
        logger.info("Starting bot...")
        async with Bot(token=env.BOT_TOKEN) as bot:
            total_sent = 0
            for chat_id in env.CHAT_IDS:
                sent = await send_files(bot, chat_id)
                total_sent += sent
            logger.info(f"Total files sent: {total_sent}")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
    finally:
        logger.info("Bot shutdown completed")


if __name__ == "__main__":
    asyncio.run(main())
