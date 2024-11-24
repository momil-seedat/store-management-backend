from rest_framework import serializers
from .models import Store,Task,Notification,Project,StoreContact,TaskSubmission,SubmissionImages,AssignedPermission, City, District,UserAttribute
from django.contrib.auth.models import User, Group

class StoreContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreContact
        fields = ['id', 'name', 'email', 'phone']

class UpdateContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreContact
        fields = ['name', 'email', 'phone']    

class StoreSerializer(serializers.ModelSerializer):
    contacts = StoreContactSerializer(many=True,required=False) 
    class Meta:
        model = Store
        fields = ['id', 'shop_name', 'sales', 'brands', 'address', 'owner_name', 'grade','channel','purchase_data', 'description', 'email', 'contacts','floors','store_area','no_of_rooms']

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts', [])  # Extract contacts data

        # Create the Store object
        store = Store.objects.create(**validated_data)

        # Create StoreContact instances associated with the created Store
        for contact_data in contacts_data:
            StoreContact.objects.create(store=store, **contact_data)

        return store
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        contacts_data = StoreContactSerializer(instance.contacts.all(), many=True).data
        representation['contacts'] = contacts_data
        return representation




class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('did', 'dname')

class CitySerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)
    class Meta:
        model = City
        fields = ('id', 'name', 'districts')
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')   
class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name','last_name','is_active','date_joined','groups']
    def get_groups(self, user):
        group = user.groups.first()  # Fetch the first group associated with the user
        if group:
            return GroupSerializer(group).data
        return None

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','id']    
class StoreObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['shop_name','id']      
class ProjectSerializer(serializers.ModelSerializer):
    store = StoreObjectSerializer()
    created_by =  UserObjectSerializer()
    class Meta:
        model = Project
        fields = ['title','description','store','created_by','project_serial_no','created_at','id','status','end_date']
        
    def validate(self, data):
        # Check if 'store' field exists in the data
        store = data.get('store')

        # Check if 'store' is not provided or is None
        if not store:
            raise serializers.ValidationError("Store is required for the project.")
        
        return data
    
class AddProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project   
        fields = '__all__'

class ProjectObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project   
        fields = ['project_serial_no','id','title']

class SubmissionImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionImages
        fields = ('image','comment')

class TaskSubmissionSerializer(serializers.ModelSerializer):
    images = SubmissionImagesSerializer(many=True, required=False)

    class Meta:
        model = TaskSubmission
        fields = ('length_measurement', 'height_measurement', 'task', 'user', 'images')

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        submission = TaskSubmission.objects.create(**validated_data)
        for image_data in images_data:
            SubmissionImages.objects.create(task_submission=submission, **image_data)
        return submission
    
class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    assignee = UserSerializer()
    task_assigned_to = UserSerializer()
    class Meta:
        model = Task
        fields = ['id', 'name', 'project', 'description', 'assignee','task_assigned_to', 'progress','task_serial_no', 'status', 'start_date', 'end_date','updated_at']

class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskObjectSerializer(serializers.ModelSerializer):
    project = ProjectObjectSerializer()
    assignee = UserObjectSerializer()
    task_assigned_to = UserObjectSerializer()
    class Meta:
        model = Task
        fields = ['id', 'name', 'project', 'description', 'assignee','task_assigned_to', 'progress','task_serial_no', 'status', 'start_date', 'end_date','updated_at']

class AssignedPermissionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    user = UserSerializer()
    assignee = UserSerializer()
    class Meta:
        model = AssignedPermission
        fields = ['user', 'assignee', 'project']

class AddPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignedPermission
        fields = '__all__'


class ImageUploadListSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    images = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(max_length=255)
        )
    )

class TaskSubmissionSerializer(serializers.ModelSerializer):
    task_submissions = SubmissionImagesSerializer(many=True, read_only=True)
    class Meta:
        model = TaskSubmission
        fields = ['submission_date','user','task','submission_feedback','task_submissions','status','id','updated_at']


class UserAttributeSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = UserAttribute
        fields = ['district', 'mobile_no','user_id'  # Add other fields as needed
                  ]

class FetchUserSerializer(serializers.ModelSerializer):
    user_attribute = UserAttributeSerializer(source='userattribute', read_only=True)
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups','user_attribute']
    def get_groups(self, user):
        group = user.groups.first()  # Fetch the first group associated with the user
        if group:
            return GroupSerializer(group).data
        return None
    
class AddSubmissionImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionImages
        fields = ['task_submission', 'image', 'comment']
