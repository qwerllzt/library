import sqlite3

class LibraryManager:

    # Используются параметризованные запросы в sqlite, чтобы избежать sql-инъекций.
    
    def __init__(self, db_name):
        """
        Контсруктор  LibraryManager - Инициализаия подключения к базе данных и создание таблицы книг, если она не существует.

        db_name (str): Имя файла базы данных.
        """
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Метод для создания таблицы книг в базе данных, если она не существует.
        """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            author TEXT,
                            description TEXT,
                            genre TEXT
                            )''')
        self.conn.commit()

    def add_book(self, title, author, description, genre):
        """
        Метод для добавления новой книги в базу данных.

        Arguments:
            title (str): Название книги.
            author (str): Автор книги.
            description (str): Описание книги.
            genre (str): Жанр книги.
        """
        query = '''INSERT INTO books (title, author, description, genre) 
                   VALUES (?, ?, ?, ?)'''
        values = (title, author, description, genre)
        self.cur.execute(query, values)
        self.conn.commit()

    def delete_book(self, book_id):
        """
        Метод для удаления новой книги из базы данных.

        Arguments:
            book_id (int): ID книги.
        """
        query = '''DELETE FROM books WHERE id = ?'''
        self.cur.execute(query, (book_id,))
        self.conn.commit()

    def search_books(self, keyword):
        """
        Метод для поиска книги.

        Arguments:
            title (str): Название книги.
            author (str): Автор книги.
        """
        query = '''SELECT * FROM books WHERE title LIKE ? OR author LIKE ?'''
        values = ('%'+keyword+'%', '%'+keyword+'%')
        self.cur.execute(query, values)
        return self.cur.fetchall()

    def get_books_by_genre(self, genre):
        """
        Метод для поиска книг по определенному жанру.

        Arguments:
            genre (str): Жанр книги.
        """
        query = '''SELECT * FROM books WHERE genre = ?'''
        self.cur.execute(query, (genre,))
        return self.cur.fetchall()

    def get_unique_genres(self):
        """
        Получение всех доступных жанров.

        Arguments:
            genre (str): Жанр книги.
        """
        query = '''SELECT DISTINCT genre FROM books'''
        self.cur.execute(query)
        return [row[0] for row in self.cur.fetchall()]

    def view_all_books(self):
        """
        Получение всех книг в библиотеке

        Arguments:
            id (int): id книги.
            title (str): Название книги.
            author (str): Автор книги.
        """
        query = '''SELECT id, title, author FROM books'''
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_book_details(self, book_id):
        """
        Получение полной информации о книге 

        Arguments:
            id (int): id книги.
        """
        query = '''SELECT * FROM books WHERE id = ?'''
        self.cur.execute(query, (book_id,))
        return self.cur.fetchone()

    def __del__(self):
        self.conn.close()

