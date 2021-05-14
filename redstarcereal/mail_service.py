from django.core.mail import send_mail
from django.contrib.auth.models import User



WELCOME_MAIL = """Welcome {username}, Its's an honor to have you on our team.

Your user account has been created successfully!
If you get in trouble you can always contact us on http://127.0.0.1:8000/home/contact .
    
Happy shopping!
"""
ORDER_MAIL = """We recived your order and are now working on shipping it to you as fast as possible!!

Your favorite online cereal shop,
Red Star Cereal!"""


class MailService:


    def welcome_mail(self, email, username):
        send_mail(
            'Redstar Cereal User Acoount Created!',
            WELCOME_MAIL.format(username=username),
            'redstarcereal@gmail.com',
            [email],
            fail_silently=False
        )
    def order_completed(self,id):
        send_mail(
            'Order confirmed!',
            ORDER_MAIL,
            'redstarcereal@gmail.com',
            [User.objects.get(id=id).email]
        )
