from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status, permissions

from contact_share_service.models import Card
from contact_share_service.serializers import UserSerializer, CardSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserSerializer


class RetrieveUpdateDestroyProfile(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    http_method_names = ['patch', 'get', 'delete']

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # If the request included an email change request,
        # reply with 403.
        email = request.data.get('email')
        if email:
            return Response(
                {'email': 'Cannot be changed.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class CreateListCard(ListCreateAPIView):
    serializer_class = CardSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Card.objects.filter(owner_id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        request.data.update({'owner': self.request.user.id})
        return super().post(request, *args, **kwargs)
