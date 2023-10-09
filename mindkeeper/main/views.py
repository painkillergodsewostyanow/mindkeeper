from django.shortcuts import render
from django.views import View


class IndexTemplateView(View):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(request, 'main/index.html')
        # TODO()
        return render(request, 'main/index.html')


