from django.db import models

from users.models import User


class Recipient(models.Model):
    email = models.EmailField(verbose_name='Почта', unique=True)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец получателей', blank=True)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'


class Letter(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец рассылки', blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Письмо рассылки'
        verbose_name_plural = 'Письма рассылки'


class Mailing(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название рассылки')
    description = models.CharField(max_length=150, verbose_name='Описание рассылки', blank=True, null=True)
    time = models.TimeField(verbose_name='Время рассылки')
    periodicity = models.IntegerField(verbose_name='Периодичность рассылки',
                                      choices=((1, 'Ежедневно'), (7, 'Еженедельно'), (30, 'Ежемесячно')))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец рассылки', blank=True, null=True)
    is_launched = models.BooleanField(default=False, verbose_name='Запущена')
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, verbose_name='Письмо рассылки', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    recipients = models.ManyToManyField(Recipient, blank=True, verbose_name='Получатели')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'deactivate_mailing',
                'Can deactivate mailing'
            ),
        ]


class MailingLog(models.Model):
    last_time = models.DateTimeField(verbose_name='Время рассылки')
    status = models.BooleanField(verbose_name='Статус последней рассылки')
    server_answer = models.TextField(verbose_name='Ответ почтового сервера', blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Письмо рассылки', blank=True,
                                null=True)

    def __str__(self):
        return f'{self.last_time} {self.status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылки'
