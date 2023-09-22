from django.urls import path
from django.views.decorators.cache import cache_page

from blog import views as v
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(v.BlogEntryListView.as_view()), name='blogentry_list'),
    # path('blog/create', v.BlogEntryCreateView.as_view(), name='create_blog_entry'),
    path('view/<slug:slug>', v.BlogEntryDetailView.as_view(), name='view_blog_entry'),
    # path('update/<slug:slug>', v.BlogEntryUpdateView.as_view(), name='update_blog_entry'),
    # path('delete/<slug:slug>', v.BlogEntryDeleteView.as_view(), name='delete_blog_entry'),

]
