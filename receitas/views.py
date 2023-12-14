# flake8: noqa
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http.response import Http404
from django.db.models import Q
# from utils.receitas.factory import make_recipe
from .models import Recipe


def home(request):
    receitas = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(
        request, 
        'receitas/pages/home.html',
        context={
            # 'receitas': [make_recipe() for _ in range(10)],
            'receitas': receitas,
        }
    )
def category(request, category_id): # noqa E302    
    receitas = get_list_or_404(
        Recipe.objects.filter(category__id=category_id,
                              is_published=True).order_by('-id')
    )
    return render(request, 'receitas/pages/category.html', context={
        'receitas': receitas,
        'title': f'{receitas[0].category.name} - Category | '
    })


def receita(request, id):    
    receita = get_object_or_404(Recipe, pk=id, is_published=True,)
    return render(request, 'receitas/pages/receita-detalhe.html',
        context={'receita': receita, 'is_detail_page': True} # noqa E128   
    )

def search(request):
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()
    
    receitas = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')

    return render(request, 'receitas/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': receitas,
    })