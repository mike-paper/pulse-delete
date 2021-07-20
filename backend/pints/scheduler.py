import pints
from logger import logger
import datetime
import random
import sqlalchemy
import json
import pytz
import uuid
from app import app, db



from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def startScheduler(engine):
    scheduler = False
    apses = pints.postgres.getSchedulerRow(engine)
    logger.info(f'apses... {apses}')
    if apses:
        pints.postgres.truncateTable(engine, 'aps_scheduler')
    logger.info(f'starting aps...')
    jobstores = {
    'default': SQLAlchemyJobStore(engine=engine, tablename='aps_scheduler', tableschema='public')
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 1,
        'misfire_grace_time': 60
    }
    scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=pytz.utc)
    checkQueueJob = scheduler.add_job(checkQueue, trigger='interval', seconds=60)
    # checkQueueJob = scheduler.add_job(testSched, trigger='interval', seconds=10)
    hourlyJob = scheduler.add_job(func=runHourly, trigger='cron', minute=19, second=20)
    # hourlyJob = scheduler.add_job(runHourly, trigger='interval', seconds=10)
    # weeklyJob = scheduler.add_job(func=runWeekly, kwargs={'engine': engine}, trigger='cron', day_of_week='mon', hour=8, minute=30, second=0)
    # monthlyJob = scheduler.add_job(func=runMonthly, kwargs={'engine': engine}, trigger='cron', day=1, hour=8, minute=30, second=0)
    scheduler.start()

def runHourly():
    logger.info(f'runHourly...')
    with app.app_context():
        teams = pints.postgres.getTeams(db.engine)
        # teams = [team for team in teams if team['id'] == 4]
        for team in teams:
            logger.info(f"team {team['id']}...")
            settings = pints.postgres.getSettings(db.engine, team['id'])
            jobUuids = fullRefresh(db.engine, team['id'])
            details = {
                'status': 'pending',
                'dependencies': jobUuids,
                'type': 'sendNotifications'
            }
            jobUuid = uuid.uuid4().hex
            targetId = pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
            messageId = pints.postgres.addMessage(db.engine, team['id'], targetId, details, jobUuid)
            logger.info(f'runHourly messageId... {messageId}')
            # TODO check if alert / notifications need to be sent
        return True

def runWeekly(engine):
    teams = pints.postgres.getTeams(engine)
    for team in teams:
        runWeeklyTeam(engine, team['id'])

def runWeeklyTeam(engine, teamId):
    logger.info(f'runWeeklyTeam... {teamId}')
    settings = pints.postgres.getSettings(engine, teamId)
    logger.info(f'runWeeklyTeam settings... {settings}')

def runMonthly(engine):
    return True

def fullRefresh(engine, teamId):
    logger.info(f'fullRefresh...')
    jobUuids = pints.stripe.getAll(engine, teamId)
    logger.info(f'fullRefresh jobUuids: {jobUuids}')
    return jobUuids
    
def do_some_work(jobRow):
    logger.info(f'do_some_work... {jobRow}')
    if random.choice([True, False]):
        logger.info(f'do_some_work failed... {jobRow}')
        raise Exception
    else:
        logger.info(f'do_some_work SUCCESS... {jobRow}')

def testSched():
    # print('testSched...')
    team = {'id': 5, 'domain': 'trypaper.io'} # trypaper.io team
    logger.info(f'testSched...')
    depJob = uuid.uuid4().hex
    details = {
        'status': 'complete',
        'dependencies': [],
        'type': 'stripe'
    }
    depJob = uuid.uuid4().hex
    pints.postgres.addJob(db.engine, team['id'], details, depJob)
    details = {
        'status': 'pending',
        'dependencies': [depJob],
        'type': 'sendNotifications'
    }
    jobUuid = uuid.uuid4().hex
    targetId = pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
    messageId = pints.postgres.addMessage(db.engine, team['id'], targetId, details, jobUuid)
    logger.info(f'testSched... {targetId} {jobUuid}')
    return True

def checkQueue():
    logger.info(f'checkQueue...')
    gettingJobs = True
    while gettingJobs:
        jobRow, queueRow = pints.postgres.getMessages(db.engine)
        if jobRow:
            logger.info(f"checkQueue jobRow: {jobRow}")
            try:
                if jobRow['details']['type'] == 'sendNotifications':
                    logger.info(f'sendNotifications...')
                    d = {
                        'name': 'John Doe',
                        'email': 'jame@doordash.com',
                        'mrr': '$100.00',
                        'msg': 'Thanks for the $100.00'
                    }
                    pints.slack.newCustomer(d)
                pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'complete', None)
            except Exception as e:
                logger.error(f'checkQueue error: {str(e)}')
                pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'error', str(e))
                # raise e
                # if we want the job to run again, insert a new item to the message queue with this job id
                # con.execute(sql, (queue_item['target_id'],))
        else:
            logger.info(f'no jobs to run...')
            gettingJobs = False
        return True