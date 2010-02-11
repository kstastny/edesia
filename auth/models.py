from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    # if True - male, if False - female
    gender = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username

#extend standard User model for simple model authorization
def can_modify(self, model):
    """
     Returns true if the user can modify specified model
    """
    if not hasattr(model, "inserted_by"):
        return False

    if not self.is_authenticated:
        return False

    if model.inserted_by == self:
        return True

    return self.is_superuser
    #return False

User.can_modify = can_modify
