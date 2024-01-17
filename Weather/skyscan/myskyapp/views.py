from django.shortcuts import render
import requests

def home(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        api_key = "f04cef006e3a47a09a183737231806"
        base_url = "https://api.weatherapi.com/v1/forecast.json"
        
        if location:
            params = {"key": api_key, "q": location, "days": 4}
            response = requests.get(base_url, params=params)
            data = response.json()

            if "error" in data:
                error_msg = "Error: Invalid location or API key"
                return render(request, 'index.html', {'error_msg': error_msg})

            current = data["current"]
            location_info = data["location"]
            forecast = data["forecast"]["forecastday"][1:4]

            context = {
                'location': f"{location_info['name']}, {location_info['country']}",
                'temperature': f"{current['temp_c']}°C",
                'condition': current['condition']['text'],
                'wind_speed': f"{current['wind_kph']} km/h",
                'pressure': f"{current['pressure_mb']} mb",
                'humidity': f"{current['humidity']}%",
                'feels_like': f"{current['feelslike_c']}°C",
                'forecast_data': [
                    {
                        'date': day['date'],
                        'temperature': f"{day['day']['avgtemp_c']}°C",
                        'condition': day['day']['condition']['text'],
                    } for day in forecast
                ]
            }

            return render(request, 'index.html', context)

    return render(request, 'index.html')
