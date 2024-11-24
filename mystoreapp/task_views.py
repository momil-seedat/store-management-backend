from rest_framework import generics, status

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from .models import Task
from .serializers import TaskSerializer, AddTaskSerializer,TaskObjectSerializer
from .models import Project, Notification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from .signals import generate_task_serial_number
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

class TaskCreateListView(generics.ListCreateAPIView):
    queryset = Task.objects.all().order_by('-updated_at')
    serializer_class = AddTaskSerializer

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')  # Assuming project ID is sent in the request data
        project_serial = None

        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                project_serial = project.project_serial_no
            except Project.DoesNotExist:
                pass

        task_serial = None
        if project_serial:
            task_serial = generate_task_serial_number(project_serial)

        task=serializer.save(task_serial_no=task_serial)
        notification_text = f"A new task has been created: {task.name}"
        notification_link = f"/task-mangement/task_profile/{task.id}"  # Change this to the appropriate link for your task details
        Notification.objects.create(text=notification_text, link=notification_link, user_id=task.task_assigned_to,type="Task Added")

    def get_serializer_class(self):
        # Use different serializer for list view
        if self.request.method == 'GET':
            return TaskObjectSerializer  # Change ListProjectSerializer to your actual serializer class
        else:
            return AddTaskSerializer    

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AddTaskSerializer
        return TaskSerializer

    def perform_update(self, serializer):
        task = self.get_object()
        assignee_id = self.request.data.get('assignee')
        task_assigned_to_id = self.request.data.get('task_assigned_to')
        project_id = self.request.data.get('project')  # Assuming project ID is sent in the request data

        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                task.project = project
            except Project.DoesNotExist:
                raise ValidationError({'project': 'Project does not exist'})

        if assignee_id:
            try:
                assignee = User.objects.get(id=assignee_id)
                task.assignee = assignee
            except User.DoesNotExist:
                raise ValidationError({'assignee': 'User does not exist'})

        if task_assigned_to_id:
            try:
                task_assigned_to = User.objects.get(id=task_assigned_to_id)
                task.task_assigned_to = task_assigned_to
            except User.DoesNotExist:
                raise ValidationError({'task_assigned_to': 'User does not exist'})

        task = serializer.save()
        notification_text = f"A task has been updated: {task.name}"
        notification_link = f"/task-management/task_profile/{task.id}"  # Corrected link
        Notification.objects.create(
            text=notification_text,
            link=notification_link,
            user_id=task_assigned_to,
            type="Task Updated"
        )
@csrf_exempt
def fetch_tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        assignee_id = data.get('assignee')
        assigned_to_id = data.get('assigned_to')
        project_id = data.get('project_id')

        user_id = None
        filter_param = None

        if assignee_id:
            user_id = assignee_id
            filter_param = 'assignee'
        elif project_id:
            tasks = Task.objects.filter(project_id=project_id).order_by('-updated_at')
        elif assigned_to_id:
            user_id = assigned_to_id
            filter_param = 'task_assigned_to'

        if filter_param:
            user = User.objects.filter(id=user_id).first()
            if user:
                tasks = Task.objects.filter(**{filter_param: user}).order_by('-updated_at')
            else:
                return JsonResponse({'error': 'User not found'}, status=404)

        tasks_data = []
        for task in tasks:
            project_serial_no = task.project.project_serial_no if task.project else None
            assigned_by = task.project.created_by.username if task.project else None
            project_title = task.project.title if task.project else None
            tasks_data.append({
                'id': task.id,
                'name':task.name,
                'status': task.status,
                'task_serial': task.task_serial_no,
                'project_serial_no': project_serial_no,
                'project_title':project_title,
                'assigned_to': task.task_assigned_to.username,
                'assignee': task.assignee.username,
                'created_at': task.start_date.strftime('%d-%m-%Y'),
                'updated_at': task.updated_at,
                 'end_date': "---" if task.end_date is None else task.end_date.strftime('%d-%m-%Y')

            })

        return JsonResponse({'tasks': tasks_data}, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def update_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task does not exist"}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        new_status = data.get('status')
        new_feedback = data.get('task_feedback')
        
        if new_status:
            task.status = new_status
        if new_feedback:
            task.task_feedback = new_feedback
        if new_status == 'APPROVED':
            task.end_date = timezone.now()


      
        task.save()

        #update progress of project
        project_id = task.project_id

        # Get total count of tasks for the project
        total_tasks = Task.objects.filter(project_id=project_id).count()

        # Get count of approved tasks for the project
        approved_tasks = Task.objects.filter(project_id=project_id, status='approved').count()

        # Calculate the average approval rate
        if total_tasks > 0:
            approval_rate = approved_tasks / total_tasks * 100
        project = Project.objects.get(id=project_id)
        project.progress = approval_rate
        project.save()
        # Create a notification for the assigned user
        notification_text = f"Task {task_id} status/feedback updated: {task.status} - {task.task_feedback}"
        Notification.objects.create(
            text=notification_text,
            type="Task Update",
            user_id=task.task_assigned_to,
        )

        serializer = TaskSerializer(task)
        response_data = {
            "message": "Task status and feedback updated successfully",
            "code":"000"
           
        }

        return JsonResponse(response_data, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def get_filter_param(user):
    if user.groups.filter(name='WORKER').exists():
        return 'task_assigned_to'
    elif user.groups.filter(name='PROJECT MANAGER').exists():
        return 'assignee'
    elif user.groups.filter(name='ADMIN').exists():
        return 'admin'
    return None

@csrf_exempt
def fetch_filtered_tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Extract filter parameters from the request data
        task_serial_no = data.get('task_serial_no')
        project_serial_no = data.get('project_serial_no')
        status = data.get('status')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        user_id = data.get('user_id')
        print(status)
        # Initialize queryset with all tasks
        tasks = Task.objects.all()

        # Apply filters based on provided parameters
        if user_id:
            user = User.objects.filter(id=user_id).first()
            if user:
                filter_param = get_filter_param(user)
                if filter_param != "admin":
                    tasks = Task.objects.filter(**{filter_param: user}).order_by('-updated_at')

  
        if task_serial_no:
            tasks = tasks.filter(task_serial_no__icontains=task_serial_no)
        if project_serial_no:
            tasks = tasks.filter(project__project_serial_no__icontains=project_serial_no)
        if status:
            if isinstance(status, list):  # Check if status is a list
                tasks = tasks.filter(status__in=status)
            else:
                tasks = tasks.filter(status=status)
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            tasks = tasks.filter(start_date__gte=start_date)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            tasks = tasks.filter(start_date__lte=end_date)

        # Serialize filtered tasks
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                 'name':task.name,
                'status': task.status,
                'task_serial': task.task_serial_no,
                'project_serial_no': task.project.project_serial_no if task.project else None,
                'project_title':task.project.title if task.project else None,
                'assigned_to': task.task_assigned_to.username,
                'assignee': task.assignee.username,
                'created_at': task.start_date.strftime('%d-%m-%Y'),
                'updated_at': task.updated_at,
                'end_date': task.end_date
            })

        return JsonResponse({'tasks': tasks_data}, safe=False)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@api_view(['PATCH'])
def change_task_status(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')
    if new_status not in ['COMPLETED', 'ON_HOLD','DISCARD']:
        return JsonResponse({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    task.status = new_status
    if new_status == 'COMPLETED':
        task.end_date = timezone.now()
    else:
        task.end_date = None

    task.save()
    serializer = TaskSerializer(task)
    return JsonResponse(serializer.data)



@api_view(['GET'])
def search_tasks(request):
    query = request.GET.get('query', '')

    if not query:
        return JsonResponse({'error': 'No Search Results found'}, status=status.HTTP_404_NOT_FOUND)

    # Perform the search using Trigram Similarity
    tasks = Task.objects.annotate(
        task_similarity=TrigramSimilarity('name', query),
        project_similarity=TrigramSimilarity('project__title', query)
    ).filter(
        Q(task_similarity__gt=0.3) | Q(project_similarity__gt=0.3)
    ).order_by('-task_similarity', '-project_similarity')

    # Prepare the task data
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'name': task.name,
            'status': task.status,
            'task_serial': task.task_serial_no,
            'project_serial_no': task.project.project_serial_no if task.project else None,
            'project_title': task.project.title if task.project else None,
            'assigned_to': task.task_assigned_to.username if task.task_assigned_to else None,
            'assignee': task.assignee.username if task.assignee else None,
            'created_at': task.start_date.strftime('%d-%m-%Y') if task.start_date else None,
            'updated_at':  task.updated_at,
            'end_date': task.end_date.strftime('%d-%m-%Y') if task.end_date else None,
        })

    # Return the response after processing all tasks
    if tasks_data:
        return JsonResponse({'tasks': tasks_data}, safe=False)
    else:
        return JsonResponse({'error': 'No Search Results found'}, status=status.HTTP_404_NOT_FOUND)
    # serializer = TaskSerializer(tasks, many=True)
    # return JsonResponse(serializer.data, safe=False)
