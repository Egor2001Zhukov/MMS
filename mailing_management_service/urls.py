from django.urls import path

from mailing_management_service import views as v
from mailing_management_service.apps import MailingManagementServiceConfig

app_name = MailingManagementServiceConfig.name

urlpatterns = [
    path('', v.MailingListView.as_view(), name='mailing_list'),
    path('create/', v.MailingCreateView.as_view(), name='create_mailing'),
    path('view/<int:pk>', v.MailingDetailView.as_view(), name='view_mailing'),
    path('view/<int:pk>/mailinglog', v.MailingLogListView.as_view(), name='view_mailinglog'),
    path('update/<int:pk>', v.MailingUpdateView.as_view(), name='update_mailing'),
    path('delete/<int:pk>', v.MailingDeleteView.as_view(), name='delete_mailing'),

    path('change_mailing_letter/<int:pk>/', v.change_letter_view, name='change_mailing_letter'),
    path('change_is_launched/<int:pk>/', v.change_is_launched_view, name='change_is_launched'),

    path('letters/', v.LetterListView.as_view(), name='letter_list'),
    path('letters/create/', v.LetterCreateView.as_view(), name='create_letter'),
    path('letters/view/<int:pk>', v.LetterDetailView.as_view(), name='view_letter'),
    path('letters/update/<int:pk>', v.LetterUpdateView.as_view(), name='update_letter'),
    path('letters/delete/<int:pk>', v.LetterDeleteView.as_view(), name='delete_letter'),

    path('recipients/', v.RecipientListView.as_view(), name='recipient_list'),
    path('recipients/create/', v.RecipientCreateView.as_view(), name='create_recipient'),
    path('recipients/view/<int:pk>', v.RecipientDetailView.as_view(), name='view_recipient'),
    path('recipients/update/<int:pk>', v.RecipientUpdateView.as_view(), name='update_recipient'),
    path('recipients/delete/<int:pk>', v.RecipientDeleteView.as_view(), name='delete_recipient'),
]
