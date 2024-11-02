from django.shortcuts import render
from rest_framework.views import APIView


class SearchView(APIView):
    def get(self, request):
        print("dksnfls")