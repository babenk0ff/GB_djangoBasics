from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse, Http404, FileResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView, View

from config import settings
from mainapp import tasks
from mainapp.forms import CourseFeedBackForm
from mainapp.models import News, Course, Lesson, CourseTeacher, CourseFeedback


class ContactsView(TemplateView):
    template_name = 'mainapp/contacts.html'

    def post(self, *args, **kwargs):
        message_body = self.request.POST.get('message_body')
        message_from = self.request.user.pk if self.request.user.is_authenticated else None
        tasks.send_feedback_to_email.delay(message_body, message_from)

        return HttpResponseRedirect(reverse_lazy('mainapp:contacts'))


class CoursesListView(ListView):
    template_name = 'mainapp/courses_list.html'
    model = Course
    paginate_by = 6


class DocSiteView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'


class LoginView(TemplateView):
    template_name = 'mainapp/login.html'


class NewsListView(ListView):
    model = News
    paginate_by = 4

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

    def get_context_data(self, pk=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['course_object'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context_data['lessons'] = Lesson.objects.filter(course=context_data['course_object'])
        context_data['teachers'] = CourseTeacher.objects.filter(course=context_data['course_object'])

        feedback_list_key = f'course_feedback_{context_data["course_object"].pk}'
        cached_feedback_list = cache.get(feedback_list_key)
        if cached_feedback_list is None:
            context_data['feedback_list'] = CourseFeedback.objects.filter(course=context_data['course_object'])
            cache.set(feedback_list_key, context_data['feedback_list'], timeout=300)
        else:
            context_data['feedback_list'] = cached_feedback_list

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

        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context_data["feedback_list"] = (
                CourseFeedback.objects.filter(course=context_data["course_object"])
                .select_related()
            )
            cache.set(f"feedback_list_{pk}", context_data["feedback_list"], timeout=300)

            # Archive object for tests --->
            import pickle

            with open(f"mainapp/fixtures/005_feedback_list_{pk}.bin", "wb") as out_file:
                pickle.dump(context_data["feedback_list"], out_file)
            # <--- Archive object for tests

        else:
            context_data["feedback_list"] = cached_feedback

        return context_data


class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedBackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('mainapp/incldues/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template})


class LogView(UserPassesTestMixin, TemplateView):
    template_name = 'mainapp/logs.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log_lines = []
        with open(settings.LOG_FILE, 'r') as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:
                    break
                log_lines.insert(0, line)

            context_data['logs'] = log_lines
        print(len(context_data['logs']))
        return context_data


class LogDownloadView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))


def google_redirect_view(request):
    search_string = request.GET.get('search_string')
    return HttpResponseRedirect(f'https://www.google.com/search?q={search_string}')
