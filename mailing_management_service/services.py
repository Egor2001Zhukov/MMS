import datetime
import getpass

from crontab import CronTab
from django.contrib.auth.models import Group

from config.settings import BASE_DIR
from mailing_management_service import models as m
from users.models import User

username: str = getpass.getuser()


def generate_cron_time(mailing: m.Mailing):
    if mailing.periodicity == 1:
        cron_time = f'{mailing.time.minute} {mailing.time.hour} * * *'
    elif mailing.periodicity == 7:
        cron_time = f'{mailing.time.minute} {mailing.time.hour} * * {datetime.date.today().weekday() + 1}'
    elif mailing.periodicity == 30:
        cron_time = f'{mailing.time.minute} {mailing.time.hour} {datetime.date.today().day} * *'
    else:
        raise ValueError("Invalid periodicity")
    return cron_time


def add_cron_task_mailing(mailing: m.Mailing):
    cron = CronTab(user=username)
    comment = f'mailing_{mailing.pk}'
    path = ''
    for element in str(BASE_DIR):
        if element == ' ':
            element = '\ '
        path += element
        print(path)
    command = f'{path}/venv/bin/python3 {path}/manage.py send_mailing_script {mailing.pk}'  # Замените на путь к вашему скрипту
    job = cron.new(command=command, comment=comment)
    job.setall(generate_cron_time(mailing))
    cron.write()


# Функция для удаления задачи Cron по комментарию
def remove_cron_task_mailing(mailing: m.Mailing):
    cron = CronTab(user=username)
    comment = f'mailing_{mailing.pk}'
    for job in cron:
        if comment in job.comment:
            cron.remove(job)
            cron.write()


def update_cron_task_mailing(mailing: m.Mailing):
    remove_cron_task_mailing(mailing)
    add_cron_task_mailing(mailing)


def is_moderator_or_creator(user: User, obj):
    moderators = Group.objects.get(name="moderators").user_set.all()
    if user in moderators:
        print('Это удалил модератор')
        return True
    elif user == obj.user:
        print('Это удалил создатель')
        return True
    else:
        print('Я не даю')
        return False


def is_creator(user: User, obj):
    if user == obj.user:
        print('Это удалил создатель')
        return True
    else:
        print('Я не даю')
        return False
