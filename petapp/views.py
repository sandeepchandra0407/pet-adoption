from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import UserModel
from django.contrib import messages
from functools import wraps



def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.usermodel.is_user:
            return view_func(request, *args, **kwargs)
        return redirect('login_page')  
    return _wrapped_view

def donater_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.usermodel.is_donater:
            return view_func(request, *args, **kwargs)
        return redirect('login_page') 
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.usermodel.is_admin:
            return view_func(request, *args, **kwargs)
        return redirect('login_page')  
    return _wrapped_view





def homepage(request):
    pets = Pet.objects.filter(is_approved=True,pet_status="Active")
    print(pets.values())
    return render(request, 'user/home.html', {'pets': pets})


def pet_detail(request, pk):
    pet_obj = get_object_or_404(Pet, pk=pk)
    # images = PetImage.objects.filter(pet=pet_obj)
    return render(request, 'user/pet_detail.html', {'pet': pet_obj})


def login_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_password = request.POST.get('password')
        user_obj = authenticate(username=user_name,password = user_password)
        if user_obj is not None:
            login(request,user_obj)
            return redirect('/')

    return render(request,'user/login.html')




@user_required
def adopt_page(request,id):
     pet_obj = Pet.objects.get(id=id)
     pet_obj.pet_status= "Inactive"
     pet_obj.save()
     user_obj= request.user
     adoption_obj = Adoption()
     adoption_obj.buyer= user_obj
     adoption_obj.pet=pet_obj
     adoption_obj.save()
     
     return redirect('/')

def pet_list(request):
    pets = Pet.objects.filter(is_approved=True,pet_status="Active")
    categories = PetCategory.objects.all()
    if request.method == "POST":
        search_text = request.POST.get('search_text')
        category_id = request.POST.get('category')
        if search_text:
            pets = pets.filter(name__icontains=search_text)
        if category_id:
            pets = pets.filter(category=PetCategory.objects.get(id=category_id))
    context = {
        'pets': pets,
        'categories': categories
    }
    return render(request, 'user/pets.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to home page after logout

@user_required
def adopted_pets_view(request):
    if request.user.is_authenticated:
        user_obj= request.user
        adopted_pets = Adoption.objects.filter(buyer=user_obj)
    else:
        adopted_pets = []

    context = {
        'adopted_pets': adopted_pets
    }
    return render(request, 'user/adopted_pets.html', context)

import random

def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        Password = request.POST['Password']
        address = request.POST['address']
        role = request.POST['role']

        is_user = role == 'user'
        is_donater = role == 'donater'

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('user/register_page')

        # password = str(random.randint(100000, 999999))
        user_obj = User.objects.create_user(username=username, password=Password, email=email, first_name=first_name, last_name=last_name)
        UserModel.objects.create(user=user_obj, mobile_number=mobile_number, address=address, is_user=is_user, is_donater=is_donater)
        
        # send_mail(
        #     'Registration Confirmation',
        #     f'Your account has been created. Your password is {password}.',
        #     'petdonation34@gmail.com',
        #     [email],
        #     fail_silently=False,
        # )
        
        messages.success(request, 'Registration successful. Check your email for the password.')
        return redirect('login_page')

    return render(request, 'user/register.html')


    
# @login_required(login_url='/login_page')
# def change_password(request):
#     if request.method=="POST":
#         password = request.POST.get('password')
#         user_obj = request.user
#         user_obj.set_password(password)


def admin_dashboard(request):
    total_users = UserModel.objects.filter(is_user=True).count()
    total_donors = UserModel.objects.filter(is_donater=True).count()
    total_approved_pets = Pet.objects.filter(is_approved=True).count()
    pending_pets = Pet.objects.filter(is_approved=False,pet_status="Active")
    print(User.objects.all().values())

    context = {
        'total_users': total_users,
        'total_donors': total_donors,
        'total_approved_pets': total_approved_pets,
        'pending_pets': pending_pets,
    }

    return render(request, 'admin/admin_dashboard.html', context)


def approve_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.is_approved = True
    pet.save()
    return redirect("/admin-dashboard")
def reject_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.is_approved = False
    pet.pet_status="Rejected"
    pet.save()
    return redirect("/admin-dashboard")


def category_dashboard(request):
    categories = PetCategory.objects.all()
    return render(request, 'admin/add_category.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        PetCategory.objects.create(name=name)
    return redirect("category")

def delete_category(request, category_id):
    category = PetCategory.objects.get(id=category_id)
    category.delete()
    return redirect("category")



def user_details_admin(request):
    user_s = UserModel.objects.filter(is_user=True)
  
    context = {
        'users' : user_s
        }
    return render(request,'admin/user_details.html', context)


def doner_details_admin(request):
    doner_s = UserModel.objects.filter(is_donater=True)
   
    context = {
        'doners' : doner_s,
      
        }
    return render(request,'admin/doner_details.html', context)

def admin_adoption_details(request):
    adoptions = Adoption.objects.all()
    return render(request, 'admin/purchase.html', {'adoptions': adoptions})

def donor_donated_pets(request, donor_id):
    print(User.objects.filter(id = donor_id).values())
    donor = get_object_or_404(User, id=donor_id)
    donated_pets = Pet.objects.filter(donor=donor)
    return render(request, 'admin/individual_donors.html', {'donor': donor, 'donated_pets': donated_pets})

'''This is for git study'''