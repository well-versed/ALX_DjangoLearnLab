from django.shortcuts import render

# Create your views here.
<<<<<<< HEAD
=======
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated  # Add this if missing

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Add this line
>>>>>>> e6b7f6858cc326b09854aa30769aa37e890f5214
