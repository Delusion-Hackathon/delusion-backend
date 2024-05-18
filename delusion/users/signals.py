import random
import string
from decouple import config

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from delusion.users.models import User, CompanyRegistration, MeshUser
from delusion.services import WebSocketClient
from .models import CompanyRegistration, MeshUser
from ..company.services.company_services import create_company


def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@receiver(post_save, sender=CompanyRegistration)
def create_mesh_user(sender, instance, created, **kwargs):
    if instance.approved:
        username = f"{instance.name.lower()}_{instance.surname.lower()}_{''.join(random.choices(string.ascii_letters + string.digits, k=6))}"
        password = generate_random_password()

        mesh_password = generate_random_password()

        user = User.objects.create_user(
            username=username,
            password=password,
            email=instance.email,
            first_name=instance.name,
            last_name=instance.surname
        )

        mesh_user = MeshUser.objects.create(user=user, mesh_username=username, mesh_password=mesh_password)
        print(mesh_user.mesh_username, mesh_user.mesh_password)
        mesh_service = WebSocketClient(username=config('MESH_USERNAME'), password=config('MESH_PASSWORD'))
        mesh_service.connect()
        mesh_service.create_new_user(email=instance.email, username=username, password=mesh_password)
        print(mesh_service.last_message)
        mesh_service.close()

        # Need to change from_email
        send_mail(
            subject="delusion Hesap Bilgileri",
            message=f"Hello {instance.name} {instance.surname},\n\ndelusion account was created for you.\n\nUsername: {username}\nPassword: {mesh_password}\n\nYou can login to delusion with these credentials.\n\nBest regards,\ndelusion Team",
            from_email="awd@gmail.com",
            recipient_list=[instance.email],
            fail_silently=False
        )
        create_company(user=user, mesh_username=mesh_user.mesh_username, mesh_password=mesh_user.mesh_password, name=instance.corporate_name, description='Example description.')



# from delusion.services import WebSocketClient

# wss = WebSocketClient(username="kazimovzaman2", password="8wbm2v7W")
# wss.connect()
# wss.create_new_user(email="indi@mail.ru", username="indi", password="indi")