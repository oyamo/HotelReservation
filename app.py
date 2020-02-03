from flask import Flask, request, jsonify, render_template
import lessons as lecs
import time
from datetime import datetime
import requests
PROJECT_ID = 'crypto-metric-237812'
KEY_FILE = './data/key.json'

app = Flask(__name__)



@app.route("/webhook",methods=['POST','GET'])
def bot():
    obj = {}
    str_now = time.strftime('%H:%M:%S')
    date_time_now =  datetime.strptime(str_now,'%H:%M:%S')
    str_day_week = datetime.today().strftime('%A')

    google_data =  request.get_json(silent=True)
    params = dict(google_data['queryResult']['parameters'])
    # str_date = '10:00:00'
    # time = datetime.strptime(str_date,'%H:%M:%S')
    requesting_next_lesson = 'lesson' in params.keys() and 'next' in params.keys()
    requesting_current_lesson = 'lesson' in params.keys() and 'current' in params.keys()
    requesting_lessons_wrt_day = 'WhatDoIhaveOn' in params.keys()
    requesting_tommorow_lesson = 'Tommorow' in params.keys()
    requesting_for_today_lesson = 'today' in params.keys()
    requesting_for_joke = 'Joke' in params.keys()


    print(True,True)
    reply = ''
    lectures = lecs.Lectures().lesson['mmu']
    ## REQUESTING NEXT LESSON 


    def get_current_lesson():
        """This function returns the current lesson"""
        filter_r = []
        if str_day_week in lectures.keys():
            lessons_wrt_day = lectures[str_day_week]
            lambda_current_lesson = lambda x: date_time_now >  datetime.strptime(x['start'],'%H:%M:%S') \
                                    and date_time_now <  datetime.strptime(x['stop'],'%H:%M:%S') 
            filter_r = list(filter(lambda_current_lesson,lessons_wrt_day))
            filter_r =  [] if len(filter_r) ==0  else filter_r[0]
        return filter_r



    def get_next_lesson():
        """This function returns the next lesson"""
        #Get the next lesson by comparing the times
        filter_r = [] # an empty list to store the filtered lessons
        if str_day_week in lectures.keys():
            lessons_wrt_day = lectures[str_day_week]
            filter_lambda = lambda x:date_time_now < datetime.strptime(x['start'],'%H:%M:%S') 
           
            #refactor the code 
            #next // tomorrow// specific day// today
            filter_r = list(filter(filter_lambda, lessons_wrt_day))
            filter_r = [] if len(filter_r) ==0  else filter_r[0]
        return filter_r
        


    def get_lesson_wrt_day(day):
        """This Returns all the lessons for the given day"""
        filter_r = []
        if day in lectures.keys():
            filter_r = lectures[day]
        return filter_r



    def get_tommorow_lesson():
        """This returns the tommorow's lesson"""
        days = ['Monday','Tuesday','Thursday','Friday','Saturday','Sunday']
        index = days.index(str_day_week)
        tommorow = days[0 if index == 6 else index +1]
        print(tommorow)
        """This Returns all the lessons for the given day"""
        filter_r = []
        if tommorow in lectures.keys():
            filter_r = lectures[tommorow]
        return {'day':tommorow,'data':filter_r}



    def get_today_lesson():
        """Returns  a list of tommorws's lessons"""
        filter_r = []
        if str_day_week in lectures.keys():
            filter_r = lectures[str_day_week]
        return filter_r
    def get_meme():
        r = requests.get('https://api.imgflip.com/get_memes')
        r_json = dict(r.json())
        jokes = r_json['data']['memes']
        import random
        joke = random.choice(jokes)
        title = joke['name']
        pic = joke['url']
        meme_obj =  {
                        "payload": {
                            "telegram": {
                                "expectUserResponse": True,
                                "richResponse": {
                                    "items": [
                                        {
                                            "basicCard": {
                                                "title": "Train",
                                                "image": {
                                                    "url": "https://8e39b052.ngrok.io/train.jpg",
                                                    "accessibilityText": "Train Image"
                                                },
                                                "imageDisplayOptions": "WHITE"
                                            }
                                        }
                                    ]
                                }
                            },
                            "google": {
                                "expectUserResponse": True,
                                "richResponse": {
                                    "items": [
                                        {
                                            "basicCard": {
                                                "title": "Train",
                                                "image": {
                                                    "url": "https://8e39b052.ngrok.io/train.jpg",
                                                    "accessibilityText": "Train Image"
                                                },
                                                "imageDisplayOptions": "WHITE"
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
        print(meme_obj)
        return meme_obj

    if requesting_next_lesson:
            #try and get the current lesson and ask the user to hurry to class
            current_lesson = get_current_lesson()
            next_lesson = get_next_lesson()
            
            if next_lesson == [] and current_lesson == []:
                reply = 'There are no more lectures for today, have a rest 😊😊'
                reply += '\n Hurray. Its Friday!!  😊😊' if str_day_week == 'Friday'\
                        else 'Its a weekend !!! Have fun' if str_day_week in ('Saturday','Sunday') else ''
            elif current_lesson !=[] and next_lesson == []:
                reply = '' 
                reply += "You currently have %s at which began  %s at %s,\n Please make it to if you haven't\n you are free after this" % (current_lesson['lesson'], current_lesson['start'], current_lesson['venue'])
            elif current_lesson ==[] and next_lesson != []:
                reply = '' 
                
                reply += "Coming up is %s at %s at %s, please reach %s before time" % (next_lesson['lesson'], next_lesson['start'], next_lesson['venue'],next_lesson['venue'])
            elif current_lesson != [] and next_lesson != []:
                reply = '' 
                reply += "You currently have %s which started at %s at %s" % (current_lesson['lesson'], current_lesson['start'], current_lesson['venue'])
                reply += "\nFollowed by %s at %s at %s, make it to  %s if you haven't" % (next_lesson['lesson'], next_lesson['start'], next_lesson['venue'],current_lesson['venue'])
    elif requesting_lessons_wrt_day:
        day_str = params['WhatDoIhaveOn']
        lessons = get_lesson_wrt_day(day_str)
        if lessons != []:
            arr = []
            for lesson in lessons:
                arr += ['%s at %s venue: %s'%(lesson['lesson'],lesson['start'], lesson['venue'])]
            
            if len(arr) > 1:
                if len(arr) == 2:
                    arr = [arr[0]+" and " + arr[1]]
                elif len(arr) > 2:
                    arr = arr[:-2] + [arr[-2]+' and '+ arr[-1]]
            reply = ','.join(arr)
        else:
            reply = 'Sorry I did not find any lecture on %s'%(day_str)

    #Checks for tomorrow's Lessons
    if requesting_tommorow_lesson:
        obj = get_tommorow_lesson()
        lessons = obj['data']
        day = obj['day']

        if lessons != []:
            arr = []
            reply = 'For Tommorrow(%s) you have '%(day)
            for lesson in lessons:
                arr += ['%s at %s venue: %s'%(lesson['lesson'],lesson['start'], lesson['venue'])]
            
            if len(arr) > 1:
                if len(arr) == 2:
                    arr = [arr[0]+" and " + arr[1]]
                elif len(arr) > 2:
                    arr = arr[:-2] + [arr[-2]+' and '+ arr[-1]]
            reply += ','.join(arr)
        else:
            reply = 'Sorry I did not find any lecture for Tommorow(%s),\n go on and have fun '%(day)
    if requesting_for_joke:
        joke = get_meme()
        reply = 'My joke module is under maintanance 😥'
        #reply = 'Im still getting trained on jokes'
    print('passes')
    if requesting_for_today_lesson:
        lessons = get_today_lesson()
    
        #Fetch the lessons then
        if lessons != []:
            arr = []
            reply = 'For Today(%s) you have '%(str_day_week)
            for lesson in lessons:
                arr += ['%s at %s venue: %s'%(lesson['lesson'],lesson['start'], lesson['venue'])]
            
            if len(arr) > 1:
                if len(arr) == 2:
                    arr = [arr[0]+" and " + arr[1]]
                elif len(arr) > 2:
                    arr = arr[:-2] + [arr[-2]+' and '+ arr[-1]]
            reply += ','.join(arr)
        else:
            reply = 'Sorry I did not find any lecture for Today, Have a rest 😊'
    return jsonify({'fulfillmentText':reply} if len(reply)>=1 else obj)


print(list(lecs.Lectures().lesson['mmu'].keys())[0])

@app.route("/")
def hello():
    return """
    <center>
    <h1> 
        This is an Azure Flask Web App 😊😊
     </h1>
     </center>
         
    """
