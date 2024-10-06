from django.core.mail import send_mail
from django.utils.crypto import get_random_string

send_mail(
            'Registration Confirmation',
            f'Your account has been created. Your password is {123}.',
            'petdonation0@gmail.com',
            ['jikkujames34@gmail.com'],
            fail_silently=False,
        )

send_mail()