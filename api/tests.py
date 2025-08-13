from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book, Author


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create authors
        self.author1 = Author.objects.create(name="John Doe")
        self.author2 = Author.objects.create(name="Jane Smith")
        self.author3 = Author.objects.create(name="Dan Bader")

        # Create some book instances
        self.book1 = Book.objects.create(title="Django Basics", author=self.author1, publication_year=2020)
        self.book2 = Book.objects.create(title="Advanced Django", author=self.author2, publication_year=2021)
        self.book3 = Book.objects.create(title="Python Tricks", author=self.author3, publication_year=2019)

        # URLs
        self.list_url = reverse('book-list')
        self.detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})

    def authenticate(self):
        """Helper method to authenticate the test user"""
        self.client.login(username='testuser', password='testpass')

    # ---------- CRUD TESTS ----------
    def test_create_book_authenticated(self):
        self.authenticate()
        data = {
            "title": "New Book",
            "author": "Author X",
            "publication_year": 2022
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "No Auth Book",
            "author": "Author Y",
            "publication_year": 2022
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book_detail(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Django Basics")

    def test_update_book_authenticated(self):
        self.authenticate()
        data = {
            "title": "Updated Django Basics",
            "author": "John Doe",
            "publication_year": 2020
        }
        response = self.client.put(self.detail_url(self.book1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Django Basics")

    def test_delete_book_authenticated(self):
        self.authenticate()
        response = self.client.delete(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------- FILTER, SEARCH, ORDER TESTS ----------
    def test_filter_books_by_author(self):
        response = self.client.get(f"{self.list_url}?author=John Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(book['author'] == "John Doe" for book in response.data))

    def test_search_books_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Advanced")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Advanced Django" in book['title'] for book in response.data))

    def test_order_books_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))


"""
HOW TO RUN TESTS:
    python manage.py test api

These tests cover:
    - CRUD operations
    - Permission restrictions
    - Filtering, searching, and ordering functionality
"""
