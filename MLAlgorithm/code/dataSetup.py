import requests
import json
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime as dt
import datetime
from collections import Counter
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator


def getLiquidationsRawData():
    params = {
        "query":'{ markets(block: {number: 17493265}) { name liquidationThreshold maximumLTV liquidates { hash amountUSD blockNumber timestamp } } }',
        "operationName": None,
        "variables": None,
        }
    url = 'https://api.thegraph.com/subgraphs/name/messari/compound-v3-ethereum'

    data = requests.post(url, data=json.dumps(params)).json()

    liquidation_distribution = []
    liquidation_timestamps = []

    for i in range(len(data['data']['markets'])):
        tot_liquidation_usd = 0
        tot_liquidation = 0
        
        #we'll use the liquidation events in further articles, that's why we quey them but don't store anywhere
        #liquidations_events = []
        
        market = data['data']['markets'][i]['name']
        tot_liquidation = tot_liquidation + len(data['data']['markets'][i]['liquidates'])

        for k in range(len(data['data']['markets'][i]['liquidates'])):
            path = data['data']['markets'][i]['liquidates'][k]
            tot_liquidation_usd = tot_liquidation_usd + float(path['amountUSD'])
            liquidation_timestamps.append(dt.fromtimestamp(int(path['timestamp'])).date())
            
        liquidation_distribution.append({'marketName': market, 'liquidationNumber': tot_liquidation, 'USDAmountLiquidated': tot_liquidation_usd})


    return liquidation_distribution, liquidation_timestamps


    
def liquidationAnalysis(liquidation_distribution):

    #create piecharts
    labels = []
    usd_data =[]
    no_data = []

    for pool in liquidation_distribution:
        if pool['USDAmountLiquidated'] == 0 and pool['liquidationNumber'] == 0:
            continue
        else:
            labels.append(pool['marketName'])
            usd_data.append(pool['USDAmountLiquidated'])
            no_data.append(pool['liquidationNumber'])

    colors = sns.color_palette('pastel')

    #USD Liquidation Distrib PieChart
    plt.pie(usd_data, labels = labels, colors = colors, autopct='%.00f%%', explode = (0,0.3,0.6,0,0))
    plt.show()

    #No Liquidations Distrib PieChart
    plt.pie(no_data, labels = labels, colors = colors, autopct='%.00f%%')
    plt.show()
    

def getRawTimeData(poolId):
    start_date = datetime.date(2022, 8, 26)
    end_date = dt.today().date()
    liquidations_history = np.array([])
    
    params = {
        "query":'{ markets(where: {id: "%s"}) {liquidates { hash amountUSD blockNumber timestamp } } }'%(poolId),
        "operationName": None,
        "variables": None,
        }
    url = 'https://api.thegraph.com/subgraphs/name/messari/compound-v3-ethereum'
    liquidates = requests.post(url, data=json.dumps(params)).json()['data']['markets'][0]['liquidates']

    for i in range((end_date-start_date).days):
        
        current = start_date+datetime.timedelta(days=i)
        liquidation_count = 0
        liquidation_usd_amount = 0

        for liquidation in liquidates:
            liquidation_date = dt.fromtimestamp(int(liquidation['timestamp'])).date()

            if liquidation_date == current:
                liquidation_count = liquidation_count + 1
                liquidation_usd_amount = liquidation_usd_amount + float(liquidation['amountUSD'])

        liquidations_history = np.append(liquidations_history, [current, liquidation_count,liquidation_usd_amount]) 
    
    np.savetxt("ethLiquidationData.csv", liquidations_history.reshape(-1, 3), delimiter=",", fmt='%s')


def histogramsPlot():
    df = pd.read_csv('btcLiquidationData.csv', names = ["Date", "LiquidationCount", "LiquidationUSDCount"], sep=",")
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.bar(pd.to_datetime(df['Date']),df['LiquidationCount'],align='center')

    plt.xlabel('Days', fontsize=8)
    plt.ylabel('Number of liquidations')
    
    plt.show()


def frequencyAnalysis(poolId):
    df = pd.read_csv('ethLiquidationData.csv', names = ["Date", "LiquidationCount", "LiquidationUSDCount"], sep=",")

    one_hour_obs = 0
    one_day_obs = 0
    one_week_obs = 0
    two_week_obs = 0
    one_month_obs = 0

    last_liquidation = 0
    obs_count = 0

    params = {
        "query":'{ markets(where: {id: "%s"}) {liquidates(orderBy: timestamp) { hash amountUSD blockNumber timestamp } } }'%(poolId),
        "operationName": None,
        "variables": None,
        }
    url = 'https://api.thegraph.com/subgraphs/name/messari/compound-v3-ethereum'
    liquidates = requests.post(url, data=json.dumps(params)).json()['data']['markets'][0]['liquidates']


    for liquidate in liquidates:
        obs_count = obs_count + 1

        if last_liquidation == 0:
            last_liquidation = dt.fromtimestamp(int(liquidate['timestamp']))
            continue
        else:
            if (dt.fromtimestamp(int(liquidate['timestamp']))-last_liquidation).days > 0:
                days_delta = (dt.fromtimestamp(int(liquidate['timestamp']))-last_liquidation).days

                if 1 <= days_delta < 7:
                    one_week_obs = one_week_obs + 1
                if 7 <= days_delta <= 14:
                    two_week_obs = two_week_obs + 1
                if days_delta > 14:
                    one_month_obs = one_month_obs + 1
                    
            if (dt.fromtimestamp(int(liquidate['timestamp']))-last_liquidation).days == 0:
                if (dt.fromtimestamp(int(liquidate['timestamp']))-last_liquidation).seconds/3600 <= 1:
                    one_hour_obs = one_hour_obs + 1
                if (dt.fromtimestamp(int(liquidate['timestamp']))-last_liquidation).seconds/3600 > 1:
                    one_day_obs = one_day_obs + 1

        last_liquidation = dt.fromtimestamp(int(liquidate['timestamp']))

    y = [one_hour_obs/obs_count, one_day_obs/obs_count, one_week_obs/obs_count, two_week_obs/obs_count, one_month_obs/obs_count]
    x = [1,2,3,4,5]
    
    plt.bar(x,y,align='center')
    sns.kdeplot(x=x, weights=y, color = 'red')
    plt.xlabel('Category Days', fontsize=8)
    plt.ylabel('Probability')
    
    plt.show()
    
    


    
#poolId = "0xc3d688b66703497daa19211eedff47f25384cdc3c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
poolId = "0xc3d688b66703497daa19211eedff47f25384cdc32260fac5e5542a773aa44fbcfedf7c193bc2c599"

frequencyAnalysis(poolId)
