from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models


class Themes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=36)
    is_private = models.BooleanField(default=False)

    search_vector = SearchVectorField(null=True, blank=True)

    theme = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        indexes = [GinIndex(fields=["search_vector"])]

    def __str__(self):
        return f"Тема #{self.pk}, {self.title}, автор: {self.user.username}"

    def update_search_vector(self, *args):
        qs = Themes.objects.filter(pk=self.pk)
        qs.update(search_vector=SearchVector(*args))


class Cards(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    theme = models.ForeignKey(Themes, on_delete=models.CASCADE)

    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        indexes = [GinIndex(fields=["search_vector"])]

    def __str__(self):
        return f"Карточка #{self.pk}, {self.title}, автор: {self.user.username}"

    def update_search_vector(self, *args):
        qs = Cards.objects.filter(pk=self.pk)
        qs.update(search_vector=SearchVector(*args))
