from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Обновлен')
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class News(CommonModel):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1024, verbose_name='Вступление')

    body = models.TextField(verbose_name='Содержимое')
    body_as_markdown = models.BooleanField(default=False, verbose_name='Разметка Markdown')

    def __str__(self):
        return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Course(CommonModel):
    name = models.CharField(max_length=256, verbose_name='Название')
    description = models.CharField(max_length=1024, verbose_name='Описание')

    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость', default=0)
    cover = models.CharField(max_length=25, default='img/no_image.svg', verbose_name='Cover')
    description_as_markdown = models.BooleanField(default=False, verbose_name='Разметка Markdown')

    def __str__(self):
        return f'{self.pk} {self.name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(CommonModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    num = models.PositiveIntegerField(default=0, verbose_name='Номер урока')

    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'#{self.num} {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseTeacher(CommonModel):
    course = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')

    def __str__(self):
        return '{0:0>3} {1} {2}'.format(self.pk, self.last_name, self.first_name)

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курс к учителям'


class CourseFeedback(CommonModel):
    RATING_FIVE = 5

    RATINGS = (
        (RATING_FIVE, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='')
    rating = models.SmallIntegerField(choices=RATINGS, default=RATING_FIVE, verbose_name='Рейтинг')
    feedback = models.TextField(verbose_name='Отзыв', default='Без отзыва')

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''

    def __str__(self):
        return f'Отзыв на {self.course} от {self.user}'
