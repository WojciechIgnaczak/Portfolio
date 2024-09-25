import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from translate import Translator
from config import api_key
from unit_constans import Unit_and_Constans
import datetime

sns.set()


class WeatherApp:
    def __init__(self, city):
        self.__api_key =api_key
        self.city = city
        self.temperature = {}
        self.precipitation = {}
        self.precip = {}
        self.translator = Translator(from_lang="en", to_lang="pl")
        self.con_and_cons=Unit_and_Constans()

    def fetch_weather_data(self):
    # pobieranie danych z API    
        try:
            date = datetime.date.today()
            url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.city}/{date}?key={self.__api_key}'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                r=self.display_weather_info(data)
                f=self.display_hourly_forecast(data)
                return r,f
            else:
                print(f"Error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        

    def display_weather_info(self, data): # Wyświetlenie podstawowych danych
        try:
            info=[    
                f"Data: {data['days'][0]['datetime']}, Miejsce: {data['resolvedAddress']}",
                f"Temperatura: {self.con_and_cons.FtoC(data['days'][0]['tempmax'])}°C, Temperatura Odczuwalna: {self.con_and_cons.FtoC(data['days'][0]['feelslikemax'])}°C",
                f"Wiatr: {self.con_and_cons.Mph_to_kmh(data['days'][0]['windspeed'])} km/h {self.con_and_cons.wind_degrees(data['days'][0]['winddir'])}, Opady: {self.con_and_cons.Cal_to_mm(data['days'][0]['precip'])} mm",
                f"Wschód słońca: {data['days'][0]['sunrise']}, Zachód słońca: {data['days'][0]['sunset']}",
                f"{self.translator.translate(data['days'][0]['description'])}\n"]
            return info
        except KeyError as e: print(f"Error: {e}")
        except Exception as e: print(f"Error: {e}") 


    def process_hourly_data(self, data): # pobieranie danych godzinowych o temperaturze,szans opadów,opadów
        hours = [f"{h}:00" for h in range(24)]  
        for i in range(24):
            self.temperature[hours[i]] = self.con_and_cons.FtoC(data['days'][0]['hours'][i]['temp'])
            self.precipitation[hours[i]] = round(data['days'][0]['hours'][i]['precipprob'])
            self.precip[hours[i]] = self.con_and_cons.Cal_to_mm(data['days'][0]['hours'][i]['precip'])
        self.sum_precip=sum(self.precip.values())


    def display_hourly_forecast(self, data): # Wyświetlanie danych godzinowym
        self.process_hourly_data(data)
        try:
            info=[]
            hours = [f"{h}:00" for h in range(24)]  # Przykładowe godziny
            for i in range(24):
                to_print_1 = f"Godzina: {data['days'][0]['hours'][i]['datetime']}, Temperatura: {self.con_and_cons.FtoC(data['days'][0]['hours'][i]['temp'])}°C,"
                to_print_2 = f" Wiatr: {self.con_and_cons.Mph_to_kmh(data['days'][0]['hours'][i]['windspeed'])} km/h {self.con_and_cons.wind_degrees(data['days'][0]['hours'][i]['winddir'])},"
                to_print_3 = f" Szansa opadów: {data['days'][0]['hours'][i]['precipprob']}%,"
                to_print_4 = f" Opady: {self.con_and_cons.Cal_to_mm(data['days'][0]['hours'][i]['precip'])} mm" if self.precip[hours[i]] > 0 else ""
                info.append(to_print_1 + to_print_2 + to_print_3 + to_print_4)
            return info
        except KeyError as e: print(f"Error: {e}")
        except Exception as e: print(f"Error: {e}")


    def display_data(self):
        weather_tables=self.fetch_weather_data()
        for weather_table in weather_tables:
            for j in weather_table:
                print(j)

    def return_string_data(self):
        data=""
        weather_tables=self.fetch_weather_data()
        for weather_table in weather_tables:
            for j in weather_table:
                data+=f"{j}\n"
        return data

    def display_all_data(self):
        self.display_data()
        self.plot_weather_data()

    
    def plot_weather_data(self): # wykresy
        # robienie Series z słowników
        try:
            temp_series = pd.Series(self.temperature)
            precip_series = pd.Series(self.precipitation)
            pre_series = pd.Series(self.precip)

            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))

            # Wykres temperatury
            bars_temp = temp_series.plot(kind='bar', title=f'{self.city.upper()}\n Temperatura [°C]', color='red', ax=ax1, fontsize=8)
            ax1.grid(True)

            for bar in bars_temp.patches:
                ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 3, f'{bar.get_height()}°', ha='center', va='bottom', color='black', fontsize=8)

            # Wykres szansy opadów
            bars_precip = precip_series.plot(kind='bar', title='Szansa Opadów [%]\n', color='blue', ax=ax2, fontsize=8)
            ax2.set_ylim(0)
            ax2.grid(True)

            for bar in bars_precip.patches:
                ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height()}%'if bar.get_height() >0 else "", ha='center', va='bottom', color='purple', fontsize=8)

            # Wykres opadów
            if self.sum_precip > 0:
                bars_pre = pre_series.plot(kind='bar', title='Opady [mm]\n', color='grey', ax=ax3, fontsize=8)
                ax3.set_ylim(0)
                ax3.grid(True)

                for bar in bars_pre.patches:
                    ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height()}' if bar.get_height() >0 else "", ha='center', va='bottom', color='purple', fontsize=10)
            else:
                ax3.axis('off')

            plt.tight_layout()
            plt.savefig("./wykres_pogody.png")
            plt.close()
        except Exception as e: print(f"Error: {e}")

