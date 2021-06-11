from django.forms import fields
from rest_framework import serializers
from DocPlus.models import AddRequest, AppUser, FaqBlog, Prescription, Profile, UserDoctor, Patholab, Hospital, Collector, Transaction
from django.http import HttpResponse

from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

class UserSerializer(serializers.ModelSerializer):
    def get_data(self, obj):
        user = self.context['request'].user
        return user

    class Meta:
        model = User 
        fields = ('username', 'email','first_name','last_name', 'id')

class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token


    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email','first_name','last_name','token', 'username', 'password','id')

class UserUpdateSerialier(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'})
    email = serializers.CharField(
        style={'input_type': 'email'}
    )
    class Meta:
        model = User
        fields = ('pk', 'email', 'password')

    def update(self, instance, validated_data):
        instance.email(validated_data.get('email', instance.email))
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


# class AppUserSerializer(serializers.ModelSerializer):
#     parser_classes = (MultiPartParser, FormParser)
#     # def get_user(self):
#     #     user = self.context["user"].user
#     #     return user

#     # def get_object(self):
#     #     pk = self.context["pk"].pk
#     #     user = get_object_or_404(User, id=pk)
#     #     obj, created  = AppUser.objects.get_or_create(
#     #             user=user)
#     #     if obj == None:
#     #         raise Http404
#     #     return obj
#     # def create(self, validated_data):
#     #     self.get_object()
#     #     return AppUser.objects.create(**validated_data)
    # def create(self, validated_data):
    #     user = self.get_user()
    #     docuser = AppUser.objects.create(user=user,
    #     user_type = validated_data['user_type'],
    #     Name = validated_data['Name'],
    #     phone = validated_data['phone'],
    #     dob= validated_data['dob'],
    #     state = validated_data['state'],
    #     city = validated_data['city'],
    #     address_line = validated_data['address_line'],
    #     profileImg = validated_data['profileImg'],
    #     zip_code =validated_data['zip_code']
    #     )
    #     docuser.save()
    #     return docuser

#     class Meta:
#         model = AppUser 
#         fields = '__all__'

class AppUserSerializer(serializers.ModelSerializer):
    # parser_classes = (MultiPartParser, FormParser)

    class Meta:
        model = AppUser 
        fields = '__all__'
        lookup_field = 'slug'
        # fields = ('user_type','Name','phone','dob','state','city','address_line','profileImg','zip_code')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile 
        fields = '__all__'
        lookup_field = 'userprofile'

class AllUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = ('username',)
    



class UserDoctorSerializer(serializers.ModelSerializer):
    # parser_classes = (MultiPartParser,)
    class Meta:
        model = UserDoctor
        fields = '__all__'
        lookup_field = 'slug'


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = '__all__'
        lookup_field = 'slug'


class AmbulanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = '__all__'
        lookup_field = 'slug'

class PatholabSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patholab
        fields = '__all__'
        lookup_field = 'slug'

class CollectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collector
        fields = '__all__'
        lookup_field = 'slug'

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        lookup_field = 'slug'

class AddRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddRequest
        fields = '__all__'
        # lookup_field = 'fromuser'


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prescription
        fields = '__all__'

class FaqBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = FaqBlog
        fields = '__all__'
        

