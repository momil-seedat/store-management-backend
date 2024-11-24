from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskSubmission
from .forms import TaskSubmissionForm


def task_submission(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new task submission
            submission = form.save(commit=False)
            submission.task = task
            submission.user = request.user
            submission.save()
         
    else:
        form = TaskSubmissionForm()

    # Query existing task submissions for this task
    task_submissions = TaskSubmission.objects.filter(task=task)

    return render(request, 'mystoreapp/task_submission.html', {'task': task, 'form': form, 'task_submissions': task_submissions})
