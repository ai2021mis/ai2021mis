from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
######################################################
from mylinebot.alert import send_alert_to_managers as line_sendAlert
from mylinebot.alert import send_alert_img_to_managers as line_sendAlert_picture
######################################################
from PIL import Image
from employee.models import employee
# Create your models here.

#so that there is no object with the same slug
def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(id=unique_slug).exists():
        unique_slug = slug + get_random_string(length=3)
    return unique_slug



class yolo_trial(models.Model):
    alert_choice = (
        (0, '無危險行為'),
        (1, '存在危險行為'),
        (2, '未知'),
        )


    # A slug is a string without special characters, in lowercase letters and with dashes instead of spaces
    id = models.SlugField(unique=True, max_length=50, blank=True, primary_key=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    alert = models.IntegerField(default = 0,choices=alert_choice)
    description = models.CharField(max_length=200, default='(none)')
    image = models.ImageField(upload_to='Uploaded Files/',default='',blank=True)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)


########## store the json file from the AI #################
class Yolo(models.Model):
    alert_choice = (
        (0, '無危險行為'),
        (1, '未正確配戴安全帽'),
        (2, '雙掛鉤未使用'),
        (3, '偵測到無安全網'),
        (4, '未知')
        )


    # A slug is a string without special characters, in lowercase letters and with dashes instead of spaces
    id = models.SlugField(unique=True, max_length=50, blank=True, primary_key=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    alert = models.IntegerField(default = 0,choices=alert_choice)
    description = models.CharField(max_length=200, default='(none)')
    timestamp = models.CharField(max_length=50, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    image_shape = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(editable=True, default = timezone.now)


    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = unique_slugify(self, slugify(self.title.rsplit('.', 1)[0]))
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Yolo"


class Yolo_Files(models.Model):
    id = models.SlugField(unique=True, max_length=50, blank=True, primary_key=True)
    yolo_id = models.ForeignKey(Yolo, on_delete=models.CASCADE,max_length=50,default="")
    #file = models.FileField(blank=True, upload_to='Uploaded Files/')
    image = models.ImageField(upload_to='Uploaded Files/',default='',blank=True)
    send_alert = models.BooleanField(default =False)
    memo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(editable=True, default = timezone.now)


    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = unique_slugify(self, slugify(self.yolo_id))
        super().save(*args, **kwargs)

        # save the resize image
        if self.image != '':
            pict = Image.open(self.image)
            pict_size = (1150,647) # we follow the size pict of 'not found pict' size
            pict = pict.resize(pict_size, Image.ANTIALIAS)
            pict.save(self.image.path)

    class Meta:
        db_table = "Yolo_Files"
#########################################################

class Alert_Data(models.Model):

    id = models.IntegerField(primary_key = True)
    body = models.CharField(max_length=50, null=True, blank=True)

    # def __str__(self):
    #     return self.body


class Picture_Files(models.Model):
    # identifier = models.ForeignKey(Yolo, on_delete=models.CASCADE,max_length=50,default="")
    identifier = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='Uploaded Files/',default='',blank=True)
    memo = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.identifier


#function to send email
@receiver(post_save, sender=Yolo)
def kirim_email(sender, instance, created, **kwargs):
    alert_choice = {
        '0': '無危險行為',
        '1': '未正確配戴安全帽',
        '2': '雙掛鉤未使用',
        '3': '偵測到無安全網',
        '4': '未知'
    }


    if created:
        subject = "Alert From Security System"
        try:
            default = 'this is an alert from YOLO'
            default_title = 'detected : '
            default_time = 'alert time: '
            x = alert_choice[str(instance.alert)]
            body1 = str(x)
            body2 = str(instance.created_at)
            default_url = "click this url to check"
            body_url = settings.WEB_HOST

            message = default + '\n' + default_title + body1 + '\n' + default_time + body2 +'\n'+'\n'+ default_url + '\n'+ body_url
        except:
            with open("/home/tam/gen_3/ai2021mis/db_api/message.txt", "r") as f:
                message = f.read()

        receiver_list = []
        employee_set = employee.objects.all()
        for i in employee_set:
            receiver = i.email
            receiver_list.append(receiver)
        send_mail(subject, message, settings.RECIPIENT_ADDRESS,receiver_list )
        # send_mail(subject, message, settings.RECIPIENT_ADDRESS, ['wiratamawidarto@gmail.com'])


##currently not using this func
##### function tp give email and line notif to the manager######
def email_sendAlert(alert):
    subject = "Alert From Security System"
    #with open("/home/christopher0908/ai2021mis/db_api/message.txt", "r") as f:
    #    body = f.read()

    try:
        total_email= Alert_Data.objects.count()
        data = Alert_Data.objects.get(id = total_email )
        #data = Alert_Data.objects.first()
        body = str(data)

    except:
        with open("/home/tam/gen_3/ai2021mis/db_api/message.txt", "r") as f:
            body = f.read()


    alert = alert
    message = body + '@' + alert
    send_mail(subject, message, settings.RECIPIENT_ADDRESS, [settings.RECIPIENT_ADDRESS])


@receiver(post_save, sender=Yolo)
def create_alert(sender, instance, created, **kwargs):
    def decode_img():
        from .decode_img import append_task_queue
        append_task_queue(instance)

    if created and instance.alert:
        Yolo_Files.objects.create(id = instance.id, yolo_id = instance, )
        # email_sendAlert('YOLO')
        line_sendAlert(instance)
        if instance.image != '':
            decode_img()
    elif created:
        if instance.image != '':
            decode_img()
    else:
        pass


@receiver(post_save, sender=Picture_Files)
def create_file(sender, instance, created, **kwargs):
    try:
        if created:
            target_yolo = Yolo.objects.get(title = instance.identifier)
            target = Yolo_Files.objects.get(yolo_id = target_yolo)
            target.image = instance.picture
            target.save()
    except Exception as e:
        instance.memo = e
        instance.save()

        # cannot directly match the pic, becozz picture file is cannot be the same
        # pic_data = instance.picture
        # file = Yolo_Files.objects.get(image = pic_data)
        # file.image = instance.picture #update
        # file.save()


@receiver(post_save, sender=Yolo_Files)
def send_picture(sender, instance, created, **kwargs):
    website_host = settings.WEB_HOST
    try:
        if created == False and instance.send_alert == False and instance.image.url != '':
            line_sendAlert_picture(instance)
            instance.send_alert = True
            instance.save()

    except Exception as e:
        instance.memo = e
        instance.save()


class JetsonNano(models.Model):
    status_choice = (
        (0, 'connected'),
        (1, 'disconnect'),
        (2, 'unknown')
    )

    # A slug is a string without special characters, in lowercase letters and with dashes instead of spaces
    id = models.SlugField(unique=True, max_length=50, blank=True, primary_key=True)
    ip = models.CharField(max_length=50, null=True, blank=True)
    status = models.IntegerField(default=2, choices=status_choice)
    timestamp = models.TextField(null=True, blank=True)
    #floor = models.CharField(max_length=50,null=True,blank=True)
    floor = models.IntegerField(default=0, unique=True, help_text="Each camera assign for one floor -- '0' means groundfloor -- '-1..' is basement") # change to integer field
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='JetsonNano/', default='', blank=True)
    created_at = models.DateTimeField(editable=True, default=timezone.now)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = unique_slugify(self, str(self.ip).replace('.', ''))
        super().save(*args, **kwargs)

        # save the resize image
        if self.image != '':
            pict = Image.open(self.image)
            pict_size = (1150,647) # we follow the size pict of 'not found pict' size
            pict = pict.resize(pict_size, Image.ANTIALIAS)
            pict.save(self.image.path)



    class Meta:
        db_table = "JetsonNano"
