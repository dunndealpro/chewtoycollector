from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3
from .models import Chewtoy, Dog, Photo
from .forms import CleaningForm
import os

# class Chewtoy:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, type, description, age):
#     self.name = name
#     self.type = type
#     self.description = description
#     self.age = age

# chewtoys = [
#   Chewtoy('Rosie Bear', 'Bear', 'such a sweetie', 3),
#   Chewtoy('Skunk', 'Rodent', 'not as smelly as you would think', 0),
#   Chewtoy('Moosh', 'Moose', 'a gentle giant', 4)
# ]

# Create your views here.
# Add the following import
from django.http import HttpResponse

# Define the home view
def home(request):
  return render(request, 'home.html') 

def about(request):
    return render(request, 'about.html') 

def chewtoys_index(request):
    chewtoys=Chewtoy.objects.all()
    return render(request, 'chewtoys/index.html', {'chewtoys': chewtoys})

def chewtoys_detail(request, chewtoy_id):
    chewtoy = Chewtoy.objects.get(id=chewtoy_id)
    id_list = chewtoy.dogs.all().values_list('id')
    dogs_chewtoys_doesnt_have = Dog.objects.exclude(id__in=id_list)
    cleaning_form=CleaningForm()
    return render(request, 'chewtoys/detail.html', 
    {'chewtoy': chewtoy,
    'cleaning_form': cleaning_form,
    'dogs': dogs_chewtoys_doesnt_have
    })

def add_cleaning(request, chewtoy_id):
  # create a ModelForm instance using the data in request.POST
  form = CleaningForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_cleaning = form.save(commit=False)
    new_cleaning.chewtoy_id = chewtoy_id
    new_cleaning.save()
  return redirect('detail', chewtoy_id=chewtoy_id)

def assoc_dog(request, chewtoy_id, dog_id):
  # Note that you can pass a dog's id instead of the whole dog object
  Chewtoy.objects.get(id=chewtoy_id).dogs.add(dog_id)
  return redirect('detail', chewtoy_id=chewtoy_id)

def unassoc_dog(request, chewtoy_id, dog_id):
  chewtoy = chewtoy.objects.get(id=chewtoy_id)
  chewtoy.dogs.remove(dog_id)
  return redirect('detail', chewtoy_id=chewtoy_id)

class ChewtoyCreate(CreateView):
    model = Chewtoy
    fields = ['name', 'type', 'description', 'age']
    success_url = '/chewtoys/'

class ChewtoyUpdate(UpdateView):
    model = Chewtoy
    fields = ['type', 'description', 'age']

class ChewtoyDelete(DeleteView):
    model = Chewtoy
    success_url = '/chewtoys/'

class DogList(ListView):
    model = Dog

class DogDetail(DetailView):
    model = Dog

class DogCreate(CreateView):
  model = Dog
  fields = '__all__'

class DogUpdate(UpdateView):
    model = Dog
    fields = ['name', 'color']

class DogDelete(DeleteView):
    model = Dog
    success_url = '/dogs/'

def add_photo(request, chewtoy_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to chewtoy_id or chewtoy (if you have a chewtoy object)
            Photo.objects.create(url=url, chewtoy_id=chewtoy_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', chewtoy_id=chewtoy_id)    