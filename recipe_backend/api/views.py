from rest_framework import viewsets, status
from rest_framework.views import Response
from .models import *
from .serializers import *
from rest_framework.permissions import  SAFE_METHODS,AllowAny, IsAuthenticatedOrReadOnly, BasePermission

# Create your views here.

class RecipePermission(BasePermission):
    message = 'Edição das receitas é restrita para os cadastrados.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.auth == request.user_id


class ChefUserViewSet(viewsets.ModelViewSet):

    queryset = ChefUser.objects.all()
    serializer_class = ChefUserSerializer
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        try:
            ChefUser.objects.get(email=request.data['email'])
            return Response({"mensagem": "Usuário já está cadastrado. Verifique seus dados"}, status=status.HTTP_400_BAD_REQUEST)
        except ChefUser.DoesNotExist:
            pass
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            newuser = serializer.save()
            if newuser:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"mensagem": "Verifique seus dados."}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, id=None):
        instance = self.get_object()
        seliarizer = self.get_serializer(instance)
        return Response(seliarizer.data, status=status.HTTP_200_OK)

    def update(self, request, id=None):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, id=None):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer = RecipeSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(self.__class__, self).get_permissions()

    def create(self, request):
        print(request.data)
        return Response({}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        print("deu certo")
        return Response({}, status=status.HTTP_200_OK)
