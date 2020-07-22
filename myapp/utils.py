from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


def OtpFun(user_obj):
    html_string=render_to_string('mails/otp_mails.html',{'user':user_obj})      #render_to_string render the given url with user_obj
    subject="My project welcome"
    plain_message=strip_tags(html_string)           #strip_tag remove html tag like<html>,</html>,<body>,</body> etc... and send email with text part only
    from_mail='parmarkomal147@gmail.com'
    send_mail(subject,plain_message,from_mail,[user_obj.EmailId],html_message=html_string)      #send email to user given email address
