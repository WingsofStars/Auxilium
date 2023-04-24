import requests

apikey = "AIzaSyAAqvxczW4ABWsOsaxKQlBDE4Ul1amwuGQ"

searchRequest = requests.get('https://www.googleapis.com/customsearch/v1?key='+apikey +'&cx=022adc636a1f945c0&q="what is an API"')
print (searchRequest.json())