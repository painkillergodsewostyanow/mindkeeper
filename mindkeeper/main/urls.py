from django.urls import path
from .views import IndexTemplateView

app_name = "main"


urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index')
]
