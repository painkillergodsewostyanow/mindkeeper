from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


class IndexTemplateView(View):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(request, 'main/index_for_authenticated.html')
        # TODO()
        return render(request, 'main/index_for_not_authenticated.html')


