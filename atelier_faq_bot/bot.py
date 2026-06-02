import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .faq import SOURCES, top_faq, topics
from .matcher import format_answer
from .settings import Settings

WELCOME = (
    "Atelier FAQ bot ready. Ask me about the AI-agent marketplace, agent registration, services, "
    "orders, bounties, payments, API, x402, or safety.\n\n"
    "Examples:\n"
    "- What is Atelier?\n"
    "- How do I register an agent?\n"
    "- How do payments work?\n"
    "- /faq\n"
    "- /topics"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(WELCOME)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Commands:\n"
        "/start - intro\n"
        "/help - commands\n"
        "/faq - common questions\n"
        "/topics - supported topics\n"
        "/ask <question> - ask a question\n"
        "/about - official Atelier links\n\n"
        "You can also just send a normal question."
    )


async def faq_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = ["Top Atelier FAQs:"]
    for idx, entry in enumerate(top_faq(), start=1):
        lines.append(f"{idx}. {entry.question}")
    lines.append("\nUse /ask <question> or send any question as a message.")
    await update.effective_message.reply_text("\n".join(lines))


async def topics_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text("Supported topics: " + ", ".join(topics()))


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "Atelier is an AI-agent marketplace where clients hire agents for tasks and agents can list services or complete bounties.\n\n"
        + "\n".join(SOURCES)
    )


async def ask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip()
    if not query:
        await update.effective_message.reply_text("Usage: /ask How do I register an agent?")
        return
    await update.effective_message.reply_text(format_answer(query))


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.effective_message.text or ""
    await update.effective_message.reply_text(format_answer(text))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.exception("Telegram handler error", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "Something went wrong while answering. Please try again, or use /help for supported commands."
            )
        except Exception:
            logging.exception("Failed to send fallback error message")


def build_application(settings: Settings) -> Application:
    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("faq", faq_cmd))
    app.add_handler(CommandHandler("topics", topics_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("ask", ask_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_error_handler(error_handler)
    return app


def run(settings: Settings) -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    app = build_application(settings)
    logging.info("Starting Atelier FAQ bot")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
