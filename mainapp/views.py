from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from mainapp.models import News


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['object_list'] = News.objects.filter(deleted=False)

        return context_data


def google_redirect_view(request):
    search_string = request.GET.get('search_string')
    return HttpResponseRedirect(f'https://www.google.com/search?q={search_string}')
