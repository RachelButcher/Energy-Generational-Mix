# import flask and create app instance
from flask import Flask, jsonify, request, render_template
import requests
import json
import sys
app = Flask(__name__)

@app.route("/")
def googlechart():
    headers = {
        'Accept': 'application/json'
    }
    r = requests.get('https://api.carbonintensity.org.uk/generation', params={}, headers=headers)
#convert JSON to python dictionary
    to_python = json.loads(r.text)
    generation_mix = to_python.get("data").get("generationmix")

#create empty dictionary and re-populate with custom information
    dict = {"Fuel": "Percent"}
    for i in generation_mix:
        dict[i.get("fuel")] = int(i.get("perc"))

# pass value into overlay
    total = dict.get("solar") + dict.get("wind") + dict.get("hydro") + dict.get("nuclear")
    return render_template('Piechart.html', data=dict, total=total)

if __name__ == "__main__":
    #debug=True restarts server as new code added
    app.run(debug=True)