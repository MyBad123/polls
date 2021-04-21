from .models import Poll, Options, OptionUser, UsersOptions
from django.contrib import admin

admin.site.register(Poll)
admin.site.register(Options)
admin.site.register(OptionUser)
admin.site.register(UsersOptions)