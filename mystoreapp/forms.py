from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Store ,Task,TaskSubmission # Replace with your user model

class CustomUserCreationForm(UserCreationForm):
    stores = forms.ModelMultipleChoiceField(
        queryset=Store.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('stores',)
class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = ['task', 'user','length_measurement','height_measurement']