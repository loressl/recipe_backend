from rest_framework import viewsets, status
from rest_framework.views import Response
from .models import *
from .serializers import *
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.decorators import action

# Create your views here.

class ChefUserViewSet(viewsets.ModelViewSet):

    queryset = ChefUser.objects.all()
    serializer_class = ChefUserSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(self.__class__, self).get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            ChefUser.objects.get(email=request.data['email'])
            return Response({"mensagem": "Usuário já está cadastrado. Verifique seus dados"}, status=status.HTTP_404_NOT_FOUND)
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
    serializer_class = RecipeSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.action == 'list' or self.action == 'recipe-detail' or self.action == 'search_recipe' or self.action == 'recipes_chef':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super(self.__class__, self).get_permissions()

    def create(self, request):
        try:
            Recipe.objects.get(title=request.data['title'])
            return Response({"mensagem": "Usuário já está cadastrado. Verifique seus dados"}, status=status.HTTP_400_BAD_REQUEST)
        except Recipe.DoesNotExist:
            pass
        chefUser = ChefUser.objects.get(email=request.user)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(chef=chefUser)
            return Response({"mensagem": "Receita cadastrada com sucesso!!"}, status=status.HTTP_201_CREATED)
        return Response({"mensagem": "Ocorreu um erro. Verifique seus dados!!"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, id=None):
        recipes = self.get_queryset()
        if not recipes:
            return Response({"mensagem": "Ainda não há receitas cadastrada na base de dados."}, status=status.HTTP_404_NOT_FOUND)
        page = self.paginate_queryset(recipes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True, url_path='search-recipe', url_name='search_recipe')
    def search_recipe(self, request):
        result_title = Recipe.objects.filter(
            title__icontains=request.data['search'])
        result_ingredients = Recipe.objects.filter(
            ingredients__icontains=request.data['search'])
        result_final = list(set(result_title) | set(result_ingredients))
        if not result_final:
            return Response({"mensagem": "Não existe receitas para essa busca."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(result_final, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True,  url_path='recipes-chef', url_name='recipes_chef')
    def recipes_chef(self, request):
        names = request.data['search'].split(' ')
        results = []
        if len(names) > 1:
            if names[0] and names[1]:
                chef = ChefUser.objects.filter(first_name__icontains = names[0], last_name= names[1])
        else:
            chef = ChefUser.objects.filter(first_name__icontains = names[0])
            for user in chef:
                result_recipes = Recipe.objects.filter(chef= user.id)
                results.append(result_recipes)
        if not results[0]:
            return Response({"mensagem": "Não existe receitas para essa busca."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(results[0], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
