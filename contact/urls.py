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
    path("delete/<str:articleID>", DeleteContacts.as_view()),
    path("contactdetails/<str:articleID>", GetContactDetails.as_view()),
    path("edit/<str:articleID>", EditContact.as_view()),
]
