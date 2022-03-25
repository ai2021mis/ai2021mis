from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from website.views import ShowAlertMsgById ,template2, template3, ShowAlertMsgById, template4,lineid_change,seemorealert,downloadcsv,downloadpdf, cameralist


# router.register('yolo-alert', AlertYoloView)
# router.register('yolo-post', YoloPostView, basename='yolo-post')

urlpatterns = [
    # Latest version
    path('', template4, name='home'),
    path('forth_gen', template4, name="template4"),
    path('lineid_change', lineid_change , name='lineid_change'),
    path('seemorealert', seemorealert ,name='seemorealert'),
    path('camera_list/', cameralist, name='camera_list'),
    url(r'^downloadcsv/(?P<alertdate>\d{4}-\d{2}-\d{2})/(?P<alertid>\w+)/(?P<alerttitle>\w+)/(?P<alertstatus>\w+)/$',downloadcsv,name='downloadcsv'),
    url(r'^downloadpdf/(?P<alertdate>\d{4}-\d{2}-\d{2})/(?P<alertid>\w+)/(?P<alerttitle>\w+)/(?P<alertstatus>\w+)/$',downloadpdf,name='downloadpdf'),

    ######
    path('second_gen', template2, name = 'homepage'),
    path('third_gen', template3, name = 'template_14_12_2021(homepage)'),
    path('detail/<str:id>/', ShowAlertMsgById, name='yolo-info'),

]

