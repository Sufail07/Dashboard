from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50)
    can_view_dashboard = models.BooleanField(default=False)
    can_create_dashboard = models.BooleanField(default=False)
    can_edit_dashboard = models.BooleanField(default=False)
    can_delete_dashboard = models.BooleanField(default=False)
    can_view_record = models.BooleanField(default=False)
    can_create_record = models.BooleanField(default=False)
    can_edit_record = models.BooleanField(default=False)
    can_delete_record = models.BooleanField(default=False)
    can_view_summary = models.BooleanField(default=False)
    can_access_insights = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Role: {self.name}"


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"User: {self.username}"

    
class FinancialRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    record_type = models.CharField(choices=[("income", "Income"), ("expense", "Expense")], max_length=7)
    category = models.CharField(max_length=50, null=True, blank=True)
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Financial record: {self.id}"
    
    class Meta:
        indexes = [
            models.Index(fields=["user", "date"]),
        ]
    
    



    