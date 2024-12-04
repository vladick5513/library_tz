import unittest
import os
from app.library import Library


class TestLibrary(unittest.TestCase):
    TEST_STORAGE_FILE = "test_library.json"

    def setUp(self):
        """Подготовка тестового окружения."""
        self.library = Library(storage_file=self.TEST_STORAGE_FILE)

    def tearDown(self):
        """Удаление тестового файла."""
        if os.path.exists(self.TEST_STORAGE_FILE):
            os.remove(self.TEST_STORAGE_FILE)

    def test_add_book(self):
        """Тест добавления книги."""
        book = self.library.add_book("Тестовая книга", "Автор", 2024)
        self.assertEqual(book.title, "Тестовая книга")
        self.assertEqual(book.author, "Автор")
        self.assertEqual(book.year, 2024)
        self.assertEqual(book.status, "в наличии")
        self.assertTrue(book.id > 0)

    def test_delete_book(self):
        """Тест удаления книги."""
        book = self.library.add_book("Тестовая книга", "Автор", 2024)
        result = self.library.delete_book(book.id)
        self.assertTrue(result)
        self.assertFalse(self.library.find_book_by_id(book.id))

    def test_delete_nonexistent_book(self):
        """Тест удаления несуществующей книги."""
        result = self.library.delete_book(999)
        self.assertFalse(result)

    def test_search_books(self):
        """Тест поиска книг."""
        self.library.add_book("Тестовая книга", "Автор1", 2024)
        self.library.add_book("Другая книга", "Автор2", 2023)
        found_books = self.library.search_books("Автор1", "author")
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0].title, "Тестовая книга")

    def test_update_status(self):
        """Тест изменения статуса книги."""
        book = self.library.add_book("Тестовая книга", "Автор", 2024)
        result = self.library.update_status(book.id, "выдана")
        self.assertTrue(result)
        updated_book = self.library.find_book_by_id(book.id)
        self.assertEqual(updated_book.status, "выдана")

    def test_update_status_invalid(self):
        """Тест изменения статуса на некорректное значение."""
        book = self.library.add_book("Тестовая книга", "Автор", 2024)
        result = self.library.update_status(book.id, "неизвестный статус")
        self.assertFalse(result)
        self.assertEqual(book.status, "в наличии")

    def test_list_books(self):
        """Тест получения всех книг."""
        self.library.add_book("Книга 1", "Автор1", 2024)
        self.library.add_book("Книга 2", "Автор2", 2023)
        books = self.library.list_books()
        self.assertEqual(len(books), 2)

    def test_save_and_load(self):
        """Тест сохранения и загрузки данных."""
        self.library.add_book("Книга для теста", "Автор", 2024)
        self.library._save_books()

        # Перезагружаем библиотеку и проверяем, что данные сохранились
        new_library = Library(storage_file=self.TEST_STORAGE_FILE)
        books = new_library.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Книга для теста")
        self.assertEqual(books[0].author, "Автор")


if __name__ == "__main__":
    unittest.main()