from django import forms
from .models import Project, Task
from django.forms import DateInput


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'team_members']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'status', 'project', 'assigned_to', 'dependencies']

        dependencies = forms.ModelMultipleChoiceField(
            queryset=Task.objects.all(),
            required=False,
            widget=forms.CheckboxSelectMultiple
        )
        widgets = {
            'due_date': DateInput(attrs={'type': 'date'}),
        }