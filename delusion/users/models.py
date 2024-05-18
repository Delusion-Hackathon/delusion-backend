from django.db import models
from django.contrib.auth.models import AbstractUser

from delusion.users.choices import CompanySize, CorporateProfession, country_names


class User(AbstractUser):
    # TODO: add default profile picture
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True
    )
    msp_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class CompanyRegistration(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    corporate_name = models.CharField(max_length=100)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)

    vat_id = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    company_size = models.CharField(
        max_length=20, choices=CompanySize.choices
    )
    corporate_profession = models.CharField(
        max_length=30, choices=CorporateProfession.choices
    )

    approved = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.corporate_name


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def create_countries(cls):
        for name in country_names:
            country = cls(name=name)
            country.save()

class MeshUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='mesh_user'
    )
    mesh_username = models.CharField(max_length=100)
    mesh_password = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    # TODO: save ovewrite save method for register mesh central

    def save(self, *args, **kwargs):
        if not self.pk:
            ...
        # TODO: register mesh central
        super().save(*args, **kwargs)
