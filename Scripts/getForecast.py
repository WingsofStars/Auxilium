import requests
import json
apiKey = "F0EGSWKDK5yZ9H8bEczPRO1hKwd69kEm"




def main(location, time=None):
    url = "https://api.tomorrow.io/v4/weather/realtime?location="+location+"&apikey=" + apiKey

    headers = {"accept": "application/json"}
    

    cloudyness = ""
    chanceOfRain = ""
    windyness = ""
    returnResponse = "It looks like it's "

    if time != None:
        url = "https://api.tomorrow.io/v4/weather/forecast?location="+location+"&timesteps=1d&apikey=" + apiKey
        response = requests.get(url, headers=headers)
        # r = (json.dumps(response, indent=4))
        responseJSON = json.loads(response.text)

        weatherData = responseJSON["timelines"]["daily"][1]["values"]
        cloudCover = weatherData["cloudCoverAvg"]
        precipitationProbability = weatherData["precipitationProbabilityAvg"]
        temperature = weatherData["temperatureAvg"]
        windGust = weatherData["windGustAvg"]

        if time == "tomorrow":
            returnResponse = "Tomorrow looks like it's going to be "
        else:
            returnResponse = "It looks like it's " 
    else:
    
        response = requests.get(url, headers=headers)
        # r = (json.dumps(response, indent=4))
        responseJSON = json.loads(response.text)
        
        weatherData = responseJSON["data"]["values"]
        cloudCover = weatherData["cloudCover"]
        precipitationProbability = weatherData["precipitationProbability"]
        temperature = weatherData["temperature"]
        windGust = weatherData["windGust"]

    temperatureConverted = int(float(temperature) * 9 /5 +32)

    if cloudCover > 9:
        cloudyness = "cloudy"
    elif cloudCover >4:
        cloudyness = "partially cloudy"
    else: 
        pass
    
    if precipitationProbability > 0.5:
        chanceOfRain = "with a chance of rain"
    elif precipitationProbability > 0.2:
        chanceOfRain = "with a slight chance of rain"

    if windGust > 8 :
        windyness = "and very windy"
    elif windGust >4 :
        windyness = "and windy"

    returnResponse = returnResponse + str(temperatureConverted) +" degrees, " + cloudyness +", " + windyness+ ", " + chanceOfRain
    print (returnResponse)
    
    return returnResponse
