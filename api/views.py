from rest_framework import generics, permissions,filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

# ----------------------------
#   VIEWSETS (Existing code)
# ----------------------------
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# ----------------------------
#   GENERIC VIEWS (New code)
# ----------------------------

# List all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # public read access
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']  # filter by these fields
    search_fields = ['title', 'author__name']  # search text in title or author name
    ordering_fields = ['title', 'publication_year']  # order by title or year
    ordering = ['title']  # default order

    def get_queryset(self):
        queryset = Book.objects.all()
        author_name = self.request.query_params.get('author')
        if author_name:
            queryset = queryset.filter(author__name__iexact=author_name)
        return queryset


# Retrieve one book
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a book with custom validation
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # must be logged in

    def perform_create(self, serializer):
        # Example of custom validation logic
        title = self.request.data.get("title", "").strip()
        if Book.objects.filter(title__iexact=title).exists():
            raise ValueError("A book with this title already exists.")
        serializer.save()


# Update an existing book with custom checks
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Example: prevent empty title updates
        if not self.request.data.get("title"):
            raise ValueError("Title cannot be empty.")
        serializer.save()


# Delete a book
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
