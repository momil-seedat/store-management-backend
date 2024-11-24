from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from .serializers import AssignedPermissionSerializer,AddPermissionsSerializer,UserSerializer
from .models import AssignedPermission, Project
import json
from rest_framework.decorators import api_view
from django.db import transaction
from datetime import datetime
class AssignedPermissionListView(generics.ListCreateAPIView):
    queryset = AssignedPermission.objects.all()
    serializer_class = AddPermissionsSerializer

class AssignedPermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AssignedPermission.objects.all()
    serializer_class = AssignedPermission


class UsersByProjectAPIView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']  # Assuming project_id is passed in URL
        return User.objects.filter(assigned_permissions__project_id=project_id)


@csrf_exempt
def fetch_assigned_projects(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')

        if user_id:
            user = User.objects.filter(id=user_id).first()
            if user:
              
                assigned_permissions = AssignedPermission.objects.filter(user_id=user)
                assigned_projects = [permission.project_id for permission in assigned_permissions]
                projects = Project.objects.filter( Q(id__in=assigned_projects) | Q(created_by=user)).order_by('-updated_at')

        # Sorting by created_at (ascending order)
                
                project_serial_no = data.get('project_serial_no')
                start_date = data.get('start_date')
                end_date = data.get('end_date')
                status = data.get('status')
                if project_serial_no:
                    projects = projects.filter(project_serial_no__icontains=project_serial_no)
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                    projects = projects.filter(created_at__gte=start_date)
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d')
                    projects = projects.filter(created_at__lte=end_date)

                if status:
                    projects = projects.filter(status__icontains=status)


                projects_data = []
                for project in projects:
                    projects_data.append({
                        'project_id': project.id,
                        'title': project.title,
                        'description': project.description,
                        'project_serial_no': project.project_serial_no,
                        'created_at':  project.created_at.strftime('%d-%m-%Y'),
                        'store':project.store.shop_name,
                        'progress':project.progress,
                        'created_by': project.created_by.username,
                        'status': project.status,
                       'end_date': "---" if project.end_date is None else project.end_date.strftime('%d-%m-%Y')

                        
                        


                        # Include other project details as needed
                    })
                return JsonResponse({'assigned_projects': projects_data}, safe=False)
            else:
                  return JsonResponse({'error': 'Invalid user'}, status=400)
            
        else:
            return JsonResponse({'error': 'Parameter user_id is required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



@api_view(['POST'])
def assign_permission(request):
    if request.method == 'POST':
        project_id = request.data.get('project_id')
        assignee_id = request.data.get('assignee_id')
        users = request.data.get('users')

        if not project_id:
            return JsonResponse({'error': 'Project ID is required'}, status=400)
        
        if not assignee_id:
            return JsonResponse({'error': 'Assignee ID is required'}, status=400)
        if not users:
            return JsonResponse({'error': 'Users list is required'}, status=400)

        try:
            with transaction.atomic():
                # Delete entries for users not in the new list
                AssignedPermission.objects.filter(project_id=project_id).exclude(user_id__in=[user['id'] for user in users]).delete()

                # Update or create AssignedPermission objects
                for user in users:
                    assigned_permission, created = AssignedPermission.objects.update_or_create(
                        project_id=project_id,
                        user_id=user['id'],
                        defaults={'assignee_id': assignee_id}
                    )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'message': 'Permissions assigned successfully'}, status=201)
