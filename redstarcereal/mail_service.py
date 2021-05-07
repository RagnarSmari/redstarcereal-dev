from django.core.mail import send_mail



WELCOME_MAIL = """Welcome {username}, Its's an honor to have you on our team.

Your user account has been created successfully!
If you get in trouble you can always contact us through this mail or www.redstarcereal.com/conntact .
    
Happy shopping!
"""

class MailService:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def welcome_mail(self):
        send_mail(
            'Redstarcereal.com User Acoount Created!',
            WELCOME_MAIL.format(username=self.username),
            'redstarcereal@gmail.com',
            [self.email],
            fail_silently=False
        )
