#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.callback import callback_delete_message
from utils.config_loader import config
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('start', start))


@restricted
def start(update, context):
    rsp = update.message.reply_text('🔺 Step 1 : Hãy gửi cho tôi file ZIP chứa các tệp SA và thêm /sa vào phía dưới file.\n'
                                    '📂 Step 2 : Sử dụng lệnh /folders để đặt thư mục đích.\n'
                                    '🔗 Step 3 : Tất cả đã sẵn sàng! Chỉ cần Forward hoặc link Google Drive')
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
