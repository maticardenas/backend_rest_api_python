from rest_framework import serializers

# Sample learning serializer
from profiles_api import models


class HelloSerializer(serializers.Serializer):
	""" Serializes a name field for testing my first APIView"""
	name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
	"""
		Serializes a UserProfile object.

		With ModelSerializer we work with MetaClass to connect the serializer to a specific Model
	"""
	class Meta:
		model = models.UserProfile
		fields = ("id", "email", "name", "password")

		extra_kwargs = {
			"password": {
				"write_only": True, # We only want password to create new objects, not retrieving
				"style": {"input_type": "password"} # Don't show password while writing it
			}
		}

	# We override the default create function provided by ModelSerializer specifically
	# for setting the password to be saved as a hash
	def create(self, validated_data):
		""" Creates and returns a new user """
		user = models.UserProfile.objects.create_user(
			email=validated_data["email"],
			name=validated_data["name"],
			password=validated_data["password"]
		)

		return user

	def update(self, instance, validated_data):
		""" Handle updating user account """
		if 'password' in validated_data:
			password = validated_data.pop('password')
			instance.set_password(password)

		return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
	""" Serializes Profile Feed items """
	class Meta:
		model = models.ProfileFeedItem
		fields = ("id", "user_profile", "status_text", "created_on")

		#We want the user_profile to be assigned only to the current authenticated user
	    # therefore we make read-only

		extra_kwargs = {
			"user_profile": {
				"read_only": True
			}
		}