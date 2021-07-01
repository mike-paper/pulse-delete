import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, String, inspect
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.elements import quoted_name
import json
import uuid
from logger import logger
import pints

def insertRows(engine, table, rows, teamId):
    with engine.connect() as con:
        for row in rows:
            d = {
                "team_id": teamId,
                "details": json.dumps(row)
                }
            sql = f'''
            INSERT INTO {table} (team_id, details) 
            VALUES(:team_id, :details)
            '''
            statement = sqlalchemy.sql.text(sql)
            res = con.execute(statement, **d)

def getMaxRecord(engine, table, teamId):
    with engine.connect() as con:
        sql = f'''
        select max(t.details ->> 'created') 
        from "public".{table} as t
        where t.team_id = {teamId}
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()[0]
        return res

def deleteRows(engine, table, teamId):
    with engine.connect() as con:
        sql = f'''
        delete from "public".{table} as t
        where t.team_id = {teamId}
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement)
        return res


def insertUser(engine, email, data):
    with engine.connect() as con:
        d = { "email": email, "details": json.dumps(data) }
        sql = '''
        INSERT INTO users(email, details) 
        VALUES(:email, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        userId = res.fetchone()[0]
        return userId

def insertTeam(engine, domain):
    with engine.connect() as con:
        teamUuid = uuid.uuid4().hex
        d = { "public_uuid": teamUuid, "domain": domain, "details": json.dumps({}) }
        sql = '''
        INSERT INTO teams(public_uuid, domain, details) 
        VALUES(:public_uuid, :domain, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        teamId = res.fetchone()[0]
        return teamId

def insertTeamMember(engine, teamId, userId):
    with engine.connect() as con:
        teamMembershipUuid = uuid.uuid4().hex
        d = { 
            "team_id": teamId,
            "user_id": userId,
            "public_uuid": teamMembershipUuid, 
            "role": "admin", 
            "details": json.dumps({}) 
            }
        sql = '''
        INSERT INTO team_membership(team_id, user_id, public_uuid, role, details) 
        VALUES(:team_id, :user_id, :public_uuid, :role, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        teamMembershipId = res.fetchone()[0]
        return teamMembershipId

def createSecrets(engine, teamId):
    with engine.connect() as con:
        d = { 
            "team_id": teamId,
            "details": json.dumps({}) 
            }
        sql = '''
        INSERT INTO public.secrets(team_id, details) 
        VALUES(:team_id, :details)
        RETURNING id;
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        secretId = res.fetchone()[0]
        return secretId

def getSecrets(engine, teamId):
    with engine.connect() as con:
        sql = f'''
        select details
        from "public".secrets as s
        where s.team_id = {teamId}
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            logger.info(f'no secrets, creating...')
            createSecrets(engine, teamId)
            return {}
        return res[0]

def updateSecrets(engine, teamId, details):
    with engine.connect() as con:
        d = { 
            "details": json.dumps(details),
            "team_id": teamId,
            }
        sql = '''
        UPDATE public.secrets
        SET details = :details
        WHERE team_id = :team_id
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement, **d)
        return True

def getStripeApiKey(engine, teamId):
    with engine.connect() as con:
        sql = f'''
        select details
        from "public".secrets as s
        where s.team_id = {teamId}
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            return False
        res = res[0]
        if res.get('stripeApiKey', False):
            return pints.utils.decrypt(res['stripeApiKey'])
        return False

def updateJob(engine, teamId, jobId, jobUuid, details):
    logger.info(f'updateJob {jobId} {jobUuid}...')
    with engine.connect() as con:
        d = { 
            "details": json.dumps(details),
            "team_id": teamId,
            "job_id": jobId,
            "public_uuid": jobUuid,
            }
        
        if jobId:
            sql = '''
            UPDATE public.jobs
            SET details = :details
            WHERE id = :job_id
            '''
            statement = sqlalchemy.sql.text(sql)
            res = con.execute(statement, **d)
            return jobId
        else:
            sql = '''
            INSERT INTO public.jobs(team_id, public_uuid, details) 
            VALUES(:team_id, :public_uuid, :details)
            RETURNING id;
            '''
            statement = sqlalchemy.sql.text(sql)
            logger.info(f'updateJob statement {statement}...')
            res = con.execute(statement, **d).fetchone()
            logger.info(f'updateJob res {res}...')
            return res[0]

def getJob(engine, jobUuid):
    with engine.connect() as con:
        sql = f'''
        select details, updated_on
        from public.jobs as j
        where public_uuid = '{jobUuid}'
        order by id desc
        limit 1
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            return {'ok': False}
        ret = res[0]
        ret['updated_on'] = res[1].timestamp()
        return {'ok': True, 'job': ret}

def getRawTableCount(engine, teamId, table):
    with engine.connect() as con:
        schema = 'public'
        sql = f'''
        select
        count(1) as ct
        from "{schema}"."stripe_{table}"
        where team_id = {teamId}
        '''
        statement = sqlalchemy.sql.text(sql)
        res = con.execute(statement).fetchone()
        if not res:
            return {'ok': False}
        return res[0]

def getRawTableCounts(engine, teamId):
    schema = 'public'
    tables = ['customers', 'coupons']
    for index, table in enumerate(tables):
        sql += f'''
        select
        '{table}' as "table",
        'raw' as "type",
        count(1) as ct
        from "{schema}"."stripe_{table}"
        where team_id = {teamId}
        '''
        if index < len(tables)-1:
            sql+= 'union all\n'
    logger.info(f'getTableCounts {sql}...')
    df = pd.read_sql(sql, engine)
    df = df.to_json(date_format = 'iso', orient='values', default_handler=str)
    return json.loads(df)

def getDbtTableCounts(engine, teamId):
    tables = ['customers', 'subscriptions', 'mrr_facts']
    sql = ''
    schema = f'team_{teamId}_stripe'
    for index, table in enumerate(tables):
        sql += f'''
        select
        '{table}' as "table",
        'modeled' as "type",
        count(1) as ct
        from "{schema}"."{table}"
        '''
        if index < len(tables)-1:
            sql+= 'union all\n'
    df = pd.read_sql(sql, engine)
    df = df.to_json(date_format = 'iso', orient='values', default_handler=str)
    return json.loads(df)

def getJobSummary(engine, teamId):
    sql = f'''
    select 
	team_id,
	details ->> 'obj' as obj,
	details ->> 'status' as "status",
	count(1) as ct,
	max(j.id) as id
	from "public".jobs as j
	where 1=1
	and team_id = {teamId}
	group by
	1, 2, 3
    '''
    df = pd.read_sql(sql, engine)
    return df

def getRecentJobs(engine, teamId):
    sql = f'''
    with jobs2 as (
        select 
        details ->> 'obj' as obj,
        count(1) as ct,
        max(j.id) as id
        from "public".jobs as j
        where details ->> 'status' = 'complete'
        and team_id = {teamId}
        group by
        1
    )

    select 
    j.public_uuid::text as public_uuid,
    details as job
    from jobs2 as j2 inner join
    "public".jobs as j on j.id = j2.id
    '''
    df = pd.read_sql(sql, engine)
    df = df.set_index('public_uuid')
    df = df.to_dict(orient='index')
    return df