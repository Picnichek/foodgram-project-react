from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone

from recipes.models import IngredientRecipe


def shopping_cart(self, request, author):
    """Скачивание списка продуктов для выбранных рецептов пользователя."""
    sum_ingredients_in_recipes = IngredientRecipe.objects.filter(
        recipe__shopping_cart__author=author).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
                amounts=Sum('amount')).order_by('amounts')
    today = timezone.now().strftime('%d-%m-%Y')
    shopping_list = [f'Список покупок на: {today}\n\n']
    for ingredient in sum_ingredients_in_recipes:
        shopping_list.append(f'{ingredient["ingredient__name"]} - ')
        shopping_list.append(f'{ingredient["amounts"]} ')
        shopping_list.append(f'{ingredient["ingredient__measurement_unit"]}\n')

    shopping_list.append(f'\n\nFoodgram ({timezone.now().year})')
    filename = 'shopping_list.txt'
    response = HttpResponse(''.join(shopping_list), content_type='text.plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
