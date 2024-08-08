from django.contrib import admin
from .models import UserModel, PetCategory, Pet, Adoption,ProfileImage
# Register your models here
admin.site.register(UserModel)
admin.site.register(PetCategory)
admin.site.register(Pet)
admin.site.register(ProfileImage)

admin.site.register(Adoption)
