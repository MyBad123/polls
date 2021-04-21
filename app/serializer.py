from rest_framework import serializers
from .models import *

class PollSerializer(serializers.Serializer):
    poll_name = serializers.CharField(max_length=50)
    poll_desc = serializers.CharField(max_length=250)
    poll_start = serializers.DateTimeField()
    poll_finish = serializers.DateTimeField()
    poll_type = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.poll_name = validated_data.get('poll_name', instance.poll_name)
        instance.poll_desc = validated_data.get('poll_desc', instance.poll_desc)
        instance.poll_start = validated_data.get('poll_start', instance.poll_start)
        instance.poll_finish = validated_data.get('poll_finish', instance.poll_finish)
        instance.poll_type = validated_data.get('poll_type', instance.poll_type)
        instance.save()
        return instance
        

class OptionsSerializer(serializers.ModelSerializer):
    option_poll = serializers.IntegerField()
    option_options = serializers.CharField(max_length=50)
