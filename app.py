from flask import Flask, request, jsonify, render_template
import time
from datetime import datetime
import requests

@app.route("/webhook",methods=['POST'])
def bot():
    obj = {}
    reply = ''
    str_now = time.strftime('%H:%M:%S')
    date_time_now =  datetime.strptime(str_now,'%H:%M:%S')
    str_day_week = datetime.today().strftime('%A')
    google_data =  request.get_json(silent=True)
    return jsonify({'fulfillmentText':reply} if len(reply)>=1 else obj)

@app.route("/")
def hello():
    return """
    <center>
    <h1> 
        This is a Bot Find it on https://<bot_client_link> 😊😊
     </h1>
     </center>
         
    """
