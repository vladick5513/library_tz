from library import Library

def main():
    library = Library()

    while True:
        print("\n--- Меню ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книг")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                book = library.add_book(title, author, year)
                print(f"Книга добавлена: {book.to_dict()}")

            elif choice == "2":
                book_id = int(input("Введите ID книги для удаления: "))
                if library.delete_book(book_id):
                    print("Книга удалена.")
                else:
                    print("Книга с таким ID не найдена.")

            elif choice == "3":
                field = input("Введите поле для поиска (title, author, year): ").lower()
                query = input("Введите значение для поиска: ")
                books = library.search_books(query, field)
                if books:
                    for book in books:
                        print(book.to_dict())
                else:
                    print("Книги не найдены.")

            elif choice == "4":
                books = library.list_books()
                if books:
                    for book in books:
                        print(book.to_dict())
                else:
                    print("Библиотека пуста.")

            elif choice == "5":
                book_id = int(input("Введите ID книги: "))
                status = input("Введите новый статус (в наличии, выдана): ")
                if library.update_status(book_id, status):
                    print("Статус книги обновлён.")
                else:
                    print("Ошибка обновления статуса.")

            elif choice == "6":
                print("Выход из программы.")
                break

            else:
                print("Некорректный выбор, попробуйте снова.")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()