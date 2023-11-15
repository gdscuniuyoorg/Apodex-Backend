from django.contrib.auth import password_validation

from .models import UserProfile

from django.contrib.auth import get_user_model

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'password2', 'name')

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        validate_password(password)  

        return data

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        refresh = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    about = serializers.CharField()
    short_description = serializers.CharField(max_length=255)
    instagram_link = serializers.URLField(required=False, allow_blank=True)
    facebook_link = serializers.URLField(required=False, allow_blank=True)
    twitter_link = serializers.URLField(required=False, allow_blank=True)
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        fields = ('name', 'about', 'short_description', 'instagram_link', 'facebook_link', 'twitter_link', 'profile_photo')

class UserProfileUpdateSerializer(UserProfileSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = UserProfileSerializer.Meta.fields + ('current_password', 'new_password', 'new_password2')

    def validate(self, data):
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        new_password2 = data.get('new_password2')

        if (new_password or new_password2) and not current_password:
            raise serializers.ValidationError("Current password is required to change the password.")

        if current_password and not self.instance.user.check_password(current_password):
            raise serializers.ValidationError("Incorrect current password.")

        if new_password != new_password2:
            raise serializers.ValidationError("New passwords do not match.")

        if new_password:
            password_validation.validate_password(new_password, self.instance.user)

        return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.about = validated_data.get('about', instance.about)
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.instagram_link = validated_data.get('instagram_link', instance.instagram_link)
        instance.facebook_link = validated_data.get('facebook_link', instance.facebook_link)
        instance.twitter_link = validated_data.get('twitter_link', instance.twitter_link)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)

        new_password = validated_data.get('new_password')
        if new_password:
            instance.user.set_password(new_password)
            instance.user.save()

        instance.save()
        return instance
