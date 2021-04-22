# App's documentation

> deploying an application
>> docker build . 
>> docker run --rm -d --publish 8000:8000 [Hash]

#API

> http://127.0.0.1:8000/api/new/
>> method: POST 
>> body: {"username": "", "password": ""}

> http://127.0.0.1:8000/api/poll-post/
>> method: POST 
>> users: admin
>> authorization: Authorization: "Token [token]"
>> body: {"poll": {"poll_name": "",
>> "poll_desc": "", "poll_start": "", "poll_finish": "",
>> "poll_type": ""}, "responses": [] }

> http://127.0.0.1:8000/api/poll-put/
>> method: PUT 
>> users: admin
>> authorization: Authorization: "Token [token]"
>> body: {"new": {"poll_name": "",
>> "poll_desc": "", "poll_start": "", "poll_finish": "",
>> "poll_type": ""}, "id":  }

> http://127.0.0.1:8000/api/poll-delete/
>> method: DELETE 
>> users: admin
>> body: {"id": }

> http://127.0.0.1:8000/api/options-put/
>> method: PUT 
>> users: admin
>> body: {"id": , "new_options": []}

> http://127.0.0.1:8000/api/post-option/
>> method: POST
>> users: any
>> body: {"id": }

> http://127.0.0.1:8000/api/post-useroption/
>> method: POST
>> users: any
>> body: {"poll_id": , "options_od": ["id of options"], "user_id": }

> http://127.0.0.1:8000/api/old-polls/
>> method: POST
>> users: any
>> body: {"id": }








