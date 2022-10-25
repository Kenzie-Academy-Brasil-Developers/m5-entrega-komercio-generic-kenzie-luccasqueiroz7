from rest_framework import generics

from users.models import User
from users.permissions import HasObjectPermission, HasPermission
from users.serializers import AccountDetailSerializer, AccountSerializer

from rest_framework.authentication import TokenAuthentication


class AccountView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class AccountDetailView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasObjectPermission]


class AccountIsActiveView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [HasPermission]


class AccountKwargsView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        num = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:num]
