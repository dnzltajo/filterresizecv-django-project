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

  #Save form
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
      print("averaging")
      kernel = int(request.POST.get('myrangeId',""))
      print(kernel)
      img=cv2.blur(img,(kernel,kernel))
    else:
      print("no averaging")
    if request.POST.get('gaussian'):
      print("gaussian")
      kernel = int(request.POST.get('myrangeId2',""))      
      print(kernel)
      img=cv2.GaussianBlur(img,(kernel,kernel),0)
    else:
      print("no gaussian")
    if request.POST.get('median'):
      print("median")
      kernel = int(request.POST.get('myrangeId3',""))      
      print(kernel)      
      img=cv2.medianBlur(img, kernel)
    else:
      print("no median")
    if request.POST.get('bilateral'):
      print("bilateral")
      kernel = int(request.POST.get('myrangeId4',""))      
      print(kernel)          
      img=cv2.bilateralFilter(img,kernel,75,75)
    else:
      print("no bilateral")            
    length = float(request.POST.get('scale'))
    if request.POST.get('interpolate') == 'nearest':
      output = cv2.resize(img, None,fx=length, fy=length,interpolation = cv2.INTER_NEAREST)
    elif request.POST.get('interpolate') == 'linear':
      output = cv2.resize(img, None,fx=length, fy=length,interpolation = cv2.INTER_LINEAR)   
    elif request.POST.get('interpolate') == 'area':      
      output = cv2.resize(img, None,fx=length, fy=length,interpolation = cv2.INTER_AREA)   
    elif request.POST.get('interpolate') == 'cubic':      
      output = cv2.resize(img, None,fx=length, fy=length,interpolation = cv2.INTER_CUBIC)     
    elif request.POST.get('interpolate') == 'lanczos':      
      output = cv2.resize(img, None,fx=length, fy=length,interpolation = cv2.INTER_LANCZOS4) 
    else:
      output = cv2.resize(img, None,fx=length, fy=length)     
    cv2.imwrite(inp.img.url, output)
    if len(Picture.objects.all()) == 0 or len(Picture.objects.all()) == 1:
      return render(request,'process.html', {'pic':input})
    else:
      not_ideal = Picture.objects.all()[1:].values_list("id", flat=True)
      Picture.objects.exclude(pk__in=list(not_ideal)).delete()
    return render(request,'process.html', {'pic':inp})
  