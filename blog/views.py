from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic as g

from blog import forms as f
from blog.models import BlogEntry


class BlogEntryListView(g.ListView):
    model = BlogEntry

    def get_queryset(self):
        return super().get_queryset().filter(is_publish=True)


class BlogEntryDetailView(LoginRequiredMixin, g.DetailView):
    model = BlogEntry

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


# class BlogEntryCreateView(LoginRequiredMixin, PermissionRequiredMixin, g.CreateView):
#     form_class = f.BlogEntryForm
#     template_name = 'blog/blogentry_form.html'
#     permission_required = 'catalog.add_blogentry'
#
#     def get_success_url(self):
#         return reverse('blog:view_blog_entry', kwargs={'slug': self.object.slug})
#
#
# class BlogEntryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, g.DeleteView):
#     model = BlogEntry
#     success_url = reverse_lazy('catalog:blog')
#     permission_required = 'catalog.delete_blogentry'
#
#
# class BlogEntryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, g.UpdateView):
#     model = BlogEntry
#     form_class = f.BlogEntryForm
#     success_url = reverse_lazy('catalog:blog')
#     permission_required = 'catalog.change_blogentry'
