from django.urls import path
from receitas import views

app_name = 'receitas'

urlpatterns = [
    path('', views.home, name="home"),  # Home
    path('receitas/<int:id>/', views.receita , name="receita"),  # Receitas
    path('receitas/category/<int:category_id>/', views.category, name="category"),
]