from dbreqs import LibraryManager

# Класс LibraryInterface, который наследует функциональность класса LibraryManager.
class LibraryInterface(LibraryManager):
    def __init__(self, db_name):
        super().__init__(db_name)

    # Функция для вывода изображения "library"
    @staticmethod
    def print_library_art():
        art = """
 /$$       /$$       /$$                                                                      
| $$      |__/      | $$                                                                      
| $$       /$$      | $$$$$$$         /$$$$$$         /$$$$$$         /$$$$$$        /$$   /$$
| $$      | $$      | $$__  $$       /$$__  $$       |____  $$       /$$__  $$      | $$  | $$
| $$      | $$      | $$  \ $$      | $$  \__/        /$$$$$$$      | $$  \__/      | $$  | $$
| $$      | $$      | $$  | $$      | $$             /$$__  $$      | $$            | $$  | $$
| $$      | $$      | $$$$$$$/      | $$            |  $$$$$$$      | $$            |  $$$$$$$
|__/      |__/      |_______/       |__/             \_______/      |__/             \____  $$
                                                                                     /$$  | $$
                                                                                    |  $$$$$$/
                                                                                     \______/                      
    """
        print(art)

    # Остальные методы класса...

    # Метод main для запуска программы
    def main_menu(self):
        self.print_library_art()
        while True:
            # Остальной код...

            print("\nВыберите действие:")
            print("1. Добавление новой книги")
            print("2. Просмотр списка книг")
            print("3. Поиск книги")
            print("4. Удаление книги")
            print("5. Выход")

            choice = input("Укажите необходимое действие >>> ")

            if choice == '1':
                self.add_new_book()
            elif choice == '2':
                self.view_books_menu()
            elif choice == '3':
                self.search_books()
            elif choice == '4':
                self.delete_book()
            elif choice == '5':
                print("\nВыход из программы.")
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")
                
    # Метод добавляет новую книгу в библиотеку.
    def add_new_book(self):
        print("\nДобавление новой книги:")
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        description = input("Введите описание книги: ")
        genre = input("Введите жанр книги: ")

        confirmation = input(f"Вы уверены, что хотите добавить книгу '{title}'? (y/n): ")
        if confirmation.lower() == 'y':
            self.add_book(title, author, description, genre)
            print("Книга успешно добавлена!")
        else:
            print("Добавление книги отменено.")

    # Метод отображает меню просмотра книг и обрабатывает выбор пользователя.
    def view_books_menu(self):
        while True:
            print("\nПросмотр списка книг:")
            print("1. Список всех книг")
            print("2. Вывести книги с определенным жанром")
            print("3. Вернуться в главное меню")

            sub_choice = input("Укажите необходимое действие >>> ")

            if sub_choice == '1':
                self.display_all_books()
            elif sub_choice == '2':
                self.view_books_by_genre()
            elif sub_choice == '3':
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")
                
    # Метод отображает список всех книг в библиотеке
    def display_all_books(self):
        books = self.view_all_books()
        if books:
            for book in books:
                print(f"{book[0]}. {book[1]} - {book[2]}")
            book_id = input("Введите ID книги для просмотра подробной информации (или нажмите Enter чтобы вернуться в меню): ")
            if book_id:
                book_details = self.get_book_details(book_id)
                if book_details:
                    print("\nПодробная информация о книге:")
                    print(f"Название: {book_details[1]}")
                    print(f"Автор: {book_details[2]}")
                    print(f"Описание: {book_details[3]}")
                    print(f"Жанр: {book_details[4]}")
                else:
                    print("Книга с указанным ID не найдена.")
        else:
            print("Библиотека пуста!")
            
    # Метод отображает книги определенного жанра.
    def view_books_by_genre(self):
        print("\nДоступные жанры:")
        genres = self.get_unique_genres()
        for index, genre in enumerate(genres, start=1):
            print(f"{index}. {genre}")
        genre_choice = input("Выберите жанр для вывода книг: ")
        try:
            selected_genre = genres[int(genre_choice) - 1]
            books_by_genre = self.get_books_by_genre(selected_genre)
            if books_by_genre:
                for book in books_by_genre:
                    print(f"{book[1]} - {book[2]}")
            else:
                print(f"Нет книг в жанре '{selected_genre}'.")
        except (ValueError, IndexError):
            print("Неверный ввод.")

    # Метод выполняет поиск книг по ключевому слову.
    def search_books(self):
        print("\nПоиск книги:")
        keyword = input("Введите ключевое слово для поиска: ")
        found_books = self.search_books(keyword)
        if found_books:
            for book in found_books:
                print(f"{book[1]} - {book[2]}")
        else:
            print("Книги по вашему запросу не найдены.")

    # Метод удаляет книгу из библиотеки.
    def delete_book(self):
        print("\nУдаление книги:")
        books = self.view_all_books()
        if books:
            print("Список всех книг:")
            for book in books:
                print(f"{book[0]}. {book[1]} - {book[2]}")
            book_id = input("Введите ID книги для удаления: ")

            confirmation = input(f"Вы уверены, что хотите удалить книгу с ID {book_id}? (y/n): ")
            if confirmation.lower() == 'y':
                super().delete_book(book_id)
                print("Книга успешно удалена!")
            else:
                print("Удаление книги отменено.")
        else:
            print("Библиотека пуста!")



def main():
    db_name = 'library.db'
    library_interface = LibraryInterface(db_name)
    library_interface.main_menu()

if __name__ == "__main__":
    main()
