from django.db import models

<<<<<<< HEAD
#represents a writer in the sytem

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    #represents  the books in the system 


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()

    #each book is linked to exactly one author
    #one author many books
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    #if author is deleted,their books are deleted

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

=======
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} by {self.author}"
>>>>>>> e6b7f6858cc326b09854aa30769aa37e890f5214
