from dataclasses import fields
from httplib2 import Response
from pexpect import ExceptionPexpect
from rest_framework import serializers
from stripe import Source
from .models import User, Zone, Notification, Activity, Score,Package,Purchasepackage,Invitation
from django.contrib.auth.hashers import make_password

from api import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print('==============validated_data==============>', validated_data)
        user = User.objects.create(**validated_data)
        print('----------------usrer------------------', user)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=254)

    class Meta:
        model = User
        fields = ['email', 'password']


class ShowinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']


class ZoneSerializer(serializers.ModelSerializer):
    user = ShowinfoSerializer(read_only=True)

    class Meta:
        model = Zone
        fields = ['name', 'description', 'user']


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        depth = 1
        fields = ['name', 'description', 'zone', 'to_user', 'from_user']


class ShowNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        depth = 1

        fields = ['id', 'name', 'description', 'from_user', 'to_user']


class AcceptrejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        depth = 1
        fields = ['name', 'description', 'to_user', 'from_user']


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Activity
        fields = ['id', 'name', 'description','user']


class ScoreSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'score', 'hours', 'minitus',
            'seconds', 'activity', 'user']

    def create(self, validated_data):
        print("=========VALIDATE_DATA ======>", validated_data['user'])
        activity = validated_data['activity']
        print("*************** activity id *************", activity.id)

        score = Score.objects.filter(activity=activity.id,  user=validated_data['user'])
        if score.exists():
                score_value = score.first()

                if validated_data['score'] >= score_value.score:

                    score.update(score=validated_data['score'], hours=validated_data['hours'],minitus=validated_data['minitus'], seconds=validated_data['seconds'])
                    print(" ****************score**************")
                    return Response({"messs":"data update"})
                
                elif validated_data['hours'] <= score_value.hours:

                        score.update(hours=validated_data['hours'],minitus=validated_data['minitus'], seconds=validated_data['seconds'])
                        print("*********** Hours ******************")
                elif validated_data['minitus'] <= score_value.minitus:
                       
                        score.update(minitus=validated_data['minitus'], seconds=validated_data['seconds'])
                        print("**************** MINITU ******************")
                elif validated_data['seconds'] <= score_value.seconds:

                        score.update(seconds=validated_data['seconds'])
                        print("********************* SECONDS ********************")
                        
                        return score
                else:
                        
                        return Response({"messs":"data update"})
        
        else:
            print("******** ENTER THE DATA ********************") 
            score = Score.objects.create(**validated_data)
            print('----------------usrer------------------',score)
            score.save()
            return score


   

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Package
        fields = ['name','price','account','activity']


class PurchaseackageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    package = PackageSerializer(read_only = True)
    class Meta:
        model = Purchasepackage
        fields = ['user','package']   


class InvitationSerializer(serializers.ModelSerializer):
    from_to = UserSerializer(read_only=True)
    class Meta:
        model = Invitation
        fields = ['from_to','email']

class SecondRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone','primary_user']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print('==============validated_data==============>', validated_data)
        user = User.objects.create(**validated_data)
        print('----------------usrer------------------', user)
        user.set_password(validated_data['password'])
        print("********************************set password ***********************")
        user.save()
        return user