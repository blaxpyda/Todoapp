from django.urls import path
from django.contrib.auth import views as auth_views
from .views import User_SignupView, user_login, Tasks_lists, Taskcreate, TaskDetail, TaskUpdate, task_delete, TaskReminderView
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('user_login/',user_login.as_view(), name= 'user_login'),

    path('logout/',LogoutView.as_view(), name= 'logout'),

    path('tasks_lists/', Tasks_lists.as_view(), name='tasks_lists'),

    path('Taskcreate/',Taskcreate.as_view(), name='Taskcreate'),

    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),

    path('task-delete/<int:pk>/', task_delete.as_view(), name='task_delete'),

    path('',User_SignupView.as_view(), name='user_signup'),

    path('task/<int:pk>/reminder/', TaskReminderView.as_view(), name='task-reminder'),

   

]