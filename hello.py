import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request
import requests
import pytz
import pandas as pd

app = Flask(__name__)
id = ''
@app.route("/" , methods=["POST", "GET"])
def hello_world():
    if request.method == "GET":
        return 'Hello World'
    else:
        pass
@app.route("/data",methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return render_template('home.html',)
    else:
        id = request.form['id']
        print(request.form['id'])
        utc=pytz.UTC
        
        # first = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations/{}/readings?latest'.format(id))
        # station_latest = first.text
        measures = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations/{}/measures'.format(id))
        measures_one_station = measures.text
        now = utc.localize(datetime.now())
        today = now.strftime('%Y-%m-%d')
        yest = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d')
        x = requests.get('https://environment.data.gov.uk/flood-monitoring/id/stations/{}/readings?startdate={}&enddate={}'.format(id,yest,today)).text
        measure_set = set()
        for j in json.loads(measures_one_station)['items']:
            measure_set.add(j['notation'])
        meas_dic = {i:[] for i in measure_set}
        for i in json.loads(x)['items']:
            time_ = datetime.strptime(i['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            _start = now-timedelta(hours=24)
            if _start <= time_ <= now:
                for j in meas_dic.keys():
                    if j in i['measure']:
                        meas_dic[j].append(i['value'])
        df = pd.DataFrame(meas_dic)
        df.to_csv('test_{}.csv'.format(id))
        return render_template('home.html',)


## instead of refresh button automatically reload the page evevry 15 minutes
## add code for latitude and longitude