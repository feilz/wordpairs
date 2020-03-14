from django.shortcuts import render
from rest_framework import generics
from .scanner.scanFiles import scan
# Create your views here.

class Filescanner(generics.ListCreateAPIView):
    
    def scan():
        scan()
        return "works"
    