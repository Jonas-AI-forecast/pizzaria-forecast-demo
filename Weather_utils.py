import requests

def hent_vejrdata():
    api_key = "DIN_API_NØGLE"  # ← erstat med din rigtige nøgle
    url = f"https://api.openweathermap.org/data/2.5/weather?lat=55.6667&lon=12.4000&units=metric&appid={api_key}"
    
    response = requests.get(url)
    data = response.json()

    temperatur = data['main']['temp']
    vejrtype = data['weather'][0]['description']
    return temperatur, vejrtype
