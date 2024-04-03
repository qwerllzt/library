from dbfunc import LibraryFunc

class LibraryInterface(LibraryFunc):
    def __init__(self, db_name):
        super().__init__(db_name)
        self.menu_options = {
            '1': self.add_new_book,
            '2': self.view_books_menu,
            '3': self.search_books_by_keyword,
            '4': self.delete_book,
            '5': self.exit_program
        }
        self.running = True
        
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

    # Метод main для запуска программы
    def main_menu(self):
        LibraryInterface.print_library_art() 
        while True:
            if not self.running:  
                break  
            print("\nВыберите действие:")
            print("1. Добавление новой книги")
            print("2. Просмотр списка книг")
            print("3. Поиск книги")
            print("4. Удаление книги")
            print("5. Выход")

            choice = input("Укажите необходимое действие >>> ")

            if choice in self.menu_options:
                self.menu_options[choice]()
            else:
                print("Неверный ввод. Попробуйте еще раз.")
                
    # Метод добавляет новую книгу в библиотеку.
    def add_new_book(self):
        print("\nДобавление новой книги:")
        exit_choice = input("Для возврата в главное меню нажмите Enter (или введите любой текст для продолжения): ")
        if not exit_choice:
            return
        
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        description = input("Введите описание книги: ")
        
        # Получаем список доступных жанров из базы данных
        genres = self.get_unique_genres()
        print("\nДоступные жанры:")
        for index, genre in enumerate(genres, start=1):
            print(f"{index}. {genre}")
        
        # Добавляем опцию для ввода пользовательского жанра
        print(f"{len(genres) + 1}. Другой жанр")
        
        genre_choice = input("Выберите жанр книги (введите номер из списка): ")
        try:
            genre_index = int(genre_choice) - 1
            if 0 <= genre_index < len(genres):
                genre = genres[genre_index]
            elif genre_index == len(genres):
                genre = input("Введите свой жанр книги: ")
            else:
                raise ValueError
        except ValueError:
            print("Неверный ввод.")
            return

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
                self.show_all_books()
            elif sub_choice == '2':
                self.view_books_by_genre()
            elif sub_choice == '3':
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")
                
    # Метод отображает список всех книг в библиотеке
    def show_all_books(self):
        books = self.view_all_books()
        if not books:
            print("Библиотека пуста!")
            return
        
        print("\nСписок всех книг в библиотеке:")
        for book in books:
            print(f"{book[0]}. {book[1]} - {book[2]}")
        book_id = input("Введите ID книги для просмотра подробной информации (или нажмите Enter чтобы вернуться в меню): ")
        if not book_id:
            return
        
        book_details = self.get_book_details(book_id)
        if not book_details:
            print("Книга с указанным ID не найдена.")
            return

        print("\nПодробная информация о книге:")
        print(f"Название: {book_details[1]}")
        print(f"Автор: {book_details[2]}")
        print(f"Описание: {book_details[3]}")
        print(f"Жанр: {book_details[4]}")

            
    # Метод отображает книги определенного жанра.
    def view_books_by_genre(self):
        print("\nДоступные жанры:")
        genres = self.get_unique_genres()
        for index, genre in enumerate(genres, start=1):
            print(f"{index}. {genre}")
        
        genre_choice = input("Выберите жанр для вывода книг (или нажмите Enter чтобы вернуться в меню): ")
        if not genre_choice:
            return

        try:
            selected_genre = genres[int(genre_choice) - 1]
            books_by_genre = self.get_books_by_genre(selected_genre)
            print(f"\nСписок всех книг жанра '{selected_genre}':")
            if books_by_genre:
                for book in books_by_genre:
                    print(f"{book[1]} - {book[2]}")
            else:
                print(f"Нет книг в жанре '{selected_genre}'.")
        except (ValueError, IndexError):
            print("Неверный ввод.")


    # Метод выполняет поиск книг по ключевому слову.
    def search_books_by_keyword(self):
        """
        Метод для поиска книги по ключевому слову.
        """
        print("\nПоиск книги:")
        keyword = input("Введите ключевое слово для поиска (Название и/или автора: ")
        found_books = self.search_books(keyword)
        if not found_books:
            print("Книги по вашему запросу не найдены.")
            return
        for book in found_books:
            print(f"Книги по вашему запросу:\n\n{book[1]} - {book[2]}")

    # Метод удаляет книгу из библиотеки.
    def delete_book(self):
        print("\nУдаление книги:")
        books = self.view_all_books()
        if not books:
            print("Библиотека пуста!")
            return
        
        print("Список всех книг:")
        for book in books:
            print(f"{book[0]}. {book[1]} - {book[2]}")
        
        book_id = input("Введите ID книги для удаления: ")
        if not book_id:
            return

        confirmation = input(f"Вы уверены, что хотите удалить книгу с ID {book_id}? (y/n): ")
        if confirmation.lower() == 'y':
            super().delete_book(book_id)
            print("Книга успешно удалена!")
        else:
            print("Удаление книги отменено.")

            
    def exit_program(self):
        print("\nВыход из программы.")
        self.running = False


def main():
    db_name = 'library.db'
    library_interface = LibraryInterface(db_name)
    library_interface.main_menu()

if __name__ == "__main__":
    main()
