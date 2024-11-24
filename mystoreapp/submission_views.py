from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TaskSubmission, SubmissionImages, Task, Notification, Project
from .serializers import ImageUploadListSerializer , TaskSubmissionSerializer ,AddSubmissionImagesSerializer
from datetime import datetime
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import os
import json
from django.http import HttpResponse,HttpResponseNotFound
from django.http import FileResponse
from django.utils import timezone


class ImageUploadListAPIView(APIView):
    def post(self, request):
        try:
            # Assuming 'image' is the key representing the file data in the request.FILES dictionary
            uploaded_file = request.FILES.get('image')

            # Save image to the filesystem with a unique name based on current datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_name = f"image_{timestamp}.jpg"  # Change the extension based on your requirement

            # Write the file to the filesystem
            with open(f"d:/fiverr/images/{image_name}", 'wb') as file:
                for chunk in uploaded_file.chunks():
                    file.write(chunk)

            return Response({"image_name": image_name}, status=201)

        except Exception as e:
            # Handle exceptions or errors here as needed
            print(f"Error while uploading: {e}")
            return Response({"message": "Error while uploading image"}, status=500)
        
class DeleteImageAPIView(APIView):
    def delete(self, request, image_name):
        try:
            # Specify the directory path where images are stored
            directory_path = "d:/fiverr/images/"  # Replace with your image directory path

            # Construct the full path of the image
            image_path = os.path.join(directory_path, image_name)

            # Check if the file exists
            if os.path.exists(image_path):
                # Delete the file
                os.remove(image_path)
                return Response({"message": f"Image {image_name} deleted successfully"}, status=200)
            else:
                return Response({"message": "Image does not exist"}, status=404)

        except Exception as e:
            # Handle exceptions or errors here as needed
            print(f"Error while deleting: {e}")
            return Response({"message": "Error while deleting image"}, status=500)
        
@api_view(['POST'])
def submit_task_api(request):
    if request.method == 'POST':
        data = request.data

        # Extracting data from the request payload
        images_data = data.get('images', [])
        comment = data.get('comment', None)
        task_id = data.get('task_id', None)
        user_id = data.get('user_id', None)  # Include 'user_id' in the request payload

        # Validating the data
        if not all([comment, task_id, user_id, isinstance(images_data, list)]):
            return Response({'error': 'Invalid data format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Fetching the user using the provided user_id
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        task.status = 'SUBMITTED'
        task.save()

        # Creating TaskSubmission with the provided user and other data
        submission = TaskSubmission.objects.create(
            task=task,
            user=user,  # Use the fetched user
            status='SUBMITTED'
        )

        # Creating SubmissionImages associated with the submission
        for image_data in images_data:
            SubmissionImages.objects.create(
                task_submission=submission,
                image=image_data.get('image', ''),
                comment=image_data.get('comment', None)
            )

        return Response({'message': 'Task submitted successfully.'}, status=status.HTTP_201_CREATED)

    return Response({'error': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_submission_details(request, submission_id):
    try:
        submission = TaskSubmission.objects.get(pk=submission_id)
    except TaskSubmission.DoesNotExist:
        return Response({'error': 'Submission does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    images_comments = SubmissionImages.objects.filter(task_submission=submission).values('image', 'comment')
    submission_data = {
        'submission': list(images_comments),
        'status': submission.status,
        'submission_feedback': submission.submission_feedback
    }

    return Response(submission_data, status=status.HTTP_200_OK)

def get_image(request, image_name):
    images_directory = "d:/fiverr/images/"
    image_path = os.path.join(images_directory, image_name)

    if os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as image_file:
                return HttpResponse(image_file, content_type='image/jpeg')  # Adjust content_type as per your image type
        except Exception as e:
            return HttpResponseNotFound(f"Error reading the file: {str(e)}")
    else:
        return HttpResponseNotFound("Image not found.")
    


@api_view(['GET'])
def task_submissions_by_task_id(request, task_id):
    try:
        task_submissions = TaskSubmission.objects.filter(task_id=task_id).order_by('-updated_at')
        serializer = TaskSubmissionSerializer(task_submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except TaskSubmission.DoesNotExist:
        return Response({'error': 'Task submissions not found.'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def update_submission(request, submission_id):
    try:
        taskSubmission = TaskSubmission.objects.get(pk=submission_id)
    except TaskSubmission.DoesNotExist:
        return JsonResponse({"error": "Task does not exist"}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        new_status = data.get('status')
        new_feedback = data.get('feedback')
        task_status = data.get("task_status")
        
        if new_status:
            taskSubmission.status = new_status
        if new_feedback:
            taskSubmission.submission_feedback = new_feedback
                
        task = Task.objects.get(pk=taskSubmission.task_id)
        if new_status == 'DECLINED':
            approved_submissions = TaskSubmission.objects.filter(task_id=taskSubmission.task_id, status='APPROVED').exists()
            if approved_submissions:
                task.status = 'APPROVED'
            else:
                task.status = 'REJECTED'
        elif task_status == 'COMPLETED':
            task.status = 'COMPLETED'
            task.task_feedback = new_feedback
            task.end_date = timezone.now()

        task.save()
        taskSubmission.save()
        

        #update progress of project
        project_id = task.project_id

        # Get total count of tasks for the project
        total_tasks = Task.objects.filter(project_id=project_id).count()
        print(total_tasks)
        # Get count of approved tasks for the project
        approved_tasks = Task.objects.filter(project_id=project_id, status='COMPLETED').count()
        print(approved_tasks)
        # Calculate the average approval rate
        if total_tasks > 0:
            approval_rate = approved_tasks / total_tasks * 100
        project = Project.objects.get(id=project_id)
        project.progress = approval_rate
        project.save()

        # Create a notification for the assigned user
        notification_text = f"Task {taskSubmission.task_id} status/feedback updated: {task.status} - {task.task_feedback}"
        Notification.objects.create(
            text=notification_text,
            type="Task Update",
            user_id=task.task_assigned_to,
            link=f"/task-submission/view-submission/{taskSubmission.task_id}"
        )

        
        response_data = {
            "message": "Task status and feedback updated successfully",
            "code":"000"
           
        }

        return JsonResponse(response_data, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)
@csrf_exempt
def update_submission_image(request):
    if request.method == 'PATCH':
        data = json.loads(request.body.decode('utf-8'))
        image_name = data.get('image_name', None)
        task_submission_id = data.get('task_submission_id', None)
        updated_image=data.get('updated_image',None)
        if not image_name or not task_submission_id:
            return JsonResponse({'error': 'Both image_name and task_submission_id are required.'}, status=400)

        try:
            submission = SubmissionImages.objects.get(image=image_name, task_submission_id=task_submission_id)
        except SubmissionImages.DoesNotExist:
            return JsonResponse({'error': 'Submission not found.'}, status=404)

        # Update the image field
        submission.image = updated_image  # Assuming image_name is the new image filename
        submission.save()

        taskSubmission = TaskSubmission.objects.get(pk=task_submission_id)
        taskSubmission.status='UPDATED_SUBMISSION'
        task = Task.objects.get(pk=taskSubmission.task_id)
        task.status = 'SUBMITTED'
        task.save()
        taskSubmission.save()

        return JsonResponse({'message': 'Submission image updated successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
