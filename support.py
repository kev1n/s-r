import oandapyV20
import oandapyV20.endpoints.instruments as instruments
from oandapyV20 import API
import plotly.graph_objects as go
import pandas as pd
import trendy
import numpy as np
def candles(candlenumber, candlelength, instrument):
    ACCESS_TOKEN = "YOUR TOKEN"
    ACCOUNT_ID = "YOUR ID"
    api = oandapyV20.API(access_token=ACCESS_TOKEN, environment="practice")

    params = {
            "count": candlenumber,
            "granularity": candlelength
        }

    instrum = instruments.InstrumentsCandles(instrument=instrument, params=params)
    json_response = api.request(instrum)

    candlestickinfo = json_response['candles']

    opening = []
    closing = []
    high = []
    low = []
    times = []
    volumes = []


    for i in candlestickinfo:
        opening.append(float(i['mid']['o']))
        closing.append(float(i['mid']['c']))
        high.append(float(i['mid']['h']))
        low.append(float(i['mid']['l']))
        volumes.append(i['volume'])

        times.append(i['time'])
    return opening, closing, high, low, volumes, times

def graph(periodsback, candlenumber, candlelength, instrument):
    newer = []

    opening, closing, high, low, volumes, times = candles(500, candlelength, instrument)

    periodsback = periodsback
    nphigh = np.average(high[-(periodsback):-1])
    npclose = np.average(closing[-(periodsback):-1])
    nplow = np.average(low[-(periodsback):-1])

    pivot = (nphigh + npclose + nplow) / 3
    S1 = (2 * pivot) - nphigh
    R1 = (2 * pivot) - nplow
    S2 = pivot - (nphigh - nplow)
    R2 = pivot + (nphigh - nplow)
    S3 = pivot - 2 * (nphigh - nplow)
    R3 = pivot + 2 * (nphigh - nplow)

    for i in times:
        newtimes = i.replace('T', ' ')
        replacelast = newtimes[0:19]
        newer.append(replacelast)
        
    datas = {'Date': newer,
            'Open': opening,
            'High': high,
            'Low': low,
            'Close': closing,
            }

    df = pd.DataFrame(datas, columns = ['Date', 'Open', 'High', 'Low', 'Close'])

    candlestick = go.Candlestick(x=df['Date'],
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])
    figure = go.Figure(data=[candlestick])
    figure.layout.xaxis.type = 'category'

    figure.add_shape(
            # Line Horizontal
                type="line",
                x0=newer[-(periodsback)],
                y0=S1,
                x1=newer[-1],
                y1=S1,
                line=dict(
                    color="LightSeaGreen",
                    width=2,
                    dash="dashdot",
                ),
        )
    figure.add_shape(
            # Line Horizontal
                type="line",
                x0=newer[-(periodsback)],
                y0=S2,
                x1=newer[-1],
                y1=S2,
                line=dict(
                    color="LightSeaGreen",
                    width=2,
                    dash="dashdot",
                ),
        )

    figure.add_shape(
            # Line Horizontal
                type="line",
                x0=newer[-(periodsback)],
                y0=S3,
                x1=newer[-1],
                y1=S3,
                line=dict(
                    color="LightSeaGreen",
                    width=2,
                    dash="dashdot",
                ),
        )

    figure.add_shape(
            # Line Horizontal
                type="line",
                x0=newer[-(periodsback)],
                y0=R1,
                x1=newer[-1],
                y1=R1,
                line=dict(
                    color="LightSeaGreen",
                    width=2,
                    dash="dashdot",
                ),
        )

    figure.add_shape(
            # Line Horizontal
                type="line",
                x0=newer[-(periodsback)],
                y0=R2,
                x1=newer[-1],
                y1=R2,
                line=dict(
                    color="LightSeaGreen",
                    width=2,
                    dash="dashdot",
                ),
        )

    figure.add_shape(
            # Line Horizontal
                type="line",
                x0=newer[-(periodsback)],
                y0=R3,
                x1=newer[-1],
                y1=R3,
                line=dict(
                    color="LightSeaGreen",
                    width=2,
                    dash="dashdot",
                ),
        )


    figure.show()

graph(25, 100, 'H1', 'GBP_JPY')