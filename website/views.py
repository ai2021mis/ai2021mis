from queue import Empty
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.template.defaulttags import register
from db_api.models import Yolo, Yolo_Files, yolo_trial, JetsonNano
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import date
from json import dumps
from django.core import serializers
#CSV
import csv
#PDF
from django.template.loader import get_template
from xhtml2pdf import pisa
# For profile (username)
from employee.models import employee, generate_password
from employee.forms import ProfileForm, ProfileFormtemplate4
from django.contrib import messages
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models.expressions import F, Value, Func




@register.filter
def return_item(x,y):
    try:
        return x[y]
    except:
        return None


@register.filter
def seraching_image(x,y):
    try:
        image = Yolo_Files.objects.get(pk=y)
        if image.image!='':
            return image.image.path
        else:
            return 'None'
    except:
        return 'None'

@register.filter
def floor_level(x,y):
    try:
        if x>0:
            return str(x) + ' Floor'
        elif x==0:
            return 'Ground Floor'
        else:
            x = x*-1
            return 'B'+str(x)+' Floor'   
    except:
        return "Somethings Error"
    
@login_required(login_url='login')
def template4(request):
    line_channel_id = settings.LINE_CHANNEL_ID
    #profile
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    if request.method == 'POST':
        profile_form = ProfileFormtemplate4(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '資料更新成功')
        else:
            messages.warning(request, '請檢查每個欄位是否都有正確填寫')
    else:
        profile_form = ProfileFormtemplate4(instance=user_profile)
    
    if user_profile.lineid == employee._meta.get_field(field_name='lineid').get_default():
        new_password = user_profile.password

    # yolo database (alerts)
    yolodata = Yolo.objects.order_by('-created_at')[:5] #only most 5 recent alert
    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    tableA =[]
    for x in yolodata:
        tableB = []
        tableB.append(x.created_at.strftime('%Y年 %m月 %d日 (%X)'))
        tableB.append(x.id)
        tableB.append(x.title)
        tableB.append(alert_choice[x.alert])
        if Yolo_Files.objects.filter(pk=x.id).exists():
            objyolofiles = Yolo_Files.objects.get(pk=x.id)
            if objyolofiles.image != '':
                url = str(objyolofiles.image.url)
                tableB.append(url)
            else:
                url = '/static/template4/images/image-not-found.png'
                tableB.append(url)
        tableA.insert(0,tableB)
    datafor_js = dumps(tableA)

    # stil not sure 
    js_serializer = serializers.get_serializer("json")()
    datafor_js1 = js_serializer.serialize(yolodata, ensure_ascii=False)



    return render(request,"template4/index.html", locals())




@login_required
def lineid_change(request):
    new_password = generate_password()
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)
    user_profile.password = new_password
    user_profile.lineid = employee._meta.get_field(field_name='lineid').get_default()
    user_profile.line_username = employee._meta.get_field(field_name='line_username').get_default()
    user_profile.save()

    return redirect('template4')

@login_required
def seemorealert(request):
    #profile #################################
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    if request.method == 'POST':
        profile_form = ProfileFormtemplate4(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '資料更新成功')
        else:
            messages.warning(request, '請檢查每個欄位是否都有正確填寫')
    else:
        profile_form = ProfileFormtemplate4(instance=user_profile)
    
    if user_profile.lineid == employee._meta.get_field(field_name='lineid').get_default():
        new_password = user_profile.password

    # yolo database (alerts) #################################
    yolodata = Yolo.objects.order_by('-created_at') #only most 5 recent alert
    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]

    # Filtering data #################################
    ## Date (created_at in database)
    alertdate_query = request.POST.get('alertdate',None)
    if alertdate_query is not None and alertdate_query!='':
        yolodata = yolodata.filter(created_at__icontains=alertdate_query)
    else:
        alertdate_query='9999-99-99' #cannot pass empty string from url
    ## ID
    alertid_query = request.POST.get('alertid',None)
    if alertid_query is not None and alertid_query!='':
        yolodata = yolodata.filter(id__icontains=alertid_query)
    else:
        alertid_query = 'None' #cannot pass empty string from url
    ## Title
    alerttitle_query = request.POST.get('alerttitle',None)
    if alerttitle_query is not None and alerttitle_query!='':
        yolodata = yolodata.filter(title__icontains=alerttitle_query)
    else:
        alerttitle_query = 'None' #cannot pass empty string from url
    ## Status(alert in database)
    alertstatus_query = request.POST.get('select',None)
    if alertstatus_query is not None and alertstatus_query!='':
        result=0
        for i in range(len(alert_choice)):
            if alertstatus_query == alert_choice[i]:
                result = i
        yolodata = yolodata.filter(alert=result)
    else:
        alertstatus_query = 'None' #cannot pass empty string from url

    # Storing data to table #################################
    tableA =[]
    for x in yolodata:
        tableB = []
        tableB.append(x.created_at.strftime('%Y年 %m月 %d日 (%X)'))
        tableB.append(x.id)
        tableB.append(x.title)
        tableB.append(alert_choice[x.alert])
        if Yolo_Files.objects.filter(pk=x.id).exists():
            objyolofiles = Yolo_Files.objects.get(pk=x.id)
            if objyolofiles.image != '':
                url = str(objyolofiles.image.url)
                tableB.append(url)
            else:
                url = '/static/template4/images/image-not-found.png'
                tableB.append(url)
        tableA.insert(0,tableB)
    datafor_js = dumps(tableA)

    return render(request,"template4/seemorealert.html", locals())

@login_required
def downloadcsv(request,alertdate,alertid,alerttitle,alertstatus):
    # Response #################################
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=alertlist.csv'

    # yolo database (alerts) #################################
    yolodata = Yolo.objects.order_by('-created_at')
    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]

    #Filtering data  #################################
    if alertdate is not None and alertdate!='' and alertdate!='9999-99-99':
        yolodata = yolodata.filter(created_at__icontains=alertdate)
    if alertid is not None and alertid!='' and alertid!='None':
        yolodata = yolodata.filter(id__icontains=alertid)
    if alerttitle is not None and alerttitle!='' and alerttitle!='None':
        yolodata = yolodata.filter(title__contains=alerttitle)
    if alertstatus is not None and alertstatus!='' and alertstatus!='None':
        result=0
        for i in range(len(alert_choice)):
            if alertstatus == alert_choice[i]:
                result = i
        yolodata = yolodata.filter(alert=result)

    # Write csv file #################################
    writer = csv.writer(response)
    writer.writerow(['Date','ID','Title','Status'])
    for x in yolodata:
        writer.writerow([x.created_at.strftime('%Y年 %m月 %d日 (%X)') , x.id , x.title , alert_choice[x.alert]])
    
    return response

@login_required
def downloadpdf(request,alertdate,alertid,alerttitle,alertstatus):
    # yolo database (alerts) #################################
    yolodata = Yolo.objects.order_by('-created_at')
    image_yolofiles = Yolo_Files.objects.all()
    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]

    #Filtering data  #################################
    if alertdate is not None and alertdate!='' and alertdate!='9999-99-99':
        yolodata = yolodata.filter(created_at__icontains=alertdate)
    if alertid is not None and alertid!='' and alertid!='None':
        yolodata = yolodata.filter(id__icontains=alertid)
    if alerttitle is not None and alerttitle!='' and alerttitle!='None':
        yolodata = yolodata.filter(title__contains=alerttitle)
    if alertstatus is not None and alertstatus!='' and alertstatus!='None':
        result=0
        for i in range(len(alert_choice)):
            if alertstatus == alert_choice[i]:
                result = i
        yolodata = yolodata.filter(alert=result)

        
    # PDF part
    template_path = 'template4/downloadpdf.html'
    context = {'yolodata': yolodata,'alert_choice':alert_choice}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Alertlist.pdf"' # if want to desplay
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"' # if only download

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='login')
def cameralist(request):
    #profile #################################
    user = request.user
    username = user.username
    user_profile = employee.objects.get(user=user)

    if request.method == 'POST':
        profile_form = ProfileFormtemplate4(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, '資料更新成功')
        else:
            messages.warning(request, '請檢查每個欄位是否都有正確填寫')
    else:
        profile_form = ProfileFormtemplate4(instance=user_profile)
    
    if user_profile.lineid == employee._meta.get_field(field_name='lineid').get_default():
        new_password = user_profile.password

    #Camera list #################################
    all_object = JetsonNano.objects.all().annotate(my_integer_field=Cast('floor', IntegerField())).order_by('my_integer_field','floor')

    unavailable = all_object.filter(status=1)
    unavailable_total = unavailable.count()
    available = all_object.filter(status=0)
    available_total = available.count()

    return render(request,"template4/cameralist.html", locals())




























###################################
def web1(request):

    database = Yolo.objects.all()
    database_image = Yolo_Files.objects.all()
    alert_choice = [
        '無危險行為',
        '存在危險行為',
        '未知',
        ]
    english_alert_choice = [
        'No dangerous behavior',
        'Dangerous behavior exists',
        'Unknown',
        ]
    data = []
    for a in database:
        body=[]
        body.append(a.id)
        body.append(a.title)
        body.append(english_alert_choice[a.alert])
        body.append(a.description)
        body.append(a.created_at)

        data.append(body)


    return render(request, 'web1.html',locals())
###################################

#   Ini perlu delete 
# bareng sama template1.html
@login_required(login_url='login')
def template1(request):
    user = request.user
    username = user.username
    database = Yolo.objects.all()
    database_image = Yolo_Files.objects.all()
    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    english_alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    data = []
    for a in database:
        body=[]
        body.append(a.id)
        body.append(a.title)
        body.append(english_alert_choice[a.alert])
        body.append(a.created_at)

        data.append(body)

    return render(request,'template1.html',locals())

####################################################################################################################


@login_required(login_url='login')
def template2(request):
    today = date.today()
    user = request.user
    username = user.username
    database = Yolo.objects.all()
    database_image = Yolo_Files.objects.all()

    total_alert = Yolo.objects.all().count()
    no_danger = Yolo.objects.filter(alert=0).count()
    unknown = Yolo.objects.filter(alert=4).count()
    total_dangerous = total_alert - no_danger
    total_danagerous_without_unknown = total_alert - no_danger - unknown

    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    data = []
    statistics = []
    # no_danger = 0
    # dangerous_behaviour = 0
    # unknown = 0
    todays_alert = 0
    this_week_alert = 0
    for a in database:
        body=[]
        body.append(a.id)
        body.append(a.title)
        body.append(alert_choice[a.alert])
        # if a.alert == 0:
        #     no_danger +=1
        # elif a.alert == 4:
        #     unknown += 1
        # else:
        #     dangerous_behaviour +=1
        body.append(a.created_at)
        statistics.append(a.created_at)

        data.append(body)
    # total_alert = len(data)
    # total_dangerous = total_alert - no_danger
    for i in statistics:
        if today.day == i.day:
            todays_alert += 1
            this_week_alert +=1
        elif today.day-7 <=  i.day:
            this_week_alert +=1
        else:
            pass
#############################################
    b=[]
    alert_list=[]
    index = 40
    index_mod = index%10
    for x in range(index):
        a=[]
        a.append("id %s"%x)
        a.append("title %s"%x)
        a.append("alert %s"%x)
        a.append("created_at %s"%x)
        if len(alert_list)==0 and len(b)==index%10:
            alert_list.insert(0,b)
            b=[]
            b.insert(0,a)
            a=[]
        elif len(b)==10:
            alert_list.insert(0,b)
            b=[]
            b.insert(0,a)
            a=[]
        else:
            b.insert(0,a)
            a=[]
    if len(b) > 0:
        alert_list.insert(0,b)
    data = dumps(alert_list)

    
    return render(request,'homepage/index.html',locals())
##########################################################################################################################
@login_required(login_url='login')
def template3(request):

    # For profile
    user = request.user
    username = user.username

    #For Alert data
    yolo_data = Yolo.objects.all()
    total_yolo_data = Yolo.objects.all().count()
    index_mod = total_yolo_data%10
    b=[]
    yolo_alert_list_desktop =[]
    alert_choice = [
        '無危險行為',
        '未正確配戴安全帽',
        '雙掛鉤未使用',
        '偵測到無安全網',
        '未知',
        ]
    for x in yolo_data:
        a=[]
        a.append(x.id)
        a.append(x.title)
        a.append(alert_choice[x.alert])
        a.append(x.created_at.strftime('%Y年 %m月 %d日 (%H:%M)'))

        if len(yolo_alert_list_desktop)==0 and len(b)==index_mod:
            yolo_alert_list_desktop.insert(0,b)
            b=[]
            b.insert(0,a)
            a=[]
        elif len(b)==10:
            yolo_alert_list_desktop.insert(0,b)
            b=[]
            b.insert(0,a)
            a=[]
        else:
            b.insert(0,a)
            a=[]
    if len(b) > 0:
        yolo_alert_list_desktop.insert(0,b)
    if index_mod == 0:
        yolo_alert_list_desktop.pop()
    alert_list_data_for_java = dumps(yolo_alert_list_desktop)
    
    

    ### Buat mobile alert list ###
    # Index diganti jadi jumlah count di model yolo
    a=[]
    alert_list_mobile=[]
    index = 46
    index_mod = index%5
    for x in range(index):
        a.insert(0,"id %s"%x)
        if len(alert_list_mobile)==0 and len(a)==index%5:
            alert_list_mobile.insert(0,a)
            a=[]
        elif len(a)==5:
            alert_list_mobile.insert(0,a)
            a=[]
    if len(a)>0:
        alert_list_mobile.insert(0,a)
        a=[]
    if index_mod == 0:
        alert_list_mobile.pop()


    ### Buat desktop dan alert details ###
    # index diganti jadi jumlah count di model yolo
    # data yang di append diambil dari yolo
    b=[]
    alert_list=[]
    index = 46
    index_mod = index%10
    for x in range(index):
        a=[]
        a.append("id %s"%x)
        a.append("title %s"%x)
        a.append("alert %s"%x)
        a.append("created_at %s"%x)
        if len(alert_list)==0 and len(b)==index%10:
            alert_list.insert(0,b)
            b=[]
            b.insert(0,a)
            a=[]
        elif len(b)==10:
            alert_list.insert(0,b)
            b=[]
            b.insert(0,a)
            a=[]
        else:
            b.insert(0,a)
            a=[]
    if len(b) > 0:
        alert_list.insert(0,b)
    if index_mod==0:
        alert_list.pop()
    #alert_list_data_for_java = dumps(alert_list)

    return render(request, 'template_14_12_2021/index.html',locals())

##########################################################################################################################

#this is for selecting specific objects
@login_required(login_url='login')
def ShowAlertMsgById(request, id='none'):
    website_host = settings.WEB_HOST
    user = request.user
    username = user.username
    if id == 'none':
        output = {'result':'No object Found'}
    elif not Yolo.objects.filter(id = id).exists():
        output = {'result':'No object Found'}
    else:
        obj_yolo = Yolo.objects.get(pk = id)
        #yolo_file.yolo_id.title get parent element from child
        if Yolo_Files.objects.filter(pk=obj_yolo.pk).exists():
            obj_yolofiles = Yolo_Files.objects.get(pk=obj_yolo.pk)
            if obj_yolofiles.image != "":
                url = str(obj_yolofiles.image.url)
            else:
                url = ''
        else:
            obj_yolofiles = ''
            url = ''

        output = {
            'result' : 'Success',
            'obj_yolo' : obj_yolo,
            'obj_yolofiles' : obj_yolofiles,
            'username' : username,
            'img_url' : url,
            }

    return render(request, 'web2.html', output)



