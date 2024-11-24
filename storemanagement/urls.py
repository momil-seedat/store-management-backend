"""
URL configuration for storemanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home/api/tasks/
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mystoreapp.store_views import StoreCreateListView,StoreWithContactsView,StoreContactListCreateView, StoreContactUpdateView
from mystoreapp.store_views import StoreDetailView
from mystoreapp.notification_views import NotificationListCreateView
from mystoreapp.project_views import  ProjectListCreateView,change_project_status, ProjectDetailView,projects_by_created_by,projects_by_store
from mystoreapp.user_views import  UsersByGroupView, AllUsersView, CreateUserWithAttributes, GroupViews,get_user_info_view
from mystoreapp.task_views import  TaskCreateListView,change_task_status,TaskDetailView, fetch_tasks, update_task ,fetch_filtered_tasks,search_tasks
from mystoreapp.task_submission_views import create_task_submission, TaskSubmissionCreateListView,TaskSubmissionDetailView
from mystoreapp.assigned_permission_views import AssignedPermissionListView,assign_permission,fetch_assigned_projects,UsersByProjectAPIView
from mystoreapp.submission_views import ImageUploadListAPIView, DeleteImageAPIView,task_submissions_by_task_id, submit_task_api,get_submission_details,get_image,update_submission,update_submission_image
from mystoreapp import login_views
from mystoreapp.region_views import CityListCreateAPIView , DistrictsByCityAPIView
from django.urls import path, include


urlpatterns = [
    #diyari daar mazdoor hacked your code
    path('admin/', admin.site.urls),
    path('api/store/', StoreCreateListView.as_view(), name='store-create'),
    path('api/store/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
    path('api/tasks/', TaskCreateListView.as_view(), name='task-create'),
    path('api/task/<int:pk>/', TaskCreateListView.as_view(), name='task-create'),
    
    path('store/<int:id>/', StoreWithContactsView.as_view(), name='store-list-with-contacts'),
    path('store/<int:store_id>/contacts/', StoreContactListCreateView.as_view(), name='store-contacts-list-create'),
    path('store/<int:store_id>/contacts/update/', StoreContactUpdateView.as_view(), name='store-contacts-update'),

    #  path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('api/notifications/user/<int:user_id>/', NotificationListCreateView().as_view(), name='user-notification-list'),
    
    path('api/projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('api/projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/change-status/', change_project_status, name='change-project-status'),

    path('api/tasksubmission/', TaskSubmissionCreateListView.as_view(), name='task-submission-create'),
    path('api/tasksubmission/<int:pk>/', TaskSubmissionDetailView.as_view(), name='task-submission-detail'),
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/change-status/', change_task_status, name='change-task-status'),
  path('api/search-tasks/', search_tasks, name='search-tasks'),
    path('accounts/login/', login_views.custom_login, name='custom_login'),
    path('accounts/logout/', login_views.custom_logout, name='logout'),
    path('users/group/<str:group_name>/', UsersByGroupView.as_view(), name='users-by-group'),
    path('users/', AllUsersView.as_view(), name='all-users'),
    path('api/user/', CreateUserWithAttributes.as_view()),
     path('api/user/<int:user_id>/', get_user_info_view, name='get_user_info'),
     path('api/auth/group', GroupViews.as_view()),
    path('task-submission/create/', create_task_submission, name='task-submission-create'),
     path('submission/<int:submission_id>/', update_submission, name='update_submission'),
      path('users/by-project/<int:project_id>/', UsersByProjectAPIView.as_view(), name='users-by-project'),
     


    path('projects/user/', projects_by_created_by, name='projects_by_created_by'),
    path('tasks/user/', fetch_tasks, name='fetch_tasks'),
     path('filtertasks/user/', fetch_filtered_tasks, name='fetch_filtered_tasks'),
    path('api/assign/permission/', AssignedPermissionListView.as_view(), name='assign-permission-create'),
    path('assign/permission', fetch_assigned_projects, name='fetch_assigned_projects'),
     path('api/projects/store/<int:store_id>/', projects_by_store, name='projects_by_store'),
 path('api/submission/',ImageUploadListAPIView.as_view(), name='submission'),
 path('delete_image/<str:image_name>/', DeleteImageAPIView.as_view(), name='delete_image'),
  path('submit_task/', submit_task_api, name='submit_task'),
   path('submission_details/<int:submission_id>/', get_submission_details, name='submission_details'),
    path('images/<str:image_name>/', get_image, name='get_image'),
    path('task_submissions/<int:task_id>/', task_submissions_by_task_id, name='task_submissions_by_task_id'),
    path('cities/', CityListCreateAPIView.as_view(), name='city-list-create'),
     path('cities/<int:city_id>/districts/', DistrictsByCityAPIView.as_view(), name='districts-by-city'),
     path('assign_permission/', assign_permission, name='assign_permission'),

      path('submission/update/',update_submission_image, name='submission-images-detail'),

]
