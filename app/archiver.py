import asyncio
from aiogram import Bot
from aiogram.types import URLInputFile
from app.settings import env, logger


async def send_files(bot: Bot, chat_id: int):
    """Send files one by one with a delay to avoid Telegram's rate limit."""
    total_files = len(env.links)
    success, errors = 0, 0

    await bot.send_message(
        chat_id, text=f"🚀 Starting file transfer\n📁 Total files: {total_files}"
    )

    for name, url in env.links.items():
        try:
            file = URLInputFile(url, filename=f"{name}.zip", timeout=15)
            await bot.send_document(chat_id=chat_id, document=file, disable_notification=True)
            success += 1
            await asyncio.sleep(3)
        except Exception as e:
            logger.error(f"❌ Failed to send {name}: {e}")
            errors += 1

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
