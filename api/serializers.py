from rest_framework import serializers
from .models import Author, Book

# =======================
# BookSerializer
# =======================
# Serializes all fields of the Book model.
# Includes custom validation for publication_year to prevent future dates.
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields in the Book model.

    # Custom validation method for publication_year.
    def validate_publication_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value


# =======================
# AuthorSerializer
# =======================
# Serializes the Author model including:
#   - The 'name' field
#   - A nested list of related books (via BookSerializer)
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer to represent books for this author.
    # Many=True since an author can have multiple books.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']  # Only include name + nested books.

    # NOTE: The relationship is handled using the 'related_name' in Book model's ForeignKey.
    # This lets DRF automatically fetch the author's books for serialization.
