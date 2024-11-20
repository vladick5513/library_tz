import json
from typing import List, Dict, Optional

class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: Dict):
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"],
        )

class Library:
    def __init__(self, storage_file: str = "library.json"):
        self.storage_file = storage_file
        self.books: List[Book] = []
        self._load_books()

    def _load_books(self):
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.books = []

    def _save_books(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> Book:
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(id=new_id, title=title, author=author, year=year)
        self.books.append(new_book)
        self._save_books()
        return new_book

    def delete_book(self, book_id: int) -> bool:
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self._save_books()
            return True
        return False

    def find_book_by_id(self, book_id: int) -> Optional[Book]:
        return next((book for book in self.books if book.id == book_id), None)

    def search_books(self, query: str, field: str) -> List[Book]:
        if field not in ["title", "author", "year"]:
            raise ValueError("Поле для поиска должно быть title, author или year")
        return [book for book in self.books if str(getattr(book, field)).lower() == query.lower()]

    def list_books(self) -> List[Book]:
        return self.books

    def update_status(self, book_id: int, status: str) -> bool:
        book = self.find_book_by_id(book_id)
        if book and status in ["в наличии", "выдана"]:
            book.status = status
            self._save_books()
            return True
        return False
