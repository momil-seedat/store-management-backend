from django.db import models
from django.contrib.auth.models import User  # Import the User model if not already imported
from django.utils import timezone
# Store Model
class Store(models.Model):
    shop_name = models.CharField(max_length=255)
    sales=models.CharField(max_length=255,null=True)
    brands=models.TextField(null=True)
    store_area=models.TextField(null=True)
    floors=models.TextField(null=True)
    no_of_rooms=models.TextField(null=True)
    estimated_completion_date=models.TextField(null=True)
    address = models.TextField()
    owner_name = models.CharField(max_length=255)
    purchase_data = models.CharField(max_length=255,null=True)
    grade = models.CharField(max_length=255,null=True)
    channel = models.CharField(max_length=255,null=True)
    description = models.TextField()
    email = models.EmailField()
    installation_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacts = models.ManyToManyField('StoreContact', related_name='storecontacts', blank=True)

    def __str__(self):
        return self.shop_name

class StoreContact(models.Model):
    store= models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store')
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project_serial_no= models.CharField(max_length=20,null=True)
    store= models.ForeignKey(Store, on_delete=models.CASCADE, related_name='project_store',null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    progress= models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=50)
    end_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.title
# Task Model
class Task(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, null=True,related_name='tasks', on_delete=models.CASCADE)
    task_serial_no= models.CharField(max_length=20,null=True)
    description = models.TextField(null=True)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    progress = models.PositiveIntegerField(default=0)
    task_assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned_to')
    status = models.CharField(max_length=50, default='BACKLOG')
    task_feedback = models.TextField(null=True)
    start_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

# Subtask Model
class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    task_feedback = models.TextField()
    field_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class StoreWorker(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} at {self.store.shop_name}"
    
class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height_measurement = models.CharField(max_length=255,null=True)
    length_measurement = models.CharField(max_length=255,null=True)
    submission_feedback = models.TextField(null=True)
    status = models.CharField(max_length=255,null=True)
    
    submission_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission for Task: {self.task.name}, User: {self.user.username}"
    
class SubmissionImages(models.Model):
    task_submission = models.ForeignKey(TaskSubmission, on_delete=models.CASCADE, related_name='task_submissions')
     
    image = models.CharField(max_length=255, blank=True)
    comment = models.TextField(null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f"Submission for Task: {self.task_submissions}"
    
class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class District(models.Model):
    did = models.AutoField(primary_key=True)
    dname = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dname}, {self.city.name}"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    link = models.TextField(null=True)
    view_status = models.BooleanField(default=False)
    type = models.CharField(max_length=255)  # Adjust the max length as needed
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming a ForeignKey to User model
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} Notification for {self.user_id.username}"


# Task model
class AssignedPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_permissions')
    assignee = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='assignee_permissions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Assuming Project model import
    create_datetime = models.DateTimeField(default=timezone.now)
    update_datetime = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.update_datetime = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User ID: {self.user}, Assignee ID: {self.assignee}, Project ID: {self.project}, Created: {self.create_datetime}, Updated: {self.update_datetime}"
    

class UserAttribute(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE,null=True)
    mobile_no = models.CharField(max_length=20)  # Assuming a character field for mobile number

    def __str__(self):
        return f"{self.user.username}'s Attributes"