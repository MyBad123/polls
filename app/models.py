from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    poll_name = models.CharField(max_length=50)
    poll_desc = models.CharField(max_length=250)
    poll_start = models.DateTimeField()
    poll_finish = models.DateTimeField()
    poll_type = models.CharField(max_length=50)

class Options(models.Model):
    option_poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    option_options = models.CharField(max_length=100)

class OptionUser(models.Model):
    optionuser_user = models.ForeignKey(User, on_delete=models.CASCADE)
    optionuser_id = models.IntegerField()


class UsersOptions(models.Model):
    user_option_user = models.ForeignKey('OptionUser', on_delete=models.CASCADE)
    user_option_options = models.ForeignKey('Options', on_delete=models.CASCADE)


