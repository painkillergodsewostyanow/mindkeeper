from django.contrib.auth import get_user_model
from django.db import models


class Themes(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=36)
    is_private = models.BooleanField(default=False)
    parent_theme = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return f"Тема #{self.pk}, {self.title}, автор: {self.user.username}"


class Cards(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    parent_theme = models.ForeignKey(Themes, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"

    def __str__(self):
        return f"Карточка #{self.pk}, {self.title}, автор: {self.user.username}"

