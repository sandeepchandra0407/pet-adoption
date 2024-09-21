from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import UserModel
from django.contrib import messages
from functools import wraps
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re
from django.contrib.auth import update_session_auth_hash


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
    pets = Pet.objects.filter(pet_status="Active")
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
            if user_obj.usermodel.is_donater:
                return redirect('doner_home')
            if user_obj.usermodel.is_admin:
                return redirect('admin-dashboard/')
            else:
                return redirect('/')
        return render(request,'user/login.html',{'status':True})
        
            

    return render(request,'user/login.html')

@user_required
def user_self_profile(request):
    user = request.user
    return render(request, 'user/user_self_profile.html',{'user_model': user})


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
    pets = Pet.objects.filter(pet_status="Active")
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

# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST['firstname']
#         last_name = request.POST['lastname']
#         username = request.POST['username']
#         email = request.POST['email']
#         mobile_number = request.POST['mobile_number']
#         Password = request.POST['Password']
#         address = request.POST['address']
#         role = request.POST['role']

#         is_user = role == 'user'
#         is_donater = role == 'donater'

#         if User.objects.filter(email=email).exists():
#             messages.error(request, 'Email is already registered.')
#             return redirect('register_page')

#         # password = str(random.randint(100000, 999999))
#         user_obj = User.objects.create_user(username=username, password=Password, email=email, first_name=first_name, last_name=last_name)
#         UserModel.objects.create(user=user_obj, mobile_number=mobile_number, address=address, is_user=is_user, is_donater=is_donater)
        
#         # send_mail(
#         #     'Registration Confirmation',
#         #     f'Your account has been created. Your password is {password}.',
#         #     'petdonation34@gmail.com',
#         #     [email],
#         #     fail_silently=False,
#         # )
        
#         messages.success(request, 'Registration successful. Check your email for the password.')
#         return redirect('login_page')

#     return render(request, 'user/register.html')

def validate_email_address(email):
    validator = EmailValidator(message="Invalid email format.")
    try:
        validator(email)
    except ValidationError:
        raise ValidationError("Invalid email format.")

    # Additional check for common domains (optional)
    domain = email.split('@')[-1]
    if not re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', domain):
        raise ValidationError("Invalid email domain.")

    return email

def validate_phone_number(phone_number):
    if not phone_number.isdigit():
        raise ValidationError("Phone number must contain only digits.")
    
    if len(phone_number) != 10:
        raise ValidationError("Phone number must be exactly 10 digits long.")
    
    return phone_number

def register(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        password = request.POST['Password']  # This line is present but no password validation is performed
        address = request.POST['address']
        role = request.POST['role']

        is_user = role == 'user'
        is_donater = role == 'donater'

        # Validation
        errors = {}
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username is already registered.'
        
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email is already registered.'
        else:
            try:
                validate_email_address(email)
            except ValidationError as e:
                errors['email'] = str(e)

        try:
            validate_phone_number(mobile_number)
        except ValidationError as e:
            print(str(e))
            errors['mobile_number'] = str(list(e)[0])
            print(errors)

        if errors:
            # If there are validation errors, display them on the form
            for key, error in errors.items():
                messages.error(request, f"{key}: {error}")
            return render(request, 'user/register.html', {
                'errors': errors,
                'data': request.POST
            })

        # If no errors, create the user
        user_obj = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        UserModel.objects.create(user=user_obj, mobile_number=mobile_number, address=address, is_user=is_user, is_donater=is_donater)

        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login_page')

    return render(request, 'user/register.html')
    
# @login_required(login_url='/login_page')
# def change_password(request):
#     if request.method=="POST":
#         password = request.POST.get('password')
#         user_obj = request.user
#         user_obj.set_password(password)

@user_required
def user_self_delete(request,pk):
    value = UserModel.objects.get(id=pk)
    value.delete()
    return redirect('register_page')


@user_required
def user_edit_profile(request, user_id):
    user_instance = get_object_or_404(UserModel, id=user_id)
    

    if request.method == 'POST': 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        username = request.POST.get('username')


        errors = {}
        if user_instance.user.username != username:
            if User.objects.filter(username=username).exists():
                errors['username'] = 'Username is already registered.'
        if user_instance.user.email != email:
            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email is already registered.'
            else:
                try:
                    validate_email_address(email)
                except ValidationError as e:
                    errors['email'] = str(list(e)[0])


        try:
            validate_phone_number(mobile_number)
        except ValidationError as e:
            print(str(e))
            errors['mobile_number'] = str(list(e)[0])
            print(errors)

        if errors:
            # If there are validation errors, display them on the form
            for key, error in errors.items():
                messages.error(request, f"{key}: {error}")
            return render(request, 'user/user_edit_profile.html', {
                'errors': errors,
                'data': user_instance
            })



        # Update user model
        use_obj = user_instance.user
        use_obj.first_name = first_name
        use_obj.last_name = last_name
        use_obj.email = email
        use_obj.username = username
        use_obj.save()

        # Update user profile
        user_instance.mobile_number = mobile_number
        user_instance.address = address
        user_instance.save()

        # Handle profile image
        if 'profile_image' in request.FILES:
            image = request.FILES['profile_image']
            if ProfileImage.objects.filter(user=use_obj):
                profile_image_instance = use_obj.profileimage
                profile_image_instance.profile_image.delete()  # Delete old image
                profile_image_instance.profile_image = image
                profile_image_instance.save()
            else:
                profile_image_obj = ProfileImage()
                profile_image_obj.profile_image = image
                profile_image_obj.user = use_obj
                profile_image_obj.save()
                # ProfileImage.objects.create(user=use_obj, profile_image=image)
        return redirect('user_self_profile')



    context = {
        'data': user_instance
        
    }
    return render(request, 'user/user_edit_profile.html', context)




@admin_required
def admin_dashboard(request):
    total_users = UserModel.objects.filter(is_user=True).count()
    total_donors = UserModel.objects.filter(is_donater=True).count()
    total_approved_pets = Pet.objects.all().count()
    pending_pets = Pet.objects.filter(pet_status="Pending")


    context = {
        'total_users': total_users,
        'total_donors': total_donors,
        'total_approved_pets': total_approved_pets,
        'pending_pets': pending_pets,
    }

    return render(request, 'admin/admin_dashboard.html', context)

@admin_required
def approve_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.pet_status="Active"
    pet.save()
    return redirect("/admin-dashboard")
@admin_required
def admin_self_profile(request):
    user = request.user
    return render(request, 'admin/admin_profile.html',{'user': user})


@admin_required
def admin_edit_profile(request):
    user_instance = request.user
    

    if request.method == 'POST': 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        username = request.POST.get('username')


        errors = {}
        if user_instance.username != username:
            if User.objects.filter(username=username).exists():
                errors['username'] = 'Username is already registered.'
        if user_instance.email != email:
            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email is already registered.'
            else:
                try:
                    validate_email_address(email)
                except ValidationError as e:
                    errors['email'] = str(list(e)[0])


        try:
            validate_phone_number(mobile_number)
        except ValidationError as e:
            print(str(e))
            errors['mobile_number'] = str(list(e)[0])
            print(errors)

        if errors:
            # If there are validation errors, display them on the form
            for key, error in errors.items():
                messages.error(request, f"{key}: {error}")
            return render(request, 'admin/admin_edit_profile.html', {
                'errors': errors,
                'data': user_instance
            })



        # Update user model
        use_obj = user_instance
        use_obj.first_name = first_name
        use_obj.last_name = last_name
        use_obj.email = email
        use_obj.username = username
        use_obj.save()

        # Update user profile
        user_model_obj = user_instance.usermodel

        user_model_obj.mobile_number = mobile_number
        user_model_obj.address = address
        user_model_obj.save()

        # Handle profile image
        if 'profile_image' in request.FILES:
            image = request.FILES['profile_image']
            if ProfileImage.objects.filter(user=use_obj):
                profile_image_instance = use_obj.profileimage
                profile_image_instance.profile_image.delete()  # Delete old image
                profile_image_instance.profile_image = image
                profile_image_instance.save()
            else:
                profile_image_obj = ProfileImage()
                profile_image_obj.profile_image = image
                profile_image_obj.user = use_obj
                profile_image_obj.save()

        return redirect('admin_self_profile')


    context = {
        'data': user_instance
        
    }
    return render(request, 'admin/admin_edit_profile.html', context)


@admin_required
def reject_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    pet.pet_status="Rejected"
    pet.save()
    return redirect("/admin-dashboard")

@admin_required
def category_dashboard(request):
    categories = PetCategory.objects.all()
    return render(request, 'admin/add_category.html', {'categories': categories})

@admin_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        PetCategory.objects.create(name=name)
    return redirect("category")
@admin_required
def delete_category(request, category_id):
    category = PetCategory.objects.get(id=category_id)
    category.delete()
    return redirect("category")


@admin_required
def user_details_admin(request):
    user_s = UserModel.objects.filter(is_user=True)
  
    context = {
        'users' : user_s
        }
    return render(request,'admin/user_details.html', context)

@admin_required
def doner_details_admin(request):
    doner_s = UserModel.objects.filter(is_donater=True)
   
    context = {
        'doners' : doner_s,
      
        }
    return render(request,'admin/doner_details.html', context)

@admin_required
def admin_adoption_details(request):
    adoptions = Adoption.objects.all()
    return render(request, 'admin/purchase.html', {'adoptions': adoptions})

@admin_required
def donor_donated_pets(request, donor_id):
    print(User.objects.filter(id = donor_id).values())
    donor = get_object_or_404(User, id=donor_id)
    donated_pets = Pet.objects.filter(donor=donor)
    return render(request, 'admin/individual_donors.html', {'donor': donor, 'donated_pets': donated_pets})

# def user_edit_admin(request,pk):
#     data = UserModel.objects.get(id=pk)
#     return render(request,'admin/user_edit.html',{'data':data})


# def doner_edit_admin(request,pk):
#     data = UserModel.objects.get(id=pk)
#     return render(request,'admin/doner_edit.html',{'data':data})
@admin_required
def user_delete(request,pk):
    value = UserModel.objects.get(id=pk)
    value.delete()
    return redirect('user_details_admin')
@admin_required
def doner_delete(request,pk):
    value = UserModel.objects.get(id=pk)
    value.delete()
    return redirect('doner_details_admin')
@admin_required
def admin_edit_user(request, user_id):
    user_instance = get_object_or_404(UserModel, id=user_id)
    

    if request.method == 'POST': 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        username = request.POST.get('username')


        errors = {}
        if user_instance.user.username != username:
            if User.objects.filter(username=username).exists():
                errors['username'] = 'Username is already registered.'
        if user_instance.user.email != email:
            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email is already registered.'
            else:
                try:
                    validate_email_address(email)
                except ValidationError as e:
                    errors['email'] = str(list(e)[0])


        try:
            validate_phone_number(mobile_number)
        except ValidationError as e:
            print(str(e))
            errors['mobile_number'] = str(list(e)[0])
            print(errors)

        if errors:
            # If there are validation errors, display them on the form
            for key, error in errors.items():
                messages.error(request, f"{key}: {error}")
            return render(request, 'admin/admin_edit_user.html', {
                'errors': errors,
                'data': user_instance
            })



        # Update user model
        use_obj = user_instance.user
        use_obj.first_name = first_name
        use_obj.last_name = last_name
        use_obj.email = email
        use_obj.username = username
        use_obj.save()

        # Update user profile
        user_instance.mobile_number = mobile_number
        user_instance.address = address
        user_instance.save()

        # Handle profile image
        if 'profile_image' in request.FILES:
            image = request.FILES['profile_image']
            if ProfileImage.objects.filter(user=use_obj):
                profile_image_instance = use_obj.profileimage
                profile_image_instance.profile_image.delete()  # Delete old image
                profile_image_instance.profile_image = image
                profile_image_instance.save()
            else:
                profile_image_obj = ProfileImage()
                profile_image_obj.profile_image = image
                profile_image_obj.user = use_obj
                profile_image_obj.save()
                # ProfileImage.objects.create(user=use_obj, profile_image=image)


        if user_instance.is_user:
             return redirect('user_details_admin')
        else:
             return redirect('doner_details_admin')
    context = {
        'data': user_instance
        
    }
    return render(request, 'admin/admin_edit_user.html', context)


@donater_required
def doner_home(request):
    donter_obj = request.user
    # usermodel_obj= donter_obj.usermodel
    # usermodel_obj.address - "kollom"
    pet_data = Pet.objects.filter(donor=donter_obj)
    return render(request,'doner/doner_home.html',{'pets': pet_data})

@admin_required
def edit_category_page(request,pk):
    data = PetCategory.objects.get(id=pk)
    return render(request,'admin/edit_category.html',{'data':data})

@admin_required
def edit_category(request):
    id = request.POST.get('id')
    cat_name = request.POST.get('name')

    data = PetCategory.objects.get(id=id)
    data.name = cat_name
    data.save()
    return redirect('category')


@admin_required
def admin_change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_obj = request.user
        errors ={}
        

        if not user_obj.check_password(old_password):
            print('old check')
            errors['old_password'] ='Old password is incorrect.'
            # errors==={'old_password': 'Old password is incorrect.'}
            return render(request, 'admin/admin_change_pass.html',{'errors':errors})
        
        try:
            validate_password_complexity(new_password)
        except ValidationError as e:
            errors['new_password'] = str(list(e)[0])
            return render(request, 'admin/admin_change_pass.html',{'errors':errors})

        

        if new_password != confirm_password:
            print('check')
            errors['check_password'] = 'New password and confirm password do not match.'
            return render(request, 'admin/admin_change_pass.html',{'errors':errors})
       
        user_obj.set_password(new_password)
        user_obj.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your password has been changed successfully.')
        return redirect('admin_dashboard')

    return render(request,'admin/admin_change_pass.html')

@admin_required
def admin_edit_pet_page(request,pk):
    pet_data = Pet.objects.get(id=pk)
    cat_data = PetCategory.objects.all()
    return render(request,'admin/admin_edit_pet.html',{'value':pet_data,'data':cat_data})

@admin_required
def admin_edit_pet(request,pk):
    if request.method == 'POST':

        data = Pet.objects.get(id = pk)


        old = data.pet_image
        new = request.FILES.get('pet_img')

        if old != None and new == None:
            data.pet_image = old
        else:  
            data.pet_image = new

        
        data.name = request.POST.get('petName')
        data.description = request.POST.get('description')
        data.price = request.POST.get('price')
        select = request.POST.get('category')
        pet_c = PetCategory.objects.get(id=select)
        data.category= pet_c
        data.save()
        return redirect('doner_details_admin')
    else:
        return redirect('admin_edit_pet_page')




@donater_required
def donor_self_profile(request):
    user = request.user
    return render(request, 'doner/doner_self_profile.html',{'user_model': user})
# @donater_required
# def doner_edit_profilepage(request,pk):
#     value = UserModel.objects.get(id=pk)
#     return render(request,'doner/doner_edit_profile.html',{'value':value})
@donater_required
def doner_edit_profile(request, user_id):
    user_instance = get_object_or_404(UserModel, id=user_id)
    

    if request.method == 'POST': 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        address = request.POST.get('address')
        username = request.POST.get('username')


        errors = {}
        if user_instance.user.username != username:
            if User.objects.filter(username=username).exists():
                errors['username'] = 'Username is already registered.'
        if user_instance.user.email != email:
            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email is already registered.'
            else:
                try:
                    validate_email_address(email)
                except ValidationError as e:
                    errors['email'] = str(list(e)[0])


        try:
            validate_phone_number(mobile_number)
        except ValidationError as e:
            print(str(e))
            errors['mobile_number'] = str(list(e)[0])
            print(errors)

        if errors:
            # If there are validation errors, display them on the form
            for key, error in errors.items():
                messages.error(request, f"{key}: {error}")
            return render(request, 'doner/doner_edit_profile.html', {
                'errors': errors,
                'data': user_instance
            })



        # Update user model
        use_obj = user_instance.user
        use_obj.first_name = first_name
        use_obj.last_name = last_name
        use_obj.email = email
        use_obj.username = username
        use_obj.save()

        # Update user profile
        user_instance.mobile_number = mobile_number
        user_instance.address = address
        user_instance.save()

        # Handle profile image
        if 'profile_image' in request.FILES:
            image = request.FILES['profile_image']
            if ProfileImage.objects.filter(user=use_obj):
                profile_image_instance = use_obj.profileimage
                profile_image_instance.profile_image.delete()  # Delete old image
                profile_image_instance.profile_image = image
                profile_image_instance.save()
            else:
                profile_image_obj = ProfileImage()
                profile_image_obj.profile_image = image
                profile_image_obj.user = use_obj
                profile_image_obj.save()
                # ProfileImage.objects.create(user=use_obj, profile_image=image)
        return redirect('doner_self_profile')



    context = {
        'data': user_instance
        
    }
    return render(request, 'doner/doner_edit_profile.html', context)


def donar_self_delete(request,pk):
    value = UserModel.objects.get(id=pk)
    value.delete()
    return redirect('register_page')


@donater_required
def add_pet_page(request):
    cat = PetCategory.objects.all()
    return render(request,'doner/add_pet.html',{'data':cat})

@donater_required
def add_pet(request):
    if request.method == 'POST':
        pet_name = request.POST.get('petName')
        select = request.POST.get('category')
        pet_description = request.POST.get('description')
        pet_price = request.POST.get('price')
        pet_img = request.FILES.get('image')
        pet_category = PetCategory.objects.get(id=select)
        regi_pet = Pet()
        regi_pet.donor = request.user
        regi_pet.name = pet_name
        regi_pet.category = pet_category
        regi_pet.description = pet_description
        regi_pet.price = pet_price
        regi_pet.pet_image = pet_img
        regi_pet.save()
    return redirect('doner_home')

@donater_required
def edit_pet_page(request,pk):
    pet_data = Pet.objects.get(id=pk)
    cat_data = PetCategory.objects.all()
    return render(request,'doner/edit_pet.html',{'value':pet_data,'data':cat_data})
@donater_required
def edit_pet(request,pk):
    if request.method == 'POST':

        data = Pet.objects.get(id = pk)


        old = data.pet_image
        new = request.FILES.get('pet_img')

        if old != None and new == None:
            data.pet_image = old
        else:  
            data.pet_image = new

        
        data.name = request.POST.get('petName')
        data.description = request.POST.get('description')
        data.price = request.POST.get('price')
        data.donor = request.user
        select = request.POST.get('category')
        pet_c = PetCategory.objects.get(id=select)
        data.category= pet_c
        data.save()
        return redirect('doner_home')
    else:
        return redirect('edit_pet_page')
    
@donater_required
def pet_del_doner(request,pk):
    value = Pet.objects.get(id=pk)
    value.delete()
    return redirect('doner_home')


def validate_password_complexity(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    
    if not re.search(r'[@$!%*?&#]', password):
        raise ValidationError("Password must contain at least one special symbol (@, $, !, %, *, ?, &, #).")
    
    return password

@donater_required
def doner_change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_obj = request.user
        errors ={}
        

        if not user_obj.check_password(old_password):
            print('old check')
            errors['old_password'] ='Old password is incorrect.'
            # errors==={'old_password': 'Old password is incorrect.'}
            return render(request, 'doner/change_password.html',{'errors':errors})
        
        try:
            validate_password_complexity(new_password)
        except ValidationError as e:
            errors['new_password'] = str(list(e)[0])
            return render(request, 'doner/change_password.html',{'errors':errors})

        

        if new_password != confirm_password:
            print('check')
            errors['check_password'] = 'New password and confirm password do not match.'
            return render(request, 'doner/change_password.html',{'errors':errors})
       
        user_obj.set_password(new_password)
        user_obj.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your password has been changed successfully.')
        return redirect('doner_home')

    return render(request, 'doner/change_password.html')



@user_required
def user_change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user_obj = request.user
        errors ={}
        

        if not user_obj.check_password(old_password):
            print('old check')
            errors['old_password'] ='Old password is incorrect.'
            # errors==={'old_password': 'Old password is incorrect.'}
            return render(request, 'user/user_change_pass.html',{'errors':errors})
        
        try:
            validate_password_complexity(new_password)
        except ValidationError as e:
            errors['new_password'] = str(list(e)[0])
            return render(request, 'user/user_change_pass.html',{'errors':errors})

        

        if new_password != confirm_password:
            print('check')
            errors['check_password'] = 'New password and confirm password do not match.'
            return render(request, 'user/user_change_pass.html',{'errors':errors})
       
        user_obj.set_password(new_password)
        user_obj.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Your password has been changed successfully.')
        return redirect('user_self_profile')

    return render(request,'user/user_change_pass.html')