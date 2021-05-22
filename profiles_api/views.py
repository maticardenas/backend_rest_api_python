from typing import Optional, Any

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# List of handy http status codes to return
from rest_framework import status

from profiles_api import serializers

"""

@author: Matías Cárdenas

"""

# As class based view.
class HelloApiView(APIView):
	""" Testing my first APIView"""
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


