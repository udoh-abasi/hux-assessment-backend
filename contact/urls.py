from django.urls import path
from .views import (
    CreateContact,
    GetContacts,
    DeleteContacts,
    GetContactDetails,
    EditContact,
)

urlpatterns = [
    path("create", CreateContact.as_view()),
    path("allcontacts", GetContacts.as_view()),
    path("delete/<str:contactID>", DeleteContacts.as_view()),
    path("contactdetails/<str:contactID>", GetContactDetails.as_view()),
    path("edit/<str:contactID>", EditContact.as_view()),
]
