from django.contrib import admin
from django.urls import path
from clubs import views
from .views import edit_announcement



urlpatterns = [
    # Your custom admin routes come before the default Django admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/user-management/', views.user_management, name='user_management'),
    path('admin/user-management/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin/user-management/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin/user-management/create/', views.create_user, name='create_user'),
    path('admin/club-management/', views.club_management, name='club_management'),
    path('admin/announcement-management/', views.announcement_management, name='announcement_management'),
   
    # Django's default admin URLs
    path('admin/', admin.site.urls),

    # Other URLs for your app
    path('', views.index, name='index'),
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/<int:pk>/', views.club_detail, name='club_detail'),
    path('clubs/<int:pk>/add-member/', views.create_member, name='create_member'),
    path('members/<int:member_id>/', views.member_detail, name='member_detail'),
    path('clubs/create/', views.create_club, name='create_club'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('details/<int:id>/', views.details, name='details'),
    path('club/<int:pk>/create-announcement/', views.create_announcement, name='create_announcement'),
    path('announcement/edit/<int:announcement_id>/', edit_announcement, name='edit_announcement'),
]
