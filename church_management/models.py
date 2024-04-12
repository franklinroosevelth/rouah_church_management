from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError(_("The username must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given username and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)

class Commune(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

class Adresse(models.Model):
    commune = models.OneToOneField(Commune, null=True, blank=True)
    quartier = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    avenue = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    
class Profession(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

class Categorie(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES =(
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=50, default='client')
    username = models.CharField(_("username"), unique=True, max_length=50)
    name = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.ForeignKey(Adresse, null=True, blank=True)
    profession = models.ManyToManyField(Profession, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now) 

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
      verbose_name = "user"

    def __str__(self):
        return f"{self.username}"

class ProgrammeHabituel(models.Model):
    jour = models.CharField(max_length=100, null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    heure_fin = models.TimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    
class Communique(models.Model):
    titre = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    
class Publication(models.Model):
    type_choices = (("predication", "Prédication"), ("post", "Post"))
    type = models.CharField(choices=type_choices, max_length=100, null=True, blank=True)
    auteur = models.OneToOneField(CustomUser, null=True, blank=True)
    theme = models.CharField(max_length=100, null=True, blank=True)
    description_courte = models.TextField(null=True, blank=True)
    description_longue = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True, upload_to='predication_images/')
    video = models.FileField(null=True, blank=True, upload_to='predication_videos/')
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    
class Commentaire(models.Model):
    nom_complet = models.CharField(max_length=100, null=True, blank=True)
    auteur = models.OneToOneField(CustomUser, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

class LieuEvenement(models.Model):
    appelation = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.ForeignKey(Adresse, null=True, blank=True)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

class CrenauxHoraire(models.Model):
    jour = models.DateField(null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    heure_fin = models.TimeField(null=True, blank=True)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

class Actvite(models.Model):
    categorie = models.ManyToManyField(Categorie, blank=True)
    lieu = models.ManyToManyField(LieuEvenement, blank=True)
    crenaux_horaire = models.ManyToManyField(CrenauxHoraire, blank=True)
    titre = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    

    

    
    
    
    

