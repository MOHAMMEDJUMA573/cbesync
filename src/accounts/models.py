from django.db import models, connection
from django.contrib.auth.models import AbstractUser
import uuid

#funtion to check table existence
def table_exists(table_name):
    return table_name in connection.introspection.table_names()

#function to generate user is
def generate_unique_user_id():
    new_id = uuid.uuid4()
    table_name = "accounts_CustomUser"
    if table_exists(table_name):
        while CustomUser.objects.filter(user_id=new_id).exists():
            new_id = uuid.uuid4()
    return new_id

#custom users table for scalability
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ("school", "School"),
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("parent", "Parent"),
        ("ntstaff", "NtStaff"),
        ("sysadmin", "SysAdmin"),
    )
    #the fields of abstract model
    user_id = models.UUIDField(default=generate_unique_user_id,editable=False, unique=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='school',help_text="user_type field for allauth modularity")
