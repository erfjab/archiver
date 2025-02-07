import asyncio
from aiogram import Bot
from aiogram.types import URLInputFile
from app.settings import env, logger


async def main():
    try:
        logger.info("Starting bot...")
        async with Bot(token=env.BOT_TOKEN) as bot:
            for chat_id in env.CHAT_IDS:
                logger.info(f"Processing chat ID: {chat_id}")
                for name, url in env.links.items():
                    await bot.send_document(
                        chat_id=chat_id,
                        document=URLInputFile(
                            url=url, filename=f"{name}.zip", timeout=5
                        ),
                    )
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
    finally:
        logger.info("Bot shutdown completed")


if __name__ == "__main__":
    asyncio.run(main())
