from django.shortcuts import render, redirect, get_object_or_404
from .models import Task 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.models import User



class Taskcreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_form.html'
    fields = ['title', 'description', 'complete', 'due_date']
    success_url = reverse_lazy('tasks_lists')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user

        task.save()
        return super().form_valid(form)



class User_SignupView(View):
    def get(self, request):
        return render(request, 'user_signup.html')

    def post(self, request):
        if request.method == 'POST':
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            Username = request.POST.get('Username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password = request.POST.get('password')
            Gender = request.POST.get('Gender')
            Terms = request.POST.get('Terms')


            #create a new user
            new_user = User.objects.create_user(username=Username, first_name=firstName, last_name=lastName, email=email, 
            password=password)
            new_user.save()
            return redirect ('user_login')
            

        else:
            #render the signup form template
            return render(request, 'signup.html')
        

class user_login(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True 

    def get_success_url(self):
        return reverse_lazy('tasks_lists')



class Tasks_lists(ListView):
    model = Task
    template_name = 'tasks_lists.html'
    context_object_name = 'tasks'


    def tasks_lists(request):
            logout_url = reverse('logout')
            context = {'logout_url': logout_url}

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks.html'

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_update.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks_lists')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class task_delete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks_lists')


class TaskReminderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'], user=request.user)
        time_difference = task.due_date - timezone.now()
        minutes_before_due = int(time_difference.total_seconds() / 60)

        if minutes_before_due <= 10:
            subject = f'Reminder: {task.title}'
            message = f'Dear {request.user.username},\n\nThis is a reminder for the task "{task.title}" which is due in 10 minutes.'

            send_mail(
                subject,
                message,
                'weeleegad@gmail.com',  
                [request.user.email],
                fail_silently=False,
            )

        return super().get(request, *args, **kwargs)
