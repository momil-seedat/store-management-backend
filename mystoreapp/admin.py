from django.contrib import admin
from .models import City, District

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['did', 'dname', 'city']
    search_fields = ['dname', 'city__name']


# from django.contrib import admin

# # Register your models here.
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User, Store, StoreWorker,Task,TaskSubmission,StoreContact
# from .forms import TaskAdminForm
# from django.urls import reverse
# from django.utils.html import format_html
# from django.db.models import Q

# class StoreUserInline(admin.TabularInline):
#     model = StoreWorker

# class TaskSubmissionInline(admin.TabularInline):
#     model = TaskSubmission

# class CustomUserAdmin(BaseUserAdmin):
#     inlines = [StoreUserInline]

# class StoreContactInline(admin.TabularInline):
#     model = Store.contacts.through
#     extra = 1

# class StoreAdmin(admin.ModelAdmin):
#     inlines = [StoreContactInline]

# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('name', 'assignee', 'progress', 'status', 'start_date', 'end_date', 'view_task_submissions_link')
#     inlines = [TaskSubmissionInline]
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "task_assigned_to"and not request.user.is_superuser:
#             store_worker = StoreWorker.objects.get(user=request.user)
#             user_store_id = store_worker.store_id
#                 # Filter users to show only those with the same store ID as the project manager
#             kwargs["queryset"] = User.objects.filter(storeworker__store_id=user_store_id)
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
#     def get_queryset(self, request):
#         # Customize the queryset to filter tasks assigned to the current user
#         queryset = super().get_queryset(request)
#         if request.user.is_superuser:
#             # Superusers can see all tasks
#             return queryset
#         else:
#             # Regular users can only see tasks assigned to them
#             return queryset.filter(Q(task_assigned_to=request.user) | Q(assignee=request.user))

#     def view_task_submissions_link(self, obj):
#         url = reverse('task_submission', args=[obj.id])  # Adjust the URL name as needed
#         return format_html('<a href="{}">View Task Submissions</a>', url)
#     view_task_submissions_link.short_description = 'Task Submissions'



# class TaskSubmissionAdmin(admin.ModelAdmin):
#     list_display = ('task', 'user', 'submission_date')
#     list_filter = ('task', 'user')
#     search_fields = ('task__name', 'user__username')
#     date_hierarchy = 'submission_date'
#     ordering = ('-submission_date',)


# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(Store, StoreAdmin)
# # Register the Task model with the TaskAdmin class
# # admin.site.register(Task, TaskAdmin)
# # admin.site.register(TaskSubmission, TaskSubmissionAdmin)
# admin.site.register(StoreContact)