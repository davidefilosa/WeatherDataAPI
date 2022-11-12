from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


stations = pd.read_csv('data_small/stations.txt', skiprows=17)
stations = stations.iloc[:, :2].to_html()


@app.route("/")
def home():
    return render_template('home.html', stations=stations)


@app.route("/api/v1/<station>/<date>")
def date(station, date):
    filename = f'data_small/TG_STAID{str(station).zfill(6)}.txt'
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature
            }

@app.route("/api/v1/<station>")
def station(station):
    filename = f'data_small/TG_STAID{str(station).zfill(6)}.txt'
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient='records')
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def year(station, year):
    filename = f'data_small/TG_STAID{str(station).zfill(6)}.txt'
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype('str')
    df = df[df['    DATE'].str.startswith(str(year))]
    result = df.to_dict(orient='records')
    return result



if __name__ == '__main__':
    app.run(debug=True)
