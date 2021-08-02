#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.config_loader import config
from utils.callback import callback_delete_message
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('help', get_help))


@restricted
def get_help(update, context):
    message = 'Gửi liên kết Google Drive hoặc chuyển tiếp tin nhắn có liên kết Google Drive để Clone file.\n' \
              'Sau đó tải lên /sa và cấu hình /folders cần sử dụng.\n\n' \
              '📚 Lệnh Commands:\n' \
              ' │ /folders - Set favorite folders\n' \
              ' │ /sa - Chỉ hợp lệ khi Private, tải lên tệp ZIP chứa các tài khoản SA với lệnh này.\n' \
              ' │ /help - Hiển thị ra thông báo này\n'
    rsp = update.message.reply_text(message)
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
