from django.views.generic import CreateView
from .models import Picture
from django.shortcuts import render
from .forms import PostForm
from django.urls import reverse_lazy
import cv2
# Create your views here.


class Home(CreateView):
  model = PostForm
  form_class = PostForm
  template_name = 'index.html'
  success_url = reverse_lazy('process')  

  def process(request):
    if request.method == 'POST':
      form = PostForm(request.POST, request.FILES)
      if form.is_valid():
        print("SAVED")
        form.save()  
    else:
      form = PostForm()
    inp = Picture.objects.last()
    img = cv2.imread(inp.img.url)
    if request.POST.get('averaging'):
      print("WORKING")
      img=cv2.blur(img,(5,5))
    else:
      print("DIDNT WORK")
    if request.POST.get('gaussian'):
      print("WORKING")
      img=cv2.GaussianBlur(img,(7,7),0)
    else:
      print("DIDNT WORK")
    output = cv2.resize(img, None, fx=2.0, fy=2.0)
    cv2.imwrite(inp.img.url, output)
    if len(Picture.objects.all()) == 1:
      return render(request,'process.html', {'pic':input})
    else:
      not_ideal = Picture.objects.all()[1:].values_list("id", flat=True)
      Picture.objects.exclude(pk__in=list(not_ideal)).delete()
    return render(request,'process.html', {'pic':inp})
  