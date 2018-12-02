from rest_framework import serializers
from .models import  CourseComments
from ..users.models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','username')

class CommentsSerilizer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = CourseComments
        fields = ('id','user','comments','add_time')