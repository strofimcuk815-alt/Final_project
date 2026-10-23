import sqlite3
import requests
from bs4 import BeautifulSoup

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sites.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sites (url TEXT)")
        self.conn.commit()

    def add(self, url):
        self.cursor.execute("INSERT INTO sites VALUES (?)", (url,))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT url FROM sites")
        return [row[0] for row in self.cursor.fetchall()]

    def clear(self):
        self.cursor.execute("DELETE FROM sites")
        self.conn.commit()

class Parser:
    def count_word(self, url, word):
        try:
            response = requests.get(url, timeout=4)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            return text.lower().count(word.lower())
        except:
            return 0

class UserInterface:
    def __init__(self, db, parser):
        self.db = db
        self.parser = parser

    def start(self):
        while True:
            print("\n--- ГОЛОВНЕ МЕНЮ ---")
            print("1. Додати сайт")
            print("2. Переглянути сайти")
            print("3. Очистити базу даних")
            print("4. Пошук слова")
            print("5. Вихід")

            choice = input("Виберіть дію (1-5): ")

            if choice == "1":
                url = input("Введіть URL сайту: ")
                self.db.add(url)
                print("Сайт додано")

            elif choice == "2":
                sites = self.db.get_all()
                print("Список сайтів:", sites if sites else "База порожня")

            elif choice == "3":
                self.db.clear()
                print("Базу очищено!")

            elif choice == "4":
                word = input("Введіть слово для пошуку: ")
                sites = self.db.get_all()
                results = []

                for site in sites:
                    count = self.parser.count_word(site, word)
                    if count > 0:
                        results.append((site, count))

                results.sort(key=lambda x: x[1], reverse=True)

                print("\nРезультати пошуку:")
                for site, count in results:
                    print(f" {site} — згадок: {count}")

            elif choice == "5":
                print("Вихід...")
                break

def run():
    db = Database()
    parser = Parser()
    ui = UserInterface(db, parser)
    ui.start()


if __name__ == "__main__":
    run()