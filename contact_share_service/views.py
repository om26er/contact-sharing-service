from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from contact_share_service.models import User, Card
from contact_share_service.serializers import UserSerializer, CardSerializer
from contact_share_service.helpers import (
    send_password_reset_email,
    generate_random_key,
)
from contact_share_service.helpers.user_helpers import UserHelpers
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

        try:
            user_account = UserHelpers(email=email)
            if user_account.is_active():
                if user_account.is_admin():
                    return Response(status=status.HTTP_403_FORBIDDEN)
                user_account.set_password_reset_key(generate_random_key())
                send_password_reset_email(
                    email,
                    user_account.get_password_reset_key()
                )
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    data={'email': ['Account not active.']},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class ChangePasswordView(APIView):
    def _validate_parameters(self, email, reset_key, new_password):
        response_constructor = ResponseConstructor()
        response_constructor.validate_field('email', email)
        response_constructor.validate_field('reset_key', reset_key)
        response_constructor.validate_field('new_password', new_password)
        return response_constructor.get_response()

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        reset_key = request.data.get('reset_key')
        new_password = request.data.get('new_password')
        message = self._validate_parameters(email, reset_key, new_password)
        if message:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_account = UserHelpers(email=email)
            if user_account.is_admin():
                return Response(status=status.HTTP_403_FORBIDDEN)
            if user_account.is_password_reset_key_valid(reset_key):
                user_account.change_password(new_password)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(
                    data={'reset_key': ['Invalid']},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )


class CreateCardView(CreateAPIView):
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        request.data.update({'owner': self.request.user.id})
        return super().post(request, *args, **kwargs)


class RetrieveCardsView(ListAPIView):
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Card.objects.filter(owner_id=self.request.user.id)
