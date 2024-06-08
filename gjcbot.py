from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters
import logging
import datetime
import nest_asyncio
import asyncio

# 应用 nest_asyncio 以允许嵌套事件循环
nest_asyncio.apply()

# 启用日志记录
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 定义机器人令牌
bot_token = 'YOUR_TELEGRAM_BOT_TOKEN'

# 定义命令处理程序
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    full_name = f"{first_name} {last_name}" if last_name else first_name

    # 模拟用户数据
    expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
    keywords = ["example", "test"]
    push_status = "已开启"
    expiry_status = "未过期"

    message = (
        f"【账号ID】{user_id}\n"
        f"【昵称及用户名】{full_name} (@{username})\n"
        f"【过期状态：】{expiry_status}\n"
        f"【过期时间：】{expiry_date.strftime('%Y-%m-%d')}\n"
        f"【推送状态：】{push_status}\n"
        f"【监听关键词：】{', '.join(keywords)}\n"
        f"【 更多功能：点击键盘按钮或 /help 】"
    )
    await update.message.reply_text(message)

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "快捷指令一览：\n"
        "/start - 基本信息\n"
        "/qun - 推送设置说明\n"
        "/gjc - 关键词设置\n"
        "/buy - 购买或续费\n"
        "/id - 查看自己及群组ID\n"
        "/help - 命令列表\n"
        "/ks - 开始监听"
    )

async def main() -> None:
    # 创建应用程序并传递机器人的令牌
    application = Application.builder().token(bot_token).build()

    # 在不同的命令上 - 在 Telegram 中回答
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # 启动机器人
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.updater.stop()
    await application.stop()
    await application.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e) == "This event loop is already running":
            nest_asyncio.apply()
            asyncio.run(main())
        else:
            raise
