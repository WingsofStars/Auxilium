from deepgram import Deepgram
import json

API_KEY = '619838795b88f3e51cda87cdb4b7aa87ab35cdf2'

PATH_TO_FILE = 'C:/Users/ndelbridge/Documents/School/Capstone/output.wav'
MIMETYPE = 'audio/wav'

def sendRequest():
    # Initializes the Deepgram SDK
    dg_client = Deepgram(API_KEY)
    
    with open(PATH_TO_FILE, 'rb') as audio:
        source = {'buffer': audio, 'mimetype': MIMETYPE}
        options = { "punctuate": True, "model": "nova", "language": "en-US" }
    
        print('Requesting transcript...')
        print('Your file may take up to a couple minutes to process.')
        print('While you wait, did you know that Deepgram accepts over 40 audio file formats? Even MP4s.')
        print('To learn more about customizing your transcripts check out developers.deepgram.com')
    
        response = dg_client.transcription.sync_prerecorded(source, options)
        r = (json.dumps(response, indent=4))
        responseJSON = json.loads(r)
        return responseJSON
        

        


transcription = sendRequest()["results"]["channels"][0]["alternatives"][0]["transcript"]
print(transcription)