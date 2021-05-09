from django.core.mail import send_mail



WELCOME_MAIL = """Welcome {username}, Its's an honor to have you on our team.

Your user account has been created successfully!
If you get in trouble you can always contact us on http://127.0.0.1:8000/home/contact .
    
Happy shopping!
"""

class MailService:


    def welcome_mail(self, email, username):
        send_mail(
            'Redstar Cereal User Acoount Created!',
            WELCOME_MAIL.format(username=username),
            'redstarcereal@gmail.com',
            [email],
            fail_silently=False
        )
