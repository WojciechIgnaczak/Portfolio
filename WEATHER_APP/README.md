# WeatherApp Project
To jest projekt aplikacji umożliwiający wysyłanie informacji pogodowych odpowiednich miast na adresy mailowe użytkowników zamieszczonych w bazie danych sqlite3. Aplikacja oparta jest na API: *weather.visualcrossing.com*
## Instrukcja
#### Aby skorzystać z aplikacji należy:
pobrać z pliku *requirements.txt* potrzebne biblioteki 

w pliku config umieścić swój klucz API, adres mail oraz hasło z którego chcemy wysyłać maile

w pliku *database.py* dodać maile użytkowników i ich miasta za pomocą metody *insert_new_user*, a następnie za pomocą metody *send_mails* wysłać maile
#### Przykładowe użycie do wysłania maila jednorazowo
###### W pliku *database.py*
```
base=DataBase() #użycie klasy i automatyczne stworzenie bazy danych i tabeli
base.insert_new_user('example1@gmail.com','Warszawa') #dodanie użytkownika o adresie mailowym example1@gmail.com i pogodzie dla miasta Warszawa
base.insert_new_user('example2@gmail.com','Kraków')
base.insert_new_user('example3@gmail.com','Katowice')
base.update_city('example2@gmail.com','Gdańsk') #zmiana miasta dla użytkowanika example2@gmail.com
base.delete_user('example3@gmail.com') #usunięcie użytkownika z bazy danych
base.send_mails() #wysłanie maili o pogodzie dla odpowiednich miast do wszystkich adresów w bazie danych 
```

#### Przykładowe użycie do wysłania maila co 24h
###### W pliku *database.py*
```
import time
base=DataBase() #użycie klasy i automatyczne stworzenie bazy danych i tabeli
base.insert_new_user('example1@gmail.com','Warszawa') #dodanie użytkownika o adresie mailowym example1@gmail.com i pogodzie dla miasta Warszawa
base.insert_new_user('example2@gmail.com','Kraków')
base.insert_new_user('example3@gmail.com','Katowice')
base.update_city('example2@gmail.com','Gdańsk') #zmiana miasta dla użytkowanika example2@gmail.com
base.delete_user('example3@gmail.com') #usunięcie użytkownika z bazy danych
while True:
    base.send_mails() #wysłanie maili o pogodzie dla odpowiednich miast do wszystkich adresów w bazie danych
    time.sleep(86400) #wstrzymanie na 24 godziny (86400 sekund)
```
# Config.py
## Plik zawierający dane potrzebne do konfiguracji programu:
**apikey:** zawiera klucz do API

**password:** zawiera hasło do adresu pocztowego z którego wysyłane są maile

**sender_mail_config** zawiera adres mail, z którego będą wysyłane maile

# Unit_constans.py
## Plik zawierający klasę Unit_and_Constans umożliwiającą stałe i konwersje danych, która zawiera metody:
**FtoC:** umożliwia zamianę stopni Fareheita na Celsjusza

**Mph_to_kmh:** umożliwia zamianę prędkości w milach na godzinę na kilomentry na godzinę

**Cal_to_mm:** umożliwia zamianę cali na milimetry

**wind_degrees:** zawiera słownik, w którym klucze to krotki zawierające przedział stopni wiania wiatru, a wartością jest kierunek wiatru

# Database.py
## Plik zawierający klasę DataBase,która zawiera łączenie z bazą danych oraz wysyła maila do wszystkich użytkowników która zawiera metody:
**init:** nawiązuje połączenie z bazą danych 'mail.db' sqlite3 i tworzy jeśli nie istnieje tabele zawierającą id, mail na który będzie wysyłana informacja pogodowa, miasto, którego pogoda będzie wysyłana. Mail musi być unikalny, nie da się wysłać kilku informacji pogodowych na 1 maila

**insert_new_user:** umożliwia dodawanie nowego użytkownika aplikacji do którego informacja pogodowa będzie wysyłana, trzeba podać mail oraz miasto

**delete_user:** umożliwia usunięcie użytkownika z bazy danych na podstawie maila

**update_city:** umożliwia aktualizację miasta dla którego ma być wysyłana informacja pogoda, trzeba podać mail oraz nazwę nowego miasta

**display_all:** umożliwia wyświetlenie wszystkich maili i miast, jakie są wpisane do bazy danych

**return_all:** zwraca w formie tablicy krotek wszystkich użytkowników i ich miast 

**send_mails:** umożliwia wysyłanie maili korzystając z metody z Mail z pliku "send_mail.py" do wszystkich użytkowników bazy

**delete_data_base:** umożliwia usunięcie całej bazy danych, przydatna metoda do testowania poprwności działania programu, do codziennego działania programu bezużyteczna

# Send_mail.py
## Plik zawierający klasę Mail, która umożliwia wysyłanie maili, która zawiera metodę:
**send_mail:** umożliwia wysyłanie maila z informacją pogodową do konkretnego odbiorcy, wysyła informację ogólną, informacje godzinową a także załącznik z wykresem temperatury, szans opadów, ilości opadów(jeśli są)

# Weather.py
## Plik zawierający klasę WeatherApp, która umożliwia pobranie danych pogodowych, która zawiera metody:
**fetch_weather_data**: umożliwia pobranie danych z api i wykorzystanie ich w metodach display_weather_info oraz display_hourly_forecast

**display_weather_info:** umożliwia na podstawie danych z API, pobranie podstawowych informacji pogodowych takich jak: data, miejsce, temperatura maksymalna, temperatura odczuwalna, prędkość i kierunek wiatru, czas wschodu i zachodu słońca, oraz krótki opis tłumaczony z angielskiego na polski za pomocą biblioteki translate

**process_hourly_data:** umożliwia na podstawie danych z API dodawanie do odpowiednich słowników, gdzie kluczem jest godzina, a wartościami: temperatura,szansa opadów,ilość opadów. Metoda ta sumuje także ilość opadów

**display_hourly_forecast:** wykorzystuje metode process_hourly_data, a następnie zapisuje do tablicy info string zawierający informacje godzinową tzn.godzine,temperature,prędkość i kierunek wiatru,szanse opadów, oraz jeśli jest to ilość opadów

**display_data:** wyświetla dane z metody fetch_weather_data, czyli wyświetla display_weather_info oraz display_hourly_forecast

**return_string_data:** zwraca wszystko to co wyświetla display_data w formie stringa

**display_all_data:** wyświetla to samo co display_data oraz tworzy i zapisuje odpowiedni wykres o nazwie "wykres_pogoda.png"

**plot_weather_data:** tworzy i zapisuje plik pod nazwą "wykres_pogoda.png" na którym znajdują się 2 lub 3 wykresy. Wszystkie wykresy są słupkowe, 1 temperaturowy zawierający dane temperatury 24h co godzine, szanse opadów w % co godzine, oraz wykres warunkowy:ilość opadów w milimetrach co godzine, jego istnienie zależy od tego czy suma opadów jest większa od 0.