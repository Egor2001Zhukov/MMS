from django.contrib import admin

from mailing_management_service import models as m


@admin.register(m.Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(m.Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('subject',)


@admin.register(m.MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_time',)


@admin.register(m.Recipient)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('email',)
