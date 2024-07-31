from django.db import models
from django.contrib.auth.models import User

# Extend the default user model
class UserModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_donater = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True,null=True)
    user_status = models.CharField(max_length=50,default='pending')
    def __str__(self) -> str:
        return self.user.username

class ProfileImage(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile',null=True)


class PetCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Pet(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(PetCategory, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField()
    is_approved = models.BooleanField(default=False)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donated_pets')
    create_at = models.DateTimeField(auto_now_add=True,null=True)
    pet_status = models.CharField(max_length=50,default="Active")
    pet_image = models.ImageField(upload_to='pet_images',null=True)

    def __str__(self):
        return self.name
    
# class PetImage(models.Model):
#     image = models.ImageField(upload_to='pet_images')
#     pet = models.ForeignKey(Pet,on_delete=models.CASCADE)
    

class Adoption(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adopted_pets')
    adoption_date = models.DateTimeField(auto_now_add=True)
    adoption_status = models.CharField(max_length=50,default='pending')
    create_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.pet.name} adopted by {self.buyer.username}"
    


