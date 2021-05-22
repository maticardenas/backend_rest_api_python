from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

"""

@author: Matías Cárdenas

"""

# As class based view.
class HelloApiView(APIView):
	""" Testing my first APIView"""

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