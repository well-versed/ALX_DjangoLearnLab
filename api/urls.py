from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import ( 
    BookViewSet, BookListView,
     BookCreateView, BookUpdateView, BookDeleteView
         )


#router viewsets
router= DefaultRouter()
router.register(r"books_all",BookViewSet)

urlpatterns = [
    #viewset routes
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    
    #generic view routes
    path('books/', BookListView.as_view(), name='book-list-create'),
     path('books-create/', BookCreateView.as_view(), name='book-create'),
    path('books-update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    path('books-delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]
