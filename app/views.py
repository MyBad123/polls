import datetime
from django.shortcuts import render
from django.views import View

from .models import Poll, Options, OptionUser, UsersOptions
from .serializer import PollSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
@permission_classes([AllowAny])
def for_uauth(request):
    try: 
        u_name = str(request.data.get('username'))
        u_pass = str(request.data.get('password'))
        auth_user = authenticate(username=u_name, password=u_pass)
        my_token = Token.objects.get(user=auth_user)
        
        return Response(data={"data": my_token.key}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_304_NOT_MODIFIED)


class WorkPolls(ViewSet):
    permission_classes = [IsAdminUser]

    def post_poll(self, request):
        try:
            poll = request.data.get('poll')
            serializer = PollSerializer(data=poll)
            poll = None
            if serializer.is_valid(raise_exception=True):
                poll = serializer.save()  
        
            oprions = request.data.get('responses')
            for i in oprions:
                a_a = Options.objects.create(option_poll=poll, option_options=i)
                a_a.save()
            return Response(status=status.HTTP_201_CREATED)   
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put_poll(self, request):
        try:
            poll = Poll.objects.get(id=request.data.get('id'))
            if (datetime.datetime.now().date() > poll.poll_start.date()): 
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if (datetime.datetime.now().date() == poll.poll_start.date()) and (datetime.datetime.now().time() > poll.poll_start.time()):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            data = request.data.get('new')
            serializer = PollSerializer(instance=poll, data=data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete_poll(self, request):
        try:
            a_a = Poll.objects.get(id=request.data.get('id'))
            a_a.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class WorkOptions(ViewSet):
    permission_classes = [IsAdminUser]

    def put_option(self, request):
        poll = Poll.objects.get(id=request.data.get('id'))
        
        if (datetime.datetime.now().date() > poll.poll_start.date()): 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if (datetime.datetime.now().date() == poll.poll_start.date()) and (datetime.datetime.now().time() > poll.poll_start.time()):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        options = Options.objects.filter(option_poll=poll)
        options.delete()
        options_arr = request.data.get('new_options')
        for i in options_arr:
            a_a = Options.objects.create(option_poll=poll, option_options=i)
            a_a.save()
        
        return Response(status=status.HTTP_201_CREATED)
    
    
#second part 

class UserOption(ViewSet):
    permission_classes = [AllowAny]
    '''work witk user s api'''
    def post_option(self, request):
        all_polls = Poll.objects.all()
        arr_id_polls = []
        for i in all_polls:
            if (datetime.datetime.now().date() > i.poll_start.date()) and (datetime.datetime.now().date() < i.poll_finish.date()):
                arr_id_polls.append(i.id) 
            elif ((datetime.datetime.now().date() == i.poll_start.date()) and (datetime.datetime.now().time() > i.poll_start.time())) \
                    and (datetime.datetime.now().date() == i.poll_finish.date()) and (datetime.datetime.now().time() < i.poll_finish.time()):
                arr_id_polls.append(i.id)

        id_user = request.data.get('id')
        users_options = UsersOptions.objects.filter(user_option_user=OptionUser.objects.get(optionuser_id=id_user))
        for i in users_options:
            if i.user_option_options.option_poll.id in arr_id_polls:
                arr_id_polls.remove(i.user_option_options.option_poll.id)

        information_polls = []
        for i in arr_id_polls:
            a_a = Poll.objects.get(id=i)
            a_b = Options.objects.filter(option_poll=a_a)
            arr_option = []
            for j in a_b:
                arr_option.append({"id": j.id, "option": j.option_options})
            information_polls.append({
                "id": a_a.id,
                "poll_name": a_a.poll_name, 
                "poll_desc": a_a.poll_desc, 
                "poll_start": a_a.poll_start, 
                "poll_finish": a_a.poll_finish, 
                "poll_type": a_a.poll_type, 
                "options": arr_option
            })
        return Response(data={"data": information_polls}, status=status.HTTP_200_OK)

    #проголосовать
    def post_users_option(self, request):
        try:
            poll = Poll.objects.get(id=request.data.get('poll_id'))
            
            if (datetime.datetime.now().date() < poll.poll_start.date()) and (datetime.datetime.now().date() > poll.poll_finish.date()):
                return Response(status=status.HTTP_204_NO_CONTENT) 
            elif ((datetime.datetime.now().date() == poll.poll_start.date()) and (datetime.datetime.now().time() < poll.poll_start.time())) \
                    and (datetime.datetime.now().date() == poll.poll_finish.date()) and (datetime.datetime.now().time() > poll.poll_finish.time()):
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            arr_idoptions = request.data.get('options_od') 
            if poll.poll_type == 'one' and len(arr_idoptions) != 1:
                return Response(status=status.HTTP_204_NO_CONTENT)

            id_user = request.data.get('user_id')
            users_options = UsersOptions.objects.filter(user_option_user=OptionUser.objects.get(optionuser_id=id_user))

            for i in users_options:
                if users_options.user_option_options.option_poll == poll:
                    return Response(status=status.HTTP_402_PAYMENT_REQUIRED)

            for i in arr_idoptions:
                a_a = UsersOptions.objects.create(user_option_user=OptionUser.objects.get(optionuser_id=id_user), user_option_options=Options.objects.get(id=i))
                a_a.save()              

            return Response(status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except: 
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #все старыне запросы
    def get_old_polls(self, request):
        try:
            this_user = OptionUser.objects.get(optionuser_id=request.data.get('id'))
            options = UsersOptions.objects.filter(user_option_user=this_user)
            
            #id poll
            polls_arr = []
            #id ответов пользователя
            options_arr = []
            
            for i in options:
                if i.user_option_options.option_poll.id not in polls_arr:
                    polls_arr.append(i.user_option_options.option_poll.id)
                options_arr.append(i.id)

            #все, что мы хотим сохранять и отправить потом пользователю
            all_imformation = []
            for i in polls_arr:
                #ответы к опросу
                arr_options = []
                all_options = Options.objects.filter(option_poll=Poll.objects.get(id=i))
                for j in all_options:
                    arr_options.append({"id": j.id, "option": j.option_options})
                
                #простые id всех ответов на опрос
                id_of_alloptions = []
                for j in arr_options:
                    id_of_alloptions.append(j["id"])

                #пользовательские ответы на вопросы
                all_users_options = []
                for j in options_arr:
                    a_a = UsersOptions.objects.get(id=j)
                    if a_a.user_option_options.id in id_of_alloptions:
                        all_users_options.append({"id": a_a.user_option_options.id, "option": a_a.user_option_options.option_options}) 
                
                poll = Poll.objects.get(id=i)

                all_imformation.append({
                    "poll": {
                        "id": poll.id, 
                        "poll_name": poll.poll_name,
                        "poll_desc": poll.poll_desc,
                        "poll_start": poll.poll_start,
                        "poll_finish": poll.poll_finish,
                        "poll_type": poll.poll_type
                    }, 
                    "options": arr_options, 
                    "users_options": all_users_options
                })

            return Response(
                data={"polls": all_imformation}, 
                status=status.HTTP_200_OK
            )
        except SyntaxError:
            return Response(status=status.HTTP_400_BAD_REQUEST)




        


