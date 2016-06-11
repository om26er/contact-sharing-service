from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from contact_share_service.serializers import UserSerializer
from contact_share_service.helpers.response_helpers import ResponseConstructor


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class PasswordResetView(APIView):
    def _validate_parameters(self, email):
        response_constructor = ResponseConstructor()
        response_constructor.validate_field('email', email)
        return response_constructor.get_response()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        message = self._validate_parameters(email)
        if message:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
