from django.contrib import admin
from .models import UserModel, PetCategory, Pet, Adoption

# Register your models here
admin.site.register(UserModel)
admin.site.register(PetCategory)
admin.site.register(Pet)

admin.site.register(Adoption)
