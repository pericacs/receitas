from django.test import TestCase
from django.urls import reverse

class RecipeURLsTest(TestCase):
    def test_receita_home_url_is_correct(self):
        url = reverse('receitas:home')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('receitas:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/receitas/category/1/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse('receitas:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')


  