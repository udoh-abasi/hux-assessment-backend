from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import Contact
from rest_framework.views import APIView
from .serializers import AllContacts


User = get_user_model()


# This view creates a new contact. It is csrf protected, and only authenticated (logged in) users can access the view
# It responds to a POST request from '/api/create', with a request body which must have the firstName, lastName and phoneNumber
@method_decorator(csrf_protect, name="dispatch")
class CreateContact(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        try:
            # Get the data (this MUST contain the firstName, 'lastName' and 'phoneNumber' properties)
            data = request.data

            # Get the user that sent the request
            user = request.user

            firstName = data.get("firstName", "").strip()
            lastName = data.get("lastName", "").strip()
            phoneNumber = data.get("phoneNumber", "").strip()

            if firstName and lastName and phoneNumber:
                # Create a new Contact object and save to the database
                obj = Contact.objects.create(
                    user=user,
                    firstName=firstName,
                    lastName=lastName,
                    phoneNumber=phoneNumber,
                )

                obj.save()

                # If everything was successful, return the created data to the frontend, with a 201 created status
                return Response(
                    {
                        "firstName": firstName,
                        "lastName": lastName,
                        "phoneNumber": phoneNumber,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# This view sends all the contacts a particular user created, back to the frontend.
# If the user has not created a contact yet, an empty list is returned
# It is csrf protected, and only authenticated (logged in) users can access the view
# It responds to a GET request to '/api/allcontacts'.
@method_decorator(csrf_protect, name="dispatch")
class GetContacts(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        try:
            user = request.user

            # Get all contacts that were saved by the logged in user only, and then order by date, so that the last added contact will appear on top
            result = Contact.objects.filter(user=user).order_by("dateAdded")

            # This will return a list containing all contacts
            serializer = AllContacts(result, many=True).data

            return Response(serializer, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# This view deletes a contact as long as it was created by the logged in user
# It is csrf protected, and only authenticated (logged in) users can access the view
# It responds to a DELETE request to '/api/delete/:contactID'.
# It takes a parameter, which is the id of the article to be deleted
@method_decorator(csrf_protect, name="dispatch")
class DeleteContacts(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, request, contactID):
        try:
            contactID = int(contactID)

            # First, we get the article the user wants to delete. We also ensured the logged in user is the one that created the contact
            article = Contact.objects.get(user=request.user, id=contactID)

            # Then we delete the article
            article.delete()

            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# This view returns a single contact as long as it was created by the logged in user
# It is csrf protected, and only authenticated (logged in) users can access the view
# It responds to a GET request to '/api/contactdetails/:contactID'.
# It takes a URL parameter, which is the id of the article that is requested
@method_decorator(csrf_protect, name="dispatch")
class GetContactDetails(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, contactID):
        try:
            contactID = int(contactID)

            # First, we get the article the user wants. We also ensured the user actually created the contact. This is to avoid another user from seeing someone else's contact
            article = Contact.objects.get(user=request.user, id=contactID)

            # Then we serialize and return the data (as JSON)
            serializer = AllContacts(
                article,
            ).data

            return Response(serializer, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# This view will edit and save a contact as long as it was created by the logged in user
# It is csrf protected, and only authenticated (logged in) users can access the view
# It responds to a PUT request to '/api/edit/:contactID'.
# It takes a URL parameter, which is the id of the article that to be edited
@method_decorator(csrf_protect, name="dispatch")
class EditContact(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request, contactID):
        try:
            data = request.data

            contactID = int(contactID)

            firstName = data.get("firstName", "").strip()
            lastName = data.get("lastName", "").strip()
            phoneNumber = data.get("phoneNumber", "").strip()

            if firstName and lastName and phoneNumber:
                # First, we get the article the user wants to edit. Also ensure the user that made the request is the one that saved the contact
                article = Contact.objects.get(user=request.user, id=contactID)

                # Make changes
                article.firstName = firstName
                article.lastName = lastName
                article.phoneNumber = phoneNumber

                # Save changes
                article.save()

                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
