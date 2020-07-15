from django.views.generic import CreateView
from .models import Picture
from django.shortcuts import render
from .forms import PostForm
from django.urls import reverse_lazy
# Create your views here.
class Home(CreateView):
  model = Picture
  form_class = PostForm
  template_name = 'index.html'
  success_url = reverse_lazy('home')
#def home(request):
# form_class = PostForm
#  return render(request, 'index.html', {'form':form_class})
