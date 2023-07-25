from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from userApp.models import User, Notes
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.generics import ListCreateAPIView

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import UserSerializer, NoteSerializer


# to get the totken
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["is_admin"] = user.is_superuser

        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "api/token",
        "api/token/refresh",
    ]

    return Response(routes)


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("serializer", serializer.data)
        return Response(serializer.data)


@api_view(["GET"])
def userList(request):
    users = User.objects.filter(is_superuser=False)
    serializer = UserSerializer(users, many=True)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["id"]
    return Response(serializer.data)


@api_view(["GET"])
def userDetails(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def userUpdate(request, pk):
    try:
        user = User.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(instance=user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        if "profile_img" in request.FILES:
            user.profile_img = request.FILES["profile_img"]
            user.save()

        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def userDelete(request, pk):
    user = User.objects.get(id=pk)
    user.delete()

    return Response("User deleted")


class classUserList(ListCreateAPIView):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]


class Notes(ListCreateAPIView):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer
