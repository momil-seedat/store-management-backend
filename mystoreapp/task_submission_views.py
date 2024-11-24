from rest_framework import generics
from .models import TaskSubmission
from .serializers import TaskSubmissionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskSubmissionSerializer

@api_view(['POST'])
def create_task_submission(request):
    serializer = TaskSubmissionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class TaskSubmissionCreateListView(generics.ListCreateAPIView):
    queryset = TaskSubmission.objects.all()
    serializer_class = TaskSubmissionSerializer

class TaskSubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskSubmission.objects.all()
    serializer_class = TaskSubmissionSerializer
