import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from weather import WeatherApp
from config import password, sender_mail_config
import datetime
import time


class Mail:
    def __init__(self,city,receiver_mail):
        self.city=city
        self.receiver_mail=receiver_mail

    def send_mail(self,city,receiver_mail):
        weather=WeatherApp(city)

        # Dane nadawcy i odbiorcy
        sender_email = sender_mail_config
        subject = f"Pogoda dla {weather.city.lower().capitalize()}, {datetime.date.today()}"
        body = f"{weather.return_string_data()}"

        # Tworzenie wiadomości email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_mail
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        weather.plot_weather_data()
        # Załączanie pliku wykresu
        filename = "wykres_pogody.png"
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )
            message.attach(part)

        # Logowanie do serwera SMTP i wysyłanie wiadomości
        try:
            # Zmiana na SMTP_SSL dla portu 465
            with smtplib.SMTP_SSL("smtp.poczta.onet.pl", 465) as server:
                server.login(sender_email,password)# logowanie za pomocą hasła
                server.sendmail(sender_email, receiver_mail, message.as_string())
                print("Wiadomość z załącznikiem wysłana pomyślnie!")
        except Exception as e:
            print(f"Błąd: {e}")


