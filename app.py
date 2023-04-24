from flask import Flask, request, render_template
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
 
# "/" is the default route. This is the route that will be called default when you visit the site.
@app.route('/', methods=['GET'])  
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def index_post():

    # Initialize the variables
    original_text = ''
    target_language = ''

    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']
    
    if request.method == 'POST' and original_text == '':
     print('Error Message: You need to enter some text to translate.')
     return render_template('index.html')
    
    else:
    # Load the values from .env
     key = os.environ['KEY']
     endpoint = os.environ['ENDPOINT']
     location = os.environ['LOCATION']

    # Indicate to translate and the API version (3.0) and the target language
     path = '/translate?api-version=3.0'
    # Add the target language parameter
     target_language_parameter = '&to=' + target_language
    # Create the full URL
     constructed_url = endpoint + path + target_language_parameter

    # The header information, which includes our subscription key
     headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # The body of the request with the text to be translated
     body = [{ 'text': original_text }]

    # Make the call using post
     translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
     translator_response = translator_request.json()
    # Retrieve the translation
     translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
     return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
     )
    

if __name__ == '__main__':
    app.run()