# views.py

from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from .models import UserAttribute
from .serializers import UserSerializer, GroupSerializer, UserCreationSerializer
from django.contrib.auth.hashers import make_password
from .models import UserAttribute
from .serializers import UserSerializer, FetchUserSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class UsersByGroupView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        group_name = self.kwargs['group_name']  # Get the group name from the URL parameter
        return User.objects.filter(groups__name=group_name, is_active=True)

class AllUsersView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)
    
class GroupViews(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CreateUserWithAttributes(APIView):
    def post(self, request, format=None):
        user_data = request.data.copy() 
        user_id = user_data.get('userId')

# Check if userId is provided in the request data
        if user_id:
    # Update existing user
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                # Handle the case where the user with the provided ID does not exist
                # You might want to return an error response or handle it according to your needs
                pass
            else:
            # Update user data without modifying the password
                if 'password' in user_data:
                    password = request.data.get('password')
                    hashed_password = make_password(password)
                    user_data['password'] = hashed_password                    

                user_serializer = UserCreationSerializer(instance=user, data=user_data, partial=True)
                if user_serializer.is_valid():
                    user_serializer.save()

                    # Additional logic for updating groups, district, mobile_no, etc.
                    group_id = user_data.get('user_group')
                    if group_id:
                        group = Group.objects.get(pk=group_id)
                        user.groups.clear()
                        user.groups.add(group)

                        district_id = user_data.get('district')
                        mobile_no = user_data.get('mobile_no')

                        UserAttribute.objects.update_or_create(user=user, defaults={'district_id': district_id, 'mobile_no': mobile_no})
                    return Response("user updated successfully", status=status.HTTP_200_OK)
        else: 
            password = request.data.get('password')
            hashed_password = make_password(password)
            user_data['password'] = hashed_password
            user_serializer = UserCreationSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()

                group_id = request.data.get('user_group')
                if group_id:
                    group = Group.objects.get(pk=group_id)
                    
                    user.groups.add(group)

                district_id = request.data.get('district')
                mobile_no = request.data.get('mobile_no')

                UserAttribute.objects.create(user=user, district_id=district_id, mobile_no=mobile_no)

                return Response(user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def get_user_info_view(request, user_id):
    user = User.objects.get(pk=user_id)
    serializer = FetchUserSerializer(user)
    return JsonResponse(serializer.data)