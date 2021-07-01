import json
import uuid
import altair
import altair_saver
import datetime

from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--disable-setuid-sandbox") 
# chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--remote-debugging-port=9222") 
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
# options.binary_location = '/opt/google/chrome/google-chrome'
service_log_path = "chromedriver.log".format('app')
service_args = ['--verbose']
driver = webdriver.Chrome('/chromedriver/chromedriver',
        chrome_options=chrome_options,
        service_args=service_args,
        service_log_path=service_log_path)

vegaConfig = {
  "view": {
    "stroke": "transparent"
  },
  "axis": {
    "grid": False
  }
}

vegaSpec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "config": vegaConfig,
    "description": "MRR by Month",
    "mark": {
    "type": "line", 
    "tooltip": False, 
    "fill": None, 
    "stroke": "#010101",
    "point": {"color": "#010101"},
    },
    "encoding": {
        "x": {
            "field": "mrr_month_dt", 
            "timeUnit": "yearmonth", 
            "type": "temporal",
            "title": None,
            "axis": {
                "values": [
                    {"year": 2019, "month": "may", "date": 1},
                    {"year": 2021, "month": "may", "date": 1}
                ]
                }
        },
        "y": {
            "field": "mrr", 
            "aggregate": "sum", 
            "type": "quantitative",
            "title": None
        },
    },
    "data": {"values": []},
}

def getMrrByItem(df):
    mrrByItem = []
    for row in df.itertuples(index=True, name='Pandas'):
        mrr = 0
        maxUpTo = 0
        quantity = row.quantity
        tiers = row.tiers
        if tiers:
            for tier in tiers:
                ct = 1
                while ct <= quantity:
                    upTo = tier.get('up_to', 9999999999999999)
                    if not upTo:
                        upTo = 9999999999999999
                    if ct <= upTo:
                        mrr+= tier['amount']
        #                 return mrr
                    elif ct > upTo:
                        pass
                    else:
                        mrr+= tier['amount']
                    ct+=1
        mrrByItem.append(mrr)
    df['items_plan_amount'] = mrrByItem
    return df

def getChart(d):
    chartId = uuid.uuid4().hex
    # spec = json.loads(specs['mrr'])
    vegaSpec['data']['values'] = d
    chart = altair.Chart.from_dict(vegaSpec)
    filename = f'./static/{chartId}.png'
    altair_saver.save(chart, filename, method='selenium', webdriver=driver)
    return {'ok': True, 'chartId': chartId, 'filename': filename}

def getSummary(last3):
    summary = {}
    dt = datetime.datetime.utcnow()
    curr = last3[2]
    prev = last3[1]
    summary['growthGoal'] = .2
    summary['prcntThruMonth'] = dt.day / 30
    summary['growthGoalNow'] = summary['growthGoal'] * summary['prcntThruMonth']
    
    # mrr
    summary['currentMrr'] = curr['mrr']
    summary['previousMrr'] = prev['mrr']
    summary['mrrGrowth'] = summary['currentMrr'] - summary['previousMrr']
    summary['mrrGrowthPrcnt'] = summary['mrrGrowth'] / summary['previousMrr']
    summary['mrrArrow'] = 'arrow_up'
    if summary['mrrGrowth'] < 0:
        summary['mrrArrow'] = 'arrow_down'
    summary['growthGoalProgress'] = "You're ahead of your goal!"
    if summary['mrrGrowthPrcnt'] < summary['growthGoalNow']:
        summary['growthGoalProgress'] = "You're behind your goal, but lets catch up!"
    summary['currentMrrK'] = round(summary['currentMrr'] / 1000, 1)
    summary['mrrGrowthK'] = round(summary['mrrGrowth'] / 1000, 1)
    summary['mrrGrowthPrcntRounded'] = round(summary['mrrGrowthPrcnt'] * 100, 1)

    summary['mrrMsg'] = f"{summary['growthGoalProgress']} MRR is currently " 
    summary['mrrMsg'] += f"*${summary['currentMrrK']}k* :tada: \n:{summary['mrrArrow']}: "
    summary['mrrMsg'] += f"{summary['mrrGrowthPrcntRounded']}% (${summary['mrrGrowthK']}k) MTD."

    # customers
    summary['currentCustomers'] = curr['active']
    summary['previousCustomers'] = prev['active']
    summary['customerGrowth'] = summary['currentCustomers'] - summary['previousCustomers']
    summary['customerGrowthPrcnt'] = summary['customerGrowth'] / summary['previousCustomers']
    summary['customersArrow'] = 'arrow_up'
    if summary['customerGrowth'] < 0:
        summary['customersArrow'] = 'arrow_down'
    summary['customerGrowthPrcntRounded'] = round(summary['customerGrowthPrcnt'] * 100, 1)
    # \n\n<https://trypaper.io|20% of your customers> account for xx% of your MRR"

    summary['customerMsg'] = f"You current have {summary['currentCustomers']} customers :tada: \n" 
    summary['customerMsg'] += f":{summary['customersArrow']}: "
    summary['customerMsg'] += f"{summary['customerGrowthPrcntRounded']}% ({summary['customerGrowth']}) MTD."
    return summary