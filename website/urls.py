from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from website.views import ShowAlertMsgById,template2, template3


# router.register('yolo-alert', AlertYoloView)
# router.register('yolo-post', YoloPostView, basename='yolo-post')

urlpatterns = [
    path('', template3),
    path('second_gen', template2, name = 'homepage'),
    path('third_gen', template3, name = 'template_14_12_2021(homepage)'),
    path('detail/<str:id>/', ShowAlertMsgById, name='yolo-info'),
]

