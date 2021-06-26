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
            INSERT INTO {table} (user_id, details) 
            VALUES(:user_id, :details)
            '''
            statement = sqlalchemy.sql.text(sql)
            con.execute(statement, **d)

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
        where t.user_id = {teamId}
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