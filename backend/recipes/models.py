from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Q

from users.models import User


class Ingredient(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        db_index=True,
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единица измерения',
        help_text='Введите единицу измерения'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Тэги для рецептов с предустановленным выбором."""
    PURPLE = '#b813d1'
    GREEN = '#09db4f'
    ORANGE = '#fa6a02'
    COLOR_CHOICES = (
        (GREEN, 'Зеленый'),
        (ORANGE, 'Оранжевый'),
        (PURPLE, 'Фиолетовый')
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Введите название тега',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Название цвета "HEX"',
        unique=True,
        choices=COLOR_CHOICES,
        help_text='Выберите цвет'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='ссылка',
        help_text='Укажите уникальную ссылку'
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """
    Модель для рецептов.
    У автора не может быть создано более одного рецепта с одним именем.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Дайте имя рецепту',
        db_index=True
    )
    image = models.ImageField(
        verbose_name='Картинка рецепта',
        help_text='Добавьте изображение рецепта',
        upload_to='media/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите приготовление рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Название тегов',
        help_text='Выберите тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1, 'Минимальное время приготовления')],
        help_text='Укажите время приготовления рецепта в минутах'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-id']
        default_related_name = 'recipe'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')]

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """
    Ингридиенты для рецепта.
    Промежуточная модель между таблиц:
      Recipe и Ingredient
    """
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ингредиент',
        help_text='Укажите ингредиенты',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Минимальное количество ингредиентов 1')],
        verbose_name='Количество ингредиентов',
        help_text='Укажите количество ингредиентов'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
        help_text='Выберите рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Cостав рецепта'
        verbose_name_plural = 'Состав рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class ShoppingCart(models.Model):
    """
    Список покупок пользователя.
    Ограничения уникальности полей:
      author, recipe.
    """
    author = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Рецепт приготовления',
        on_delete=models.CASCADE,
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_cart')]

    def __str__(self):
        return f'{self.recipe}'


class Favorite(models.Model):
    """
    Список покупок пользователя.
    Ограничения уникальности полей:
      author, recipe.
    """
    author = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite',
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [models.UniqueConstraint(
            fields=['author', 'recipe'],
            name='unique_favorite')]

    def __str__(self):
        return f'{self.recipe}'


class Follow(models.Model):
    """
    Подписки на авторов рецептов.
    Ограничения уникальности полей:
      author, user.
    """
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        help_text='Текущий пользователь',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        related_name='followed',
        on_delete=models.CASCADE,
        verbose_name='Подписка',
        help_text='Подписаться на автора'
    )

    class Meta:
        verbose_name = 'Мои подписки'
        verbose_name_plural = 'Мои подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following'),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='no_self_following')]

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'
