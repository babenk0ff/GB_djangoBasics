from django.contrib import admin

from mainapp.models import News, Course, Lesson, CourseTeacher


admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseTeacher)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'deleted', 'slug')
    list_filter = ('deleted', 'created_at',)
    ordering = ('pk',)
    list_per_page = 3
    search_fields = ('title', 'preamble', 'body',)
    actions = ('mark_as_deleted',)

    def slug(self, obj):
        return obj.title.lower().replace(' ', '-')

    slug.short_description = 'Слаг'

    def mark_as_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_deleted.short_description = 'Пометить удаленным'
