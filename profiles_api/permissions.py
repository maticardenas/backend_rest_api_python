from typing import TYPE_CHECKING

from rest_framework import permissions

if TYPE_CHECKING:
	from django.http import HttpRequest
	from profiles_api.models import UserProfile
	from profiles_api.views import UserProfileViewSet


class UpdateOwnProfile(permissions.BasePermission):
	def has_object_permission(self, request: "HttpRequest", view: "UserProfileViewSet", obj: "UserProfile") -> bool:
		""" Check User is trying to edit their own profile """
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
	""" Allows users to update THEIR OWN status """
	def has_object_permission(self, request: "HttpRequest", view: "UserProfileViewSet", obj: "UserProfile") -> bool:
		""" Check the user is trying to update their own status """
		# If it's GET then just allow to retrieve it
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.user_profile.id == request.user.id


