from django.contrib import admin

# Register your models here.


from .models import Contact, Category, Task, Subtask
from user_auth_app.models import UserProfile

# Register your models here.

admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Subtask)
admin.site.register(UserProfile)
