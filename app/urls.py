from django.urls import path
from .views import *


urlpatterns = [
    path('new/', for_uauth), 
    path('example/', WorkPolls.as_view({"post": "all_old_polls"})),
    path('poll-post/', WorkPolls.as_view({"post": "post_poll"})),
    path('poll-put/', WorkPolls.as_view({"put": "put_poll"})),
    path('poll-delete/', WorkPolls.as_view({"delete": "delete_poll"})),
    path('options-put/', WorkOptions.as_view({"put": "put_option"})),
    #work with user
    path('post-option/', UserOption.as_view({"post": "post_option"})),
    path('post-useroption/', UserOption.as_view({"post": "post_users_option"})),
    path('old-polls/', UserOption.as_view({"post": "get_old_polls"})),
]

