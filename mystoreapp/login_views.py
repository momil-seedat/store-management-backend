from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
@csrf_exempt  # You can use csrf_exempt for testing, but it's not recommended in production.
@authentication_classes([TokenAuthentication])
@permission_classes([AllowAny])
def custom_login(request):
   
    if request.method == 'POST':
        # Retrieve username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Authentication successful, log in the user
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            user_groups = user.groups.all()
            
            # Retrieve user's permissions
            user_permissions = []
            for group in user_groups:
                group_permissions = group.permissions.all()
                user_permissions.extend(group_permissions)

            # Prepare data to include in the JSON response
            response_data = {
                'message': 'Authentication successful',
                'user_group': [group.name for group in user_groups],
                'user_permissions': [permission.codename for permission in user_permissions],
                'token': token.key,
                'userId': user.id,
                'userName':user.username
            }
            
            return JsonResponse(response_data)

        else:
            # Authentication failed, return an error response
            return JsonResponse({'message': 'Authentication failed'}, status=401)
    else:
        # Handle other HTTP methods (GET, etc.) if needed
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
@csrf_exempt 
@api_view(['POST'])
def custom_logout(request):
    # Handle logout
    token = Token.objects.get(user=request.user)

    # Delete the token
    token.delete()

    return JsonResponse({'message': 'Logged out successfully'})
