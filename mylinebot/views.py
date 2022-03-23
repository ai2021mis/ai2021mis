from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.urls import reverse

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, FlexSendMessage, TemplateSendMessage, CarouselColumn, CarouselTemplate, URIAction, QuickReply, QuickReplyButton, MessageAction

from .models import Manager, AlertNotification
from employee.models import employee
from db_api.models import Yolo

import json
import requests
ACCESS_TOKEN = settings.LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest


        for event in events:
            user_id = event.source.user_id
            headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
            result = requests.get(f'https://api.line.me/v2/bot/profile/{user_id}', headers=headers)
            user_name = json.loads(result.text)['displayName']

            if not Manager.objects.filter(line_id = user_id).exists():
                unit = Manager.objects.create(name=user_name, line_id=user_id)
                unit.save()
                mode = 'no'
            else:
                unit = Manager.objects.get(line_id = user_id)
                mode = unit.state

            if isinstance(event, MessageEvent):
                sent_message = event.message.text
                reply_token = event.reply_token
                # elif sent_message == '@請輸入帳號' and mode=='login':
                #     message = TextSendMessage(text='你已輸入帳號，請輸入密碼:')

                #######Super user login#######
                if sent_message == 'admin activate':
                    try:
                        instance = Manager.objects.get(line_id = user_id)
                        message = TextSendMessage(text=f'登入成功，已添加『{user_name}』為系統管理員')
                    except ObjectDoesNotExist:
                        Manager.objects.create(name=user_name, line_id=user_id)
                        message = TextSendMessage(text=f'已添加『{user_name}』為系統管理員')

                    unit.state = 'logged in'
                    unit.save()
                    mode = unit.state

                ######normal user login######

                if mode == 'no':
                    if sent_message == '@管理員登入':
                        flex_message = login_flex_message()
                        message = FlexSendMessage(alt_text='@點此登入系統', contents=flex_message)

                    elif sent_message == '@控制台':
                        flex_message = website_flex_message()
                        message = FlexSendMessage(alt_text='@點此登入網頁控制台', contents=flex_message)

                    elif sent_message[:1] == '@' and len(sent_message) > 8:
                        username = 'none'
                        password = 'none'
                        try:
                            flist = sent_message[1:].split("@")
                            username = str(flist[0])
                            password = str(flist[1])
                        except Exception:
                            message = TextSendMessage(text='格式錯誤、請重新輸入\n『格式：@你的賬戶@你的密碼』')

                        if username != 'none' and password != 'none':
                            if not employee.objects.filter(gongHao = username).exists():
                                message = TextSendMessage(text='無此帳號！')

                            else:
                                user = employee.objects.get(gongHao = username)
                                if password != user.password:
                                    message = TextSendMessage(text='密碼錯誤')

                                elif password == user.password and user.lineid == 'no':
                                    user.lineid = user_id
                                    user.line_username = user_name
                                    user.save()
                                    message = TextSendMessage(text=f'登入成功，已添加『{user_name}』為系統管理員')

                                    # unit = Manager.objects.get(line_id = user_id)
                                    unit.state = 'logged in'
                                    unit.save()

                                elif password == user.password and user.lineid == user_id:
                                    message = TextSendMessage(text='登入成功')
                                    unit.state = 'logged in'
                                    unit.save()

                                elif password == user.password and user.lineid != user_id:
                                    message = TextSendMessage(text=f'帳戶『{username}；次此帳戶已有人註冊成為管理員，請聯繫系統管理員')
                        # else:
                        #     message = TextSendMessage(text='請重新輸入')

                    else:
                        message = TextSendMessage(text='請先登入系統～')

                #############################################################
                # funtions after user logged in
                elif mode != 'no' and sent_message =='@管理員登入':
                    message = TextSendMessage(text=f'『{user_name}』已經是系統管理員')

                elif sent_message == '@控制台':
                    flex_message = website_flex_message()
                    message = FlexSendMessage(alt_text='@點此登入網頁控制台', contents=flex_message)

                elif sent_message == '@查看':
                    try:
                        line_bot_api.push_message(user_id, TextSendMessage(text='好的請稍候~'))
                        send_alert_list = SendAlertList()
                        ram_orders = Yolo.objects.all().order_by('-created_at', )
                        all_alert_instances = [order for order in ram_orders if order.alert != "0"]
                        total_alerts = len(all_alert_instances)
                        # total_alerts = Yolo.objects.all().filter(alert='1').count()
                        if total_alerts > 10:
                            instances = all_alert_instances[:9]
                            # instances = Yolo.objects.all().filter(alert='1').order_by('-created_at', )[:9]
                            more_than_10 = True
                        else:
                            instances = all_alert_instances
                            # instances = Yolo.objects.all().filter(alert='1').order_by('-created_at', )
                            more_than_10 = False
                        carousel_columns = send_alert_list.create_message(instances=instances, more_than_10=more_than_10)
                        line_bot_api.push_message(user_id, TemplateSendMessage(alt_text="@查看", template=CarouselTemplate(columns=carousel_columns)))
                        text = f'總共 {total_alerts}個警報'
                        message = TextSendMessage(text=text)

                    except Exception as e:
                        message = TextSendMessage(text=f'{user_name} something wrong')
                        print(e)

                elif sent_message == '@管理員登出':
                    try:
                        instance = Manager.objects.get(line_id = user_id)
                        instance.delete()
                        # delete_user = employee.objects.get(lineid = user_id)
                        # delete_user.lineid = 'no'
                        # delete_user.save()
                        message = TextSendMessage(text=f'管理員『{user_name}』，已被移除')

                    except ObjectDoesNotExist:
                        message = TextSendMessage(text = f'『{user_name}』不是管理員')

                elif "解除警報" in sent_message:
                    action, alert_id, notification_id = '(none)', '(none)', '(none)'
                    try:
                        flist = sent_message.split("@")
                        action = str(flist[0])
                        alert_id = str(flist[1])
                        notification_id = str(flist[2])

                    except Exception:
                        message = TextSendMessage(text='解除警報格式錯誤，請聯繫管理員')

                    try:
                        if notification_id != '(none)' and alert_id != '(none)':
                            alert = AlertNotification.objects.get(pk=notification_id)
                            alert.received = True
                            alert.timestamp = timezone.now()
                            alert.save()
                            message = TextSendMessage(text=f'已解除警報『{alert_id}』')
                    except Exception:
                        message = TextSendMessage(text='解除警報失敗，請聯繫管理員')

                elif sent_message == '@常用聯繫人':
                    if employee.objects.filter(lineid=user_id).exists():
                        user = employee.objects.get(lineid=user_id)
                        user_emergency_contact_list = user.emergency_contact
                        if user_emergency_contact_list != "":
                            user_emergency_contact_list = user_emergency_contact_list.split("&")
                            emergency_contact = EmengencyConatct()
                            flex_message_2 = emergency_contact.create_contact_list(user_emergency_contact_list)
                            line_bot_api.push_message(user_id, FlexSendMessage(alt_text='常用聯繫人', contents=flex_message_2))
                            message = TextSendMessage(text="點擊按鈕，即可撥打~")
                        else:
                            flex_message = website_flex_message()
                            flex_message_2 = FlexSendMessage(alt_text='@點此登入網頁控制台', contents=flex_message)
                            message = TextSendMessage(text="無設定聯絡人資料，可上網登記聯繫人資料")
                            line_bot_api.push_message(user_id, flex_message_2)

                elif sent_message == '@其它':
                    quick_reply = OtherFuncQuickReply()
                    message = TextSendMessage(text='請選擇功能：', quick_reply=quick_reply.return_quick_reply())

                elif sent_message == 'admin activate':
                    pass
                else:
                    message = TextSendMessage(text=sent_message)

                line_bot_api.reply_message(reply_token, message)

        return HttpResponse()

    else:
        HttpResponseBadRequest()


def login_flex_message():
    website_host = settings.WEB_HOST
    url = website_host + reverse('user_login_line')
    message ={
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "點此登入",
                      "uri": url
                    },
                    "style": "primary",
                    "margin": "sm"
                  },
                  {
                    "type": "text",
                    "text": "1） 點擊上方的按鈕，登入你的賬戶",
                    "margin": "xl",
                    "size": "md",
                    "weight": "bold",
                    "style": "italic",
                    "align": "start",
                    "gravity": "center",
                    "wrap": True
                  },
                  {
                    "type": "text",
                    "text": "2）登入成功後將獲得『鑰匙』",
                    "margin": "xs",
                    "size": "md",
                    "weight": "bold",
                    "style": "italic",
                    "align": "start",
                    "gravity": "center",
                    "wrap": True
                  },
                  {
                    "type": "text",
                    "text": "3）點擊發送，即可啟動機器人",
                    "margin": "xs",
                    "size": "md",
                    "weight": "bold",
                    "style": "italic",
                    "align": "start",
                    "gravity": "center",
                    "wrap": True
                  }
                ]
              }
            }
    return message


def website_flex_message():
    website_host = settings.WEB_HOST
    url = website_host + reverse('home')
    message ={
              "type": "bubble",
              "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "網頁控制台",
                      "uri": url
                    },
                    "style": "primary",
                    "margin": "sm"
                  }
                ]
              }
            }
    return message


class SendAlertList:
    def __generate_carousel_column(self, alert_id='(none)', timestamp='(none)', descrption='(none)'):
        website_host = settings.WEB_HOST
        if alert_id != '(none)':
            yolo_info_url = website_host + "/website/detail/" + alert_id + "/"
        else:
            yolo_info_url = website_host + reverse('seemorealert')

        CarouselColumn_message = CarouselColumn(
            thumbnail_image_url='https://cdn.pixabay.com/photo/2012/04/12/22/25/warning-sign-30915__340.png',
            title=f'ID: {alert_id}',
            text=f'時間: {timestamp}\n警報內容: {descrption}',
            actions=[
                URIAction(
                    label='查看',
                    uri=yolo_info_url
                ),
            ]
        )
        return CarouselColumn_message


    def __generate_carousel_column_more(self):
        website_host = settings.WEB_HOST
        website = website_host + reverse('seemorealert')

        CarouselColumn_message = CarouselColumn(
            thumbnail_image_url='https://cdn.pixabay.com/photo/2012/04/12/22/25/warning-sign-30915__340.png',
            title='其他',
            text='其他',
            actions=[
                URIAction(
                    label='其他',
                    uri=website
                ),
            ]
        )
        return CarouselColumn_message

    def create_message(self, instances, more_than_10):
        columns = []
        for instance in instances:
            instance_id = str(instance)
            instance_timestamp = str(instance.timestamp)
            instance_description = str(instance.description)
            carousel_column_object = self.__generate_carousel_column(instance_id, instance_timestamp, instance_description)
            columns.append(carousel_column_object)
        if more_than_10:
            carousel_column_object = self.__generate_carousel_column_more()
            columns.append(carousel_column_object)

        return columns


class EmengencyConatct():
    def __create_button(self, name, contact_num):
        button = {
                    "type": "button",
                    "style": "secondary",
                    "action": {
                        "type": "uri",
                        "label": f"{name}  {contact_num}",
                        "uri": f"tel:{contact_num}"
                    },
                    "margin": "md"
                }
        return button

    def create_contact_list(self, instances):
        contents = []
        contents.append({
                        "type": "text",
                        "text": "常用聯繫人",
                        "weight": "bold",
                        "size": "xl",
                        "align": "center"
                    })
        for instance in instances:
            flist = instance.split("@")
            name = str(flist[0])
            contact_num = str(flist[1])
            button = self.__create_button(name, contact_num)
            # button = self.__create_button('chris', '0933')
            contents.append(button)
        message = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": contents
                        }
                }

        return message


class OtherFuncQuickReply():
    def return_quick_reply(self):
        quick_reply = QuickReply(
            items = [
                QuickReplyButton(
                    action=MessageAction(label="老師登入", text="admin activate")
                ),
                QuickReplyButton(
                    action=MessageAction(label="老師登入2", text="admin activate")
                ),
            ]
        )

        return quick_reply
