# flake8: noqa
from django.urls import reverse, resolve
from receitas import views
from .test_receita_base import RecipeTestBase # noqa E261 

class RecipeViewsTest(RecipeTestBase): # noqa E302     
    def test_recipe_home_view_function_is_correct(self): # noqa E302 
        view = resolve(reverse('receitas:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertTemplateUsed(response, 'receitas/pages/home.html')    # noqa W292     

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        # Recipe.objects.get(pk=1).delete()
        response = self.client.get(reverse('receitas:home'))
        self.assertIn(
            '<h1>Nenhuma receita cadastrada !</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('receitas:home'))        
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['receitas']
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1) # noqa W292 

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('receitas:home'))
        # Check if one recipe exists
        self.assertIn(
            '<h1>Nenhuma receita cadastrada !</h1>',
            response.content.decode('utf-8')
         )# noqa W292
    
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('receitas:home'))
        # Check if one recipe exists
        self.assertIn(
            '<h1>Nenhuma receita cadastrada !</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('receitas:receita', kwargs={'id': 1})
        )
        self.assertIs(view.func, views.receita)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('receitas:receita', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'receitas:receita', kwargs={'id': 1})
        )
        content = response.content.decode('utf-8')
        # Check if one recipe exists
        self.assertIn(needed_title, content)        

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'receitas:receita', kwargs={'id': recipe.id}
            )
        ) # noqa W292
        self.assertEqual(response.status_code, 404)# noqa W292

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('receitas:search'))
        self.assertIs(resolved.func, views.search)
    
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('receitas:search') + '?q=teste')
        self.assertTemplateUsed(response, 'receitas/pages/search.html')
    
    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('receitas:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

