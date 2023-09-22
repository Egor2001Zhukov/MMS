import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings
from mailing_management_service import models as m


class Command(BaseCommand):
    help = 'Command for send mailing'

    def add_arguments(self, parser):
        parser.add_argument('mailing_pk', type=int, help='mailing_pk')

    def handle(self, *args, **options):
        print('я сработал')
        mailing = m.Mailing.objects.get(pk=options['mailing_pk'])
        try:
            send_mail(subject=mailing.letter.subject, message=mailing.letter.body,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list=mailing.recipients.all())
            status = True
            server_answer = 'Email sent successfully'
        except Exception as e:
            status = False
            server_answer = str(e)
        m.MailingLog.objects.create(
            status=status,
            server_answer=server_answer,
            mailing=mailing,
            last_time=datetime.datetime.now())
