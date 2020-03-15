from django.db import models


class Employees(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=255, unique=True)
    data_status = models.BooleanField(default=False)
    department = models.CharField(max_length=255, null=True)
    post = models.CharField(max_length=255, blank=True)
    active_status = models.BooleanField(default=True)
    joined_at = models.DateTimeField(blank=True, auto_now_add=True)


class Attendance(models.Model):
    user_id = models.ForeignKey(Employees, on_delete=models.CASCADE, null=False)
    entry_date = models.DateField(null=True)
    entry_time = models.TimeField(null=True)
    exit_date = models.DateField(null=True)
    exit_time = models.TimeField(null=True)


