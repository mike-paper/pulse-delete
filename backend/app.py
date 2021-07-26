from flask import Flask
import flask

import json
import os
import sys
import uuid
from flask_cors import CORS 
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
import sqlalchemy
import pandas as pd
import yaml
import subprocess

# import selenium.webdriver

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1420,1080')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(chrome_options=chrome_options)
# chromedriver
# driver = webdriver.Chrome('/chromedriver/chromedriver')


from logger import logger
from metrics import metrics

SQLALCHEMY_DATABASE_URI = os.environ.get('PAPER_SQLALCHEMY_DATABASE_URI')
# SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

session_options = {
    'autocommit': True
}
db = SQLAlchemy(app, session_options=session_options)

import pints

pints.scheduler.startScheduler(db.engine)

def getTeamDomain(email):
    return email.split('@')[1]

def checkForTeam(engine, email, userId):
    domain = getTeamDomain(email)
    sql = '''
    SELECT 
    u.id as user_id, t.id as team_id
    FROM 
    public.users as u inner join
    public.team_membership as tm on u.id = tm.user_id inner join
    public.teams as t on tm.team_id = t.id
    WHERE 
    t.domain = '{domain}'
    order by u.created_on desc
    '''.format(domain = domain)
    df = pd.read_sql(sql, db.engine)
    if len(df) > 0:
        logger.info(f'already team for {domain}')
    else:
        logger.info(f'no team for {domain}, creating...')
        teamId = pints.postgres.insertTeam(engine, domain)
        teamMembershipId = pints.postgres.insertTeamMember(engine, teamId, userId)
        logger.info(f'adding user to team {teamId}...')
    return True

# with app.app_context():
# scs = pints.stripe.getCustomers(db.engine, 3)

# logger.info(f'scs len: {len(scs)}')
# logger.info(f'scs: {scs}')

# subs = pints.stripe.getSubscriptions(db.engine, 1)

# logger.info(f'subs len: {len(subs)}')
# logger.info(f'subs: {subs}')

# subItems = pints.stripe.getSubscriptionItems(db.engine, 1)

# logger.info(f'subItems len: {len(subItems)}')
# logger.info(f'subItems: {subItems}')

# testStripe = pints.stripe.getPlans(db.engine, 1)

# testStripe = pints.stripe.getObject(db.engine, 1, 'coupons')
# testStripe = pints.stripe.getObject(db.engine, 1, 'invoices')
# testStripe = pints.stripe.getAll(db.engine, 4)
# testStripe = pints.scheduler.testSched()

@app.route('/ping', methods=["GET"])
def ping():
    j = {'ok': True}
    return json.dumps(j), 200, {'ContentType':'application/json'}

@app.route('/get_stripe', methods=["GET", "POST"])
def get_stripe():
    data = flask.request.get_json()
    logger.info(f'get_stripe: {data}')
    user = getUser(data)
    jobIds = pints.stripe.getAll(db.engine, user['team_id'])
    return json.dumps({'ok' : True, 'jobIds': jobIds}), 200, {'ContentType':'application/json'}

@app.route('/get_dbt', methods=["GET", "POST"])
def get_dbt():
    data = flask.request.get_json()
    logger.info(f'get_dbt: {data}')
    user = getUser(data)
    d = pints.modeling.getDbt()
    return json.dumps({'ok' : True, 'data': d}), 200, {'ContentType':'application/json'}

@app.route('/get_raw_counts', methods=["GET", "POST"])
def get_raw_counts():
    data = flask.request.get_json()
    logger.info(f'get_raw_counts: {data}')
    user = getUser(data)
    counts = pints.postgres.getRawTableCounts(db.engine, user['team_id'])
    return json.dumps({'ok' : True, 'counts': counts}), 200, {'ContentType':'application/json'}

@app.route('/run_dbt', methods=["GET", "POST"])
def run_dbt():
    data = flask.request.get_json()
    logger.info(f'run_dbt: {data}')
    user = getUser(data)
    dbtLogs, dbtErrors = pints.modeling.runDbt(user['team_id'])
    return json.dumps({
        'ok' : True, 
        'dbtLogs': dbtLogs, 
        'dbtErrors': dbtErrors
        }), 200, {'ContentType':'application/json'}

@app.route('/run_analysis', methods=["GET", "POST"])
def run_analysis():
    data = flask.request.get_json()
    user = getUser(data)
    logger.info(f'run_analysis: {data}')
    sql = pints.yaml2sql.dbt2Sql(data['dbt'], f"team_{user['team_id']}_stripe")
    logger.info(f'run_analysis sql: {sql}')
    try:
        df = pd.read_sql(sql['sql'], db.engine)
    except Exception as e:
        logger.error(f'run_analysis error: {e}')
        return {
            'ok': False,
            'error': str(e),
            'sql': sql,
        }
    logger.info(f'run_analysis df: {df.head()}')
    cols = df.columns.tolist()
    cols2 = []
    for col in cols:
        # import pdb; pdb.set_trace()
        colFormat = [s for s in sql['selected'] if s['alias'] == col]
        if colFormat:
            colFormat = colFormat[0].get('format', False)
        else:
            colFormat = False
        col2 = {
            'name': col,
            'format': colFormat
            }
        cols2.append(col2)
    df = df.to_json(date_format = 'iso', orient='values',
        default_handler=str)
    return json.dumps(
        {
            'ok' : True,
            'sql': sql,
            'rows': json.loads(df, strict=False),
            'cols': cols2,
        }), 200, {'ContentType':'application/json'}

def getUser(data):
    logger.debug(f'getUser: {data}')
    publicAddress = data['user'].get('publicAddress', False)
    if not publicAddress:
        d = {
            'ok': False,
            'reason': 'noUser'
        }
        return d
    sql = '''
    SELECT 
    u.id as user_id, u.email, u.details, tm.team_id as team_id
    FROM 
    public.users as u left join
    public.team_membership as tm on u.id = tm.user_id
    WHERE 
    u.details ->> 'publicAddress' = '{publicAddress}'
    order by tm.created_on desc
    limit 1
    '''.format(publicAddress = publicAddress)
    df = pd.read_sql(sql, db.engine)
    if len(df) == 0:
        d = {
            'ok': False,
            'reason': 'noUser'
        }
        return d
    else:
        return json.loads(df.to_json(orient='records'))[0]


@app.route('/update_settings', methods=["GET", "POST"])
def update_settings():
    data = flask.request.get_json()
    logger.info(f"update_settings: {data}")
    user = getUser(data)
    pints.postgres.updateSettings(db.engine, user['team_id'], data['user']['settings'])
    ret = {'ok': True}
    return json.dumps(ret), 200, {'ContentType':'application/json'} 

@app.route('/update_secret', methods=["GET", "POST"])
def update_secret():
    data = flask.request.get_json()
    logger.info(f"update_secret: {data}")
    if data['type'] == 'stripe':
        user = getUser(data)
        keyTest = pints.stripe.testKey(data['stripeApiKey'])
        if keyTest['ok']:
            secrets = pints.postgres.getSecrets(db.engine, user['team_id'])
            secrets['stripeApiKey'] = pints.utils.encrypt(data['stripeApiKey'])
            pints.postgres.updateSecrets(db.engine, user['team_id'], secrets)
            jobIds = pints.stripe.getAll(db.engine, user['team_id'])
            keyTest['jobIds'] = jobIds
        return json.dumps(keyTest), 200, {'ContentType':'application/json'} 
    elif data['type'] == 'slack':
        logger.info(f"update_secret slack...")
        user = getUser(data)
        slackAuth = pints.slack.getToken(data['code'])
        logger.info(f"update_secret slackAuth...{slackAuth}")
        if slackAuth.get('access_token', False):
            secrets = pints.postgres.getSecrets(db.engine, user['team_id'])
            slackAuth['access_token'] = pints.utils.encrypt(slackAuth['access_token'])
            secrets['slack'] = slackAuth
            pints.postgres.updateSecrets(db.engine, user['team_id'], secrets)
    return json.dumps({'ok': True}), 200, {'ContentType':'application/json'} 

@app.route('/get_recent_jobs', methods=["GET", "POST"])
def get_recent_jobs():
    data = flask.request.get_json()
    user = getUser(data)
    jobs = pints.postgres.getRecentJobs(db.engine, user['team_id'])
    for key, job in jobs.items():
        logger.info(f'get_recent_jobs job: {job}')
        logger.info(f'get_recent_jobs job: {key}')
        if 'job' in job and 'obj' in job['job']:
            job['jobId'] = str(key)
            logger.info(f'job: {job}')
            job['job']['count'] = pints.postgres.getRawTableCount(db.engine, 
                user['team_id'], job['job']['obj'])
            jobs[key] = job['job']
    return json.dumps({'ok': True, 'jobs': jobs}), 200, {'ContentType':'application/json'}

@app.route('/get_job', methods=["GET", "POST"])
def get_job():
    data = flask.request.get_json()
    job = pints.postgres.getJob(db.engine, data['jobId'])
    if job['ok'] and job['job']['status'] == 'complete' and job['job']['type'] == 'stripe':
        user = getUser(data)
        job['job']['count'] = pints.postgres.getRawTableCount(db.engine, 
                    user['team_id'], job['job']['obj'])
    return json.dumps(job), 200, {'ContentType':'application/json'}

@app.route('/login', methods=["GET", "POST"])
def login():
    data = flask.request.get_json()
    email = data['email']
    if not email:
        d = {
            'ok': False,
            'new': False
        }
        return json.dumps(d), 200, {'ContentType':'application/json'}
    publicAddress = data['publicAddress']
    sql = '''
    SELECT 
    u.id as user_id, 
    u.email, 
    u.details,
    t.details as settings,
    case when s.details ->> 'stripeApiKey' is not null then 1 else 0 end as has_stripe
    FROM 
    public.users as u left join
    public.team_membership as tm on u.id = tm.user_id left join
    public.teams as t on tm.team_id = t.id left join
    public.secrets as s on tm.team_id = s.team_id
    WHERE 
    u.details ->> 'publicAddress' = '{publicAddress}'
    order by u.created_on desc
    limit 1
    '''.format(publicAddress = publicAddress)
    df = pd.read_sql(sql, db.engine)
    if len(df) > 0:
        user = df.details[0]
        user['settings'] = df.settings[0]
        user['hasStripe'] = bool(df.has_stripe[0] > 0)
        d = {
            'ok': True,
            'new': False,
            'user': user
        }
    else:
        userId = pints.postgres.insertUser(db.engine, email, data)
        checkForTeam(db.engine, email, userId)
        d = {
            'ok': True,
            'new': True
        }
    return json.dumps(d), 200, {'ContentType':'application/json'}

@app.route('/get_funders', methods=["GET", "POST"])
def get_funders():
    data = flask.request.get_json()
    sql = '''
    SELECT 
    f.public_id,
    f.name,
    f.domain,
    f.max_loan_amount,
    f.min_loan_amount,
    f.min_annual_revenue,
    f.paper_rank,
    f.focus,
    f.max_mrr_multiple,
    f.loan_type,
    f.payment_details,
    f.saas_focus,
    f.warrants,
    f.region,
    f.personal_guarantor,
    f.days_to_close,
    cb."data"
    FROM 
    public.funders as f left join
    public.clearbit as cb on f."domain" = cb."domain"
    WHERE f.active = '1'
    and f.loan_type != 'Shared Earnings'
    order by f.paper_rank desc
    ;
    '''.format(active = 1)
    df = pd.read_sql(sql, db.engine)
    cols = json.loads(df.dtypes.to_json())
    d = {
        'ok': True, 
        'data': json.loads(df.to_json(orient='records')),
        'columns': cols
    }
    return json.dumps(d), 200, {'ContentType':'application/json'}

@app.route('/update_user_data', methods=["GET", "POST"])
def update_user_data():
    data = flask.request.get_json()
    logger.info(f'update_user_data: {data}')
    publicAddress = data['user'].get('publicAddress', False)
    if not publicAddress:
        d = {
            'ok': False,
            'reason': 'noUser'
        }
        return json.dumps(d), 200, {'ContentType':'application/json'}
    sql = '''
    SELECT 
    u.id as user_id, u.email, u.details, ud.details as user_data
    FROM 
    public.users as u left join
    public.user_data as ud on u.id = ud.user_id
    WHERE 
    u.details ->> 'publicAddress' = '{publicAddress}'
    order by u.created_on desc
    '''.format(publicAddress = publicAddress)
    df = pd.read_sql(sql, db.engine)
    if len(df) == 0:
        d = {
            'ok': False,
            'reason': 'noUser'
        }
        return json.dumps(d), 200, {'ContentType':'application/json'}
    with db.engine.connect() as con:
        d = { "user_id": int(df.user_id[0]), "details": json.dumps(data['userData']) }
        sql = '''
        INSERT INTO public.user_data(user_id, details) 
        VALUES(:user_id, :details)
        ON CONFLICT (user_id) DO UPDATE
        SET details = :details
        '''
        statement = sqlalchemy.sql.text(sql)
        con.execute(statement, **d)
    return json.dumps(d), 200, {'ContentType':'application/json'}

# CREATE TABLE public.applications (
#     id    SERIAL PRIMARY KEY,
#     public_uuid uuid DEFAULT uuid_generate_v1(),
#     user_id integer,
#     created_on timestamp DEFAULT current_timestamp,
#     updated_on timestamp DEFAULT current_timestamp,
#     details JSONB
# );

@app.route('/get_metrics', methods=["GET", "POST"])
def get_metrics():
    data = flask.request.get_json()
    logger.info(f'get_metrics: {data}')
    user = getUser(data)
    logger.info(f'get_metrics user: {user}')
    sql = '''
    select 
    *,
    1 as active
    from 
    "team_{teamId}_stripe".mrr_facts as mrr
    order by mrr.mrr_dt asc
    '''.format(teamId=user['team_id'])
    df = pd.read_sql(sql, db.engine)
    piv = df.pivot_table(index='mrr_month_dt', values=['mrr', 'active', 'churned_mrr'], aggfunc='sum')
    df = json.loads(df.to_json(orient='records'))
    summary = piv.tail(3).to_dict(orient='records')
    logger.info(f"piv summary: {summary}")
    # summary = piv.tail(1).to_dict(orient='records')[0]
    # prevMonth = piv.tail(2).to_dict(orient='records')[1]
    toSlack = {}
    chart = metrics.getMrrChart(df)
    toSlack['mrrChartUrl'] = pints.cabinet.file(chart['filename'])
    chart = metrics.getCustomerChart(df)
    toSlack['customerChartUrl'] = pints.cabinet.file(chart['filename'])
    try:
        toSlack['summary'] = metrics.getSummary(summary)
    except Exception as e:
        logger.error(f"error getting summary: {str(e)}")
        toSlack['summary'] = False
    # logger.info(f'chart: {chart}')
    # app.wsgi_app.add_files('static/', prefix='assets/')
    # chart['title'] = 'MRR'
    logger.info(f"piv summary: {toSlack}")
    # res = pints.slack.push(toSlack)
    # logger.info(f'pints.slack.push: {res}')
    # res = pints.sheets.push(
    #     {
    #         'df': piv.reset_index(),
    #         'spreadsheetId': '1HrMEtpyW7EQZo-QEHDJBjsKCOrEUPF62fBYjNdcPPr0',
    #         'startCell': 'A1',
    #         'sheet': 'Sheet1'
    #     }
    #         )
    # logger.info(f'pints.slack.push: {res}')
    
    ret = {
        'ok': True, 
        'data': df,
        'summary': piv.tail(3).to_dict(orient='records')
        }
    return json.dumps(ret), 200, {'ContentType':'application/json'}

@app.route('/to_slack', methods=["GET", "POST"])
def to_slack():
    data = flask.request.get_json()
    logger.info(f'to_slack: {data}')
    publicId = uuid.uuid4().hex
    return json.dumps({'ok' : True}), 200, {'ContentType':'application/json'}