import ptbot
import os
from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = '{0:.1f}'
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify(chat_id):
    bot.send_message(chat_id, 'Время вышло')


def notify_progress(time, chat_id, message_id, progress_bar_lenght):
    progress = progress_bar_lenght - time
    timer = f'Осталось {time} секунд\n{render_progressbar(progress_bar_lenght, progress)}'
    bot.update_message(chat_id, message_id, timer)


def countdown(chat_id, message):
    time = parse(message)
    progress_bar_lenght = parse(message)
    message_id = bot.send_message(chat_id, 'Запускаю таймер...')
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        progress_bar_lenght=progress_bar_lenght
    )
    time_2 = time + 1
    bot.create_timer(time_2, notify, chat_id=chat_id)


def main():
    bot.reply_on_message(countdown)
    bot.run_bot()


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.getenv('BOT_TOKEN')
    bot = ptbot.Bot(tg_token)
    main()