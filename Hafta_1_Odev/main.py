import requests

# API'ye bağlanmak için gerekli URL ve parametreleri tanımlayalım.
API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "YOUR_API_KEY"

# Kullanıcıdan bir şehir adı isteyelim.
city_name = input("Bir şehir adı girin: ")

# API'ye istek gönderelim.
response = requests.get(
    API_URL,
    params={
        "q": city_name,
        "appid": API_KEY,
    },
)

# API'den gelen yanıtı kontrol edelim.
if response.status_code == 200:
    # Yanıtı JSON formatında ayrıştıralım.
    response_json = response.json()

    # Çıktı için gerekli verileri hazırlayalım.
    city = response_json["name"]
    temp = response_json["main"]["temp"]
    weather_description = response_json["weather"][0]["description"]

    # Çıktıyı ekrana yazdıralım.
    print(f"Şehir: {city}")
    print(f"Sıcaklık: {temp} derece")
    print(f"Hava durumu: {weather_description}")

else:
    print("Başarısız")