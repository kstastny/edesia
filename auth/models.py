from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    # if True - male, if False - female
    gender = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    def user_saved(sender, **kwargs):
        """
        Creates and saves new model if the user was created
        """
        print 'user was just saved'

def test(sender, **kwargs):
    print 'in test method'

post_save.connect(UserProfile.user_saved, sender=User)
post_save.connect(test, sender=User)
