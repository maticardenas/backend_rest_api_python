from typing import Optional, Any

from django.http import HttpResponse, HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

# List of handy http status codes to return
from rest_framework import status
from rest_framework.viewsets import ViewSet, ModelViewSet

from profiles_api import serializers, models, permissions

"""

@author: Matías Cárdenas

"""

# As class based view.

class HelloAPIView(APIView):
	"""
	Testing my first APIView

	APIViews are mostly used when:
	* We need full customization and control in our API logic
	* Processing files and provifing synchronous response

	"""
	serializer_class = serializers.HelloSerializer

	def get(self, request: HttpRequest, format=None) -> HttpResponse:
		"""Returns a list of APIView features"""
		an_apiview = [
			"Uses HTTP methods as function (get, post, patch, put, delete)",
			"Is similar to a traditional DjangoView",
			"Gives you the most control over you application logic",
			"It's mapped manually to URLs",
		]

		response = {
			"message": "hello",
			"an_apiview": an_apiview
		}

		return Response(response)

	def post(self, request: HttpRequest) -> HttpResponse:
		""" Create a hello message with our name """
		# Standard way of working with serializers in APIView
		serializer = self.serializer_class(data=request.data)

		# same as django forms
		if serializer.is_valid():
			name = serializer.validated_data.get("name")
			message = f"Hello {name}"
			response = {"message": message}
			return Response(response)
		else:
			return Response(
				serializer.errors,
				status=status.HTTP_400_BAD_REQUEST
			)

	def put(self, request: HttpRequest, pk: Optional[Any] = None) -> HttpResponse:
		""" Handle update of an object (full object) """
		response = {
			"method": "PUT"
		}
		return Response(response)

	def patch(self, request: HttpRequest, pk: Optional[Any] = None) -> HttpResponse:
		""" Handle update of an object (specified field) """
		response = {
			"method": "PATCH"
		}
		return Response(response)

	def delete(self, request: HttpRequest, pk: Optional[Any] = None) -> HttpResponse:
		""" Handle deleting of an object """
		response = {
			"method": "DELETE"
		}
		return Response(response)


class HelloViewSet(ViewSet):
	"""
	View Sets provide already logic for basic HTTP operations

	Useful when we need to build basic database APIs in our application
	"""

	serializer_class = serializers.HelloSerializer

	def list(self, request: HttpRequest) -> HttpResponse:
		""" Returns a hello message """

		a_viewset = [
			"Uses actions (list, create, retrieve, update, partial_update)",
			"Automatically maps to URLs using Routers",
			"Provides more functionality with less code"
		]

		response = {
			"message": "Hello!",
			"a_viewset": a_viewset
		}

		return Response(response)

	def create(self, request: HttpRequest) -> HttpResponse:
		"""Create a new hello message."""
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			name = serializer.validated_data.get("name")
			message = f"Hello {name}!"
			response = {
				"message": message
			}
			return Response({"message": message})
		else:
			return Response(
				serializer.errors,
				status=status.HTTP_400_BAD_REQUEST
			)

	def retrieve(self, request: HttpRequest, pk: Optional["Any"] = None) -> HttpResponse:
		"""Handle getting an object by its ID"""
		response = {
			"http_method": "GET"
		}
		return Response(response)

	def update(self, request: HttpRequest, pk: Optional["Any"] = None) -> HttpResponse:
		"""Handle updating an object"""
		response = {
			"http_method": "PUT"
		}
		return Response(response)

	def partial_update(self, request: HttpRequest, pk: Optional["Any"] = None) -> HttpResponse:
		"""Handle updating part of an object"""
		response = {
			"http_method": "PATCH"
		}
		return Response(response)

	def destroy(self, request: HttpRequest, pk: Optional["Any"] = None) -> HttpResponse:
		"""Handle removing an object"""
		response = {
			"http_method": "DELETE"
		}
		return Response(response)


class UserProfileViewSet(ModelViewSet):
	""" Handle Creating and Updating Profiles """
	serializer_class = serializers.UserProfileSerializer
	queryset = models.UserProfile.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.UpdateOwnProfile,)
	filter_backends = (filters.SearchFilter,)
	search_fields = ("name", "email",)


class UserLoginAPIView(ObtainAuthToken):
	""" Handling creating user authentication tokens """
	renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(ModelViewSet):
	""" Handles creating, reading and updating Profile Feed Items """
	serializer_class =  serializers.ProfileFeedItemSerializer
	queryset =  models.ProfileFeedItem.objects.all()
	authentication_classes = (TokenAuthentication,)
	permission_classes = (
		permissions.UpdateOwnStatus,
		#IsAuthenticatedOrReadOnly -> Lets to ONLY read the API list
		IsAuthenticated, # Won't give access to the API to non-authenticated users
	)

	def perform_create(self, serializer: serializers.ProfileFeedItemSerializer):
		""" Sets the user profile to the logged in user """
		serializer.save(user_profile=self.request.user)