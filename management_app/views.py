from .models import Project
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from .email import send_task_email

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Your Projects"
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        if project.user != request.user:
            messages.error(request, "You are not authorized to view this project.")
            return redirect('project-list')
        return super().get(request, *args, **kwargs)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Project created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating project. Please check the form.")
        return super().form_invalid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_update.html'
    context_object_name = 'project'
    success_url = reverse_lazy('project-list')

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.user != request.user:
            messages.error(request, "You are not authorized to update this project.")
            return redirect('project-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Project updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating project. Please check the form.")
        return super().form_invalid(form)


class ProjectDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        project = get_object_or_404(Project, pk=pk)
        if project.user != request.user:
            messages.error(request, "You are not authorized to delete this project.")
            return redirect('project-list')
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect('project-list')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user) | Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Your Tasks"
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user and task.assigned_to != request.user:
            messages.error(request, "You are not authorized to view this task.")
            return redirect('task-list')
        return super().get(request, *args, **kwargs)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        # Set the user field to the logged-in user
        form.instance.user = self.request.user
        task = form.save()

        subject = f"New Task Assigned: {task.title}"
        message = (
            f"Dear {task.assigned_to.username},\n\n"
            f"You have been assigned a new task:\n\n"
            f"Title: {task.title}\n"
            f"Description: {task.description}\n"
            f"Due Date: {task.due_date}\n"
            f"Status: {task.status}\n"
            f"Priority: {task.priority}\n"
            f"Project: {task.project.title}\n\n"
            f"Thank you!"
        )

        try:
            send_task_email(subject, message, task.assigned_to.email)
        except Exception as e:
            messages.error(self.request, f"Error Sending email {str(e)}.")
        messages.success(self.request, "Task created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error creating task. Please check the form.")
        return super().form_invalid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user and task.assigned_to != request.user:
            messages.error(request, "You are not authorized to update this task.")
            return redirect('task-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        task = form.save()
        subject = f"Your Task Updated: {task.title}"
        message = (
            f"Dear {task.assigned_to.username},\n\n"
            f"Your task has been updated:\n\n"
            f"Title: {task.title}\n"
            f"Description: {task.description}\n"
            f"Due Date: {task.due_date}\n"
            f"Status: {task.status}\n"
            f"Priority: {task.priority}\n"
            f"Project: {task.project.title}\n\n"
            f"Thank you!"
        )

        try:
            send_task_email(subject, message, task.assigned_to.email)
        except Exception as e:
            messages.error(self.request, f"Error Sending email {str(e)}.")
        messages.success(self.request, "Task updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error updating task. Please check the form.")
        return super().form_invalid(form)


class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        if task.user != request.user:
            messages.error(request, "You are not authorized to delete this task.")
            return redirect('task-list')
        task.delete()
        messages.success(request, "Task deleted successfully.")
        return redirect('task-list')
