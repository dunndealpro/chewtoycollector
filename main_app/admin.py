from django.contrib import admin

# Register your models here.
from .models import Chewtoy, Cleaning, Dog, Photo

# Register your models here
admin.site.register(Chewtoy)
admin.site.register(Cleaning)
admin.site.register(Dog)
admin.site.register(Photo)