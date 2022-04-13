from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#######################################################
import random
import string

def generate_password():
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(10)))
    return result_str


def generate_temp_id():
    source = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(source) for i in range(5)))
    return result_str


class Company(models.Model):
    name = models.CharField(max_length = 50, null=True, blank=True)
    name2 = models.CharField(max_length = 50, null=True, blank=True)

    def __str__(self):
        return self.name

        class Meta:
            db_table = "Company"



class employee(models.Model):
    gongHao = models.CharField(max_length=50, primary_key = True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True, blank=True, default='(No name)')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=2)
    email = models.CharField(max_length=100, null=True, blank=True)
    lineid = models.CharField(max_length=150, null=False, blank=True, default='no')
    line_username = models.CharField(max_length=150, null=False, blank=True, default='no')
    alert_service = models.BooleanField(default=False)
    continuous_alert = models.BooleanField(default=False)
    contact_num = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=50, null=False, blank=True, default=generate_password())
    emergency_contact = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.name

    class Meta:
        db_table = "employee"


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         # emp = employee.objects.create(user=instance, password=generate_password())
#         employee.objects.create(gongHao='1234', password=generate_password())


