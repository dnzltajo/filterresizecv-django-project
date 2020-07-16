from django.views.generic import CreateView
from .models import Picture
from django.shortcuts import render
from .forms import PostForm
from django.urls import reverse_lazy
import cv2
# Create your views here.

class Home(CreateView):
  model = Picture
  form_class = PostForm
  template_name = 'index.html'
  success_url = reverse_lazy('loading')
  
def loading(request):
  input = Picture.objects.last()
  img = cv2.imread(input.img.url)
  output = cv2.resize(img, None, fx=2.0, fy=2.0)
  cv2.imwrite(input.img.url, output)
  if len(Picture.objects.all()) == 1:
    return render(request,'loading.html', {'pic':input})
  else:
    not_ideal = Picture.objects.all()[1:].values_list("id", flat=True)
    Picture.objects.exclude(pk__in=list(not_ideal)).delete()
  return render(request,'loading.html', {'pic':input})
  