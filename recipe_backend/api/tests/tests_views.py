from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import ChefUser, Recipe
from ..serializers import RecipeSerializer
from dotenv import load_dotenv
from django.urls import reverse
import pathlib
import os
import json

# Create your tests here.


class RecipeViewSetTest(TestCase):

    def setUp(self):
        path_dir = pathlib.Path().absolute()
        load_dotenv(os.path.join(path_dir, '.env'))
        self.API_URL = os.getenv('API_BASE')
        self.chef = ChefUser.objects.create(username="alvoD", first_name="Alvo",
                                            last_name="Dumbledore", email="alvo@hogwarts.com", password="alvo1234")
        self.client = APIClient()
        self.refresh = RefreshToken.for_user(self.chef)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        Recipe.objects.create(title="Pão de aveia", ingredients="1 ovo, 2 colheres de farinha de aveia, pitada de sal",
                              preparation_mode="Mistura todos os ingredientes e coloque na figideira.", chef=self.chef)

    def test_create_recipe(self):
        data = {
            "title": "Mousse de Chocolate Funcional",
            "ingredients": "1 abacate, 2 bananas maduras e cacau em pó 100%.",
            "preparation_mode": "Bata todos os ingredientes no liquidificador e depois coloque na geladeira."
        }
        response = self.client.post(
            '{0}api/recipes/'.format(self.API_URL), data, format='json')
        self.assertEquals(response.status_code, 201)

    def test_return_list_recipes(self):
        response = self.client.get(
            '{0}api/recipes/'.format(self.API_URL), format='json')
        encoded_recipe = json.dumps(response.data)
        decoded_recipe = json.loads(encoded_recipe)
        value = next(
            (True for recipe in decoded_recipe if recipe['title'] == 'Pão de aveia'), None)
        self.assertEquals(value, True)
        self.assertEquals(response.status_code, 200)

    def test_get_recipe_by_id(self):
        response = self.client.get(
            '{0}api/recipes/1/'.format(self.API_URL), format='json')
        self.assertEquals(response.data['title'], 'Pão de aveia')

    def test_update_recipe(self):
        data = {
            "title": "Pão de aveia funcional"
        }
        response = self.client.put(
            '{0}api/recipes/1/'.format(self.API_URL), data, format='json')
        self.assertEquals(response.data['title'], 'Pão de aveia funcional')

    def test_delete_recipe(self):
        response = self.client.delete(
            '{0}api/recipes/1/'.format(self.API_URL))
        recipes = Recipe.objects.all()
        self.assertEquals(len(recipes), 0)
        self.assertEquals(response.status_code, 204)

    def test_search_recipes_chef(self):
        data = {
            "search": "Alvo"
        }
        response = self.client.post(
            reverse('recipes_chef'), data, format='json')
        encoded_recipe = json.dumps(response.data)
        decoded_recipe = json.loads(encoded_recipe)
        self.assertEquals(decoded_recipe[0]['title'], 'Pão de aveia')
        self.assertEquals(response.status_code, 200)

    def test_search_recipe(self):
        data = {
            "search": "aveia"
        }
        response = self.client.post(
            reverse('search_recipe'), data, format='json')
        encoded_recipe = json.dumps(response.data)
        decoded_recipe = json.loads(encoded_recipe)
        self.assertEquals(decoded_recipe[0]['title'], 'Pão de aveia')
        self.assertEquals(response.status_code, 200)
