from django.urls import path
from . import views 

urlpatterns = [
    
    path('', views.homepage, name='homepage'),
    path('pet/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('login_page',views.login_page,name='login_page'),
    path('register_page',views.register,name='register_page'),
    path('adopt/<int:id>',views.adopt_page,name='adopt_page'),
    path('pets/', views.pet_list, name='pet_list'),
    path('logout/', views.logout_view, name='logout'),
    path('adopted_pets/', views.adopted_pets_view, name='adopted_pets'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve_pet/<int:pet_id>/', views.approve_pet, name='approve_pet'),
    path('category', views.category_dashboard, name='category'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('user_details_admin', views.user_details_admin, name= 'user_details_admin'),
    path('doner_details_admin', views.doner_details_admin, name= 'doner_details_admin'),
    path('adoption-details/', views.admin_adoption_details, name='admin_adoption_details'),
    path('individual_donors_pets/<int:donor_id>/', views.donor_donated_pets, name='individual_donors_pets'),

]


