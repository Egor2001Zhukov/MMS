from django.db import models


class BlogEntry(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    content = models.TextField(verbose_name='Текст статьи')
    img = models.ImageField(null=True, blank=True, verbose_name='Изображение', upload_to='images/')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    is_publish = models.BooleanField(verbose_name='Опубликовано', default=False)
    slug = models.SlugField(verbose_name='slug', unique=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'

