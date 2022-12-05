from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from mainapp.forms import CourseFeedBackForm
from mainapp.models import News, Course, Lesson, CourseTeacher, CourseFeedback


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'


class CoursesListView(ListView):
    template_name = 'mainapp/courses_list.html'
    model = Course


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class NewsDetailView(DetailView):
    model = News

    def get_object(self, queryset=None):
        if super().get_object().deleted is True:
            raise Http404
        return super().get_object()


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',)


class CourseDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['course_object'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CourseTeacher.objects.filter(course=context_data['course_object'])
        context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])

        user = self.request.user
        feedback_list = context_data['feedback_list']

        if user.is_authenticated:
            if feedback_list:
                for feedback in feedback_list:
                    if feedback.user.pk == self.request.user.pk:
                        return context_data

            context_data['feedback_form'] = CourseFeedBackForm(
                course=context_data['course_object'],
                user=self.request.user
            )

        return context_data


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedBackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/incldues/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})


def google_redirect_view(request):
    search_string = request.GET.get('search_string')
    return HttpResponseRedirect(f'https://www.google.com/search?q={search_string}')
