import random
import sqlite3
import psycopg2




class User:
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.record_points = 1

    def get_my_points(self):
        return self.record_points

    def update_my_points(self, points):
        self.record_points = points

    def start_game(self):
        target_number = random.randint(1, 100)
        attempts = 6

        while attempts > 0:
            guess = int(input("Угадайте число от 1 до 100: "))

            if guess == target_number:
                print("Поздравляем, вы угадали правильное число!")
                if attempts < self.record_points:
                    self.update_my_points(attempts)
                break
            elif guess < target_number:
                print("Неверное предположение. Целевое число выше.")
            else:
                print("Неверное предположение. Целевое число ниже.")

            attempts -= 1

        if attempts == 0:
            print("Игра закончена. Вы использовали все свои попытки.")


def register():
    first_name = input("Введите свое имя: ")
    last_name = input("Введите свою фамилию: ")
    email = input("Введите ваш адрес электронной почты: ")
    password = input("Введите ваш пароль: ")

    user = User(first_name, last_name, email, password)

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT UNIQUE, password TEXT)")
    cursor.execute("INSERT INTO users VALUES (?, ?)", (email, password))
    connection.commit()
    connection.close()

    return user


def login(email, password):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    result = cursor.fetchone()
    connection.close()

    if result:
        user = User(None, None, email, password)
        return user
    else:
        return None


def sign_in():
    email = input("Введите ваш адрес электронной почты: ")
    password = input("Введите ваш пароль: ")

    user = login(email, password)

    if user:
        print("Авторизация прошла успешно!")
    else:
        print("Неверный адрес электронной почты или пароль.")


def sign_out():
    global user

    user = None

    print("Выход выполнен успешно!")


def main():
    user = None

    while True:
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("3. Начать игру")
        print("4. Посмотреть рекорд")
        print("5. выход")
        print("6. Покидать")

        choice = input("Введите свой выбор: ")

        if choice == "1":
            sign_in()
        elif choice == "2":
            user = register()
        elif choice == "3":
            if user:
                user.start_game()
            else:
                print("Сначала вам необходимо войти в систему.")
        elif choice == "4":
            if user:
                print("Ваш рекорд", user.get_my_points())
            else:
                print("Сначала вам необходимо войти в систему.")
        elif choice == "5":
            sign_out()
        elif choice == "6":
            break


if __name__ == "__main__":
    main()


conn = psycopg2.connect(host="localhost", database="postgres",
                        user="postgres", password="...")

cur = conn.cursor()
cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
databases = cur.fetchall()
print("Available databases:")
for i in range(len(databases)):
    print(f"{i+1}. {databases[i][0]}")

db = input("Enter the database you want to use: ")
print(f"Using database - {db.upper()}")