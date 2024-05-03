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


# This view creates a new contact
@method_decorator(csrf_protect, name="dispatch")
class CreateContact(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        try:
            data = request.data
            user = request.user

            firstName = data.get("firstName", "").strip()
            lastName = data.get("lastName", "").strip()
            phoneNumber = data.get("phoneNumber", "").strip()

            if firstName and lastName and phoneNumber:
                obj = Contact.objects.create(
                    user=user,
                    firstName=firstName,
                    lastName=lastName,
                    phoneNumber=phoneNumber,
                )

                obj.save()
                print("Saved Object", obj)

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


@method_decorator(csrf_protect, name="dispatch")
class GetContacts(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        user = request.user

        result = Contact.objects.filter(user=user).order_by("dateAdded")

        serializer = AllContacts(result, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)


# Delete a contact
@method_decorator(csrf_protect, name="dispatch")
class DeleteContacts(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, request, articleID):
        try:
            articleID = int(articleID)
            # First, we get the article the user wants to delete
            article = Contact.objects.get(user=request.user, id=articleID)

            article.delete()
            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name="dispatch")
class GetContactDetails(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, articleID):
        try:
            articleID = int(articleID)
            # First, we get the article the user wants to see
            article = Contact.objects.get(user=request.user, id=articleID)

            serializer = AllContacts(
                article,
            ).data

            return Response(serializer, status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_protect, name="dispatch")
class EditContact(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request, articleID):
        try:
            data = request.data

            articleID = int(articleID)

            firstName = data.get("firstName", "").strip()
            lastName = data.get("lastName", "").strip()
            phoneNumber = data.get("phoneNumber", "").strip()

            if firstName and lastName and phoneNumber:
                # First, we get the article the user wants to edit
                article = Contact.objects.get(user=request.user, id=articleID)

                article.firstName = firstName
                article.lastName = lastName
                article.phoneNumber = phoneNumber

                article.save()

                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
