from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Category

# Create your views here.

class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user = self.request.user)
    
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class UserMixin(object):
    def get_queryset(self):
        qs = super().get_querset()
        return qs.filter(user = self.request.user)
    
class UserEdit(object):
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class UserCategoryMixin(UserMixin):
    model = Category
    fields = ['subject','title', 'slug','view']
    success_url = reverse_lazy('category_list')

    
    
