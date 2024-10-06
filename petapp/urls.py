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
    path('user_self_profile', views.user_self_profile, name='user_self_profile'),
    path('user_edit_profile/<int:user_id>', views.user_edit_profile,name='user_edit_profile'),
    path('user_change_pass',views.user_change_password,name='user_change_pass'),
    path('user_self_delete_/<int:pk>', views.user_self_delete, name='user_self_delete'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve_pet/<int:pet_id>/', views.approve_pet, name='approve_pet'),
    path('reject_pet/<int:pet_id>/', views.reject_pet, name='reject_pet'),
    path('category', views.category_dashboard, name='category'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('admin_self_profile', views.admin_self_profile, name = 'admin_self_profile'),
    path('profile_edit_admin',views.admin_edit_profile, name = 'profile_edit_admin'),
    path('user_details_admin', views.user_details_admin, name= 'user_details_admin'),
    path('doner_details_admin', views.doner_details_admin, name= 'doner_details_admin'),
    path('admin_edit_pet_page/<int:pk>',views.admin_edit_pet_page,name='admin_edit_pet_page'),
    path('admin_pet_edit/<int:pk>',views.admin_edit_pet, name='admin_pet_edit'),
    path('adoption-details/', views.admin_adoption_details, name='admin_adoption_details'),
    path('individual_donors_pets/<int:donor_id>/', views.donor_donated_pets, name='individual_donors_pets'),
    path('user_edit_admin/<int:user_id>',views.admin_edit_user, name = 'user_edit_admin'),
    path('admin_change_password',views.admin_change_password,name='admin_change_password'),
    #path('doner_edit_admin/<int:pk>',views.admin_edit_donar, name = 'doner_edit_admin'),
    path('user_delete_admin/<int:pk>', views.user_delete, name='user_delete_admin'),
    path('doner_delete_admin/<int:pk>', views.doner_delete, name='doner_delete_admin'),
    path('doner_home',views.doner_home,name='doner_home'),
    path('edit_category/<int:pk>', views.edit_category_page, name='edit_category'),
    path('edit_category', views.edit_category, name='edit_category'),
    path('doner_self_profile', views.donor_self_profile, name='doner_self_profile'),
    path('doner_edit_profile/<int:user_id>', views.doner_edit_profile,name='doner_edit_profile'),
    path('donar_self_delete_/<int:pk>', views.donar_self_delete, name='donar_self_delete'),
    path('add_pet_page', views.add_pet_page, name='add_pet_page'),
    path('add_pet',views.add_pet,name='add_pet'),
    path('edit_pet_page/<int:pk>',views.edit_pet_page,name='edit_pet_page'),
    path('pet_edit/<int:pk>',views.edit_pet, name='pet_edit'),
    path('pet_del_doner/<int:pk>', views.pet_del_doner, name='pet_del_doner'),
    path('doner_change_password',views.doner_change_password,name='doner_change_password'),
    path('notification/read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),


]


