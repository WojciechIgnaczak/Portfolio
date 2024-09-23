import sqlite3
import os
from send_mail import Mail

class DataBase:
    def __init__(self):
        # Nawiązanie połączenia z bazą danych
        conn = sqlite3.connect('mail.db')
        cursor = conn.cursor()

        # Utworzenie kursora, który wykonuje zapytania SQL
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mail TEXT NOT NULL UNIQUE,
                city TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_new_user(self, mail, city):
        conn = sqlite3.connect('mail.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mail(mail, city)
            VALUES (?, ?)
        ''', (mail, city))
        conn.commit()
        conn.close()

    def delete_user(self, mail):
        conn = sqlite3.connect('mail.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM mail
            WHERE mail = ?
        ''', (mail,))
        conn.commit()
        conn.close()

    def update_city(self, mail, new_city):
        conn = sqlite3.connect('mail.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE mail
            SET city = ?
            WHERE mail = ?
        ''', (new_city, mail))
        conn.commit()
        conn.close()
    
    def display_all(self):
        conn = sqlite3.connect('mail.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM mail')
        rows = cursor.fetchall()

        for row in rows:
            print(row)
        conn.commit()
        conn.close()

    def return_all(self):
        conn = sqlite3.connect('mail.db')
        cursor = conn.cursor()
        cursor.execute('SELECT mail,city FROM mail')
        rows = cursor.fetchall()
        data=[]
        for row in rows:
            data.append(row)
        conn.commit()
        conn.close()   
        return data
    
    def send_mails(self):
        data=self.return_all()
        for i in data:
            receiver_mail=i[0]
            city=i[1]
            mail=Mail(city,receiver_mail)
            mail.send_mail(city,receiver_mail)

    def delete_data_base(self):
        if os.path.exists('mail.db'):
            os.remove('mail.db')
            print("Baza danych została usunięta.")
        else:
            print("Baza danych nie istnieje.")
# Tworzenie obiektu bazy danych
base = DataBase()
#base.insert_new_user('pogoda3@onet.pl','warszawa')
# Przykładowe użycie metod
# base.insert_new_user('pogoda04@onet.pl','Rzeszów')
# base.insert_new_user('wojciech.ignaczak@onet.pl','Płock')
# base.send_mails()
# base.display_all()
base.delete_data_base()