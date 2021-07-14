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
    # hourlyJob = scheduler.add_job(func=runHourly, trigger='cron', minute=16, second=0)
    hourlyJob = scheduler.add_job(runHourly, trigger='interval', seconds=10)
    # weeklyJob = scheduler.add_job(func=runWeekly, kwargs={'engine': engine}, trigger='cron', day_of_week='mon', hour=8, minute=30, second=0)
    # monthlyJob = scheduler.add_job(func=runMonthly, kwargs={'engine': engine}, trigger='cron', day=1, hour=8, minute=30, second=0)
    scheduler.start()

def runHourly():
    logger.info(f'runHourly...')
    with app.app_context():
        teams = pints.postgres.getTeams(db.engine)
        for team in teams:
            settings = pints.postgres.getSettings(db.engine, team['id'])
            jobUuids = fullRefresh(db.engine, team['id'])
            details = {
                'status': 'pending',
                'dependencies': jobUuids,
                'type': 'sendNotifications'
            }
            jobUuid = uuid.uuid4().hex
            targetId = pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
            messageId = pints.postgres.addMessage(db.engine, team['id'], targetId, details)
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

# def runScheduledJobs(engine, teamId):
#     dt = datetime.datetime.utcnow()
#     schedule = False
#     lastRunDt = False
#     daysSinceLastRun = 0
#     destinations = []
#     if dt.day == 1:
#         schedule = 'monthly'
#     elif dt.weekday() == 0:
#         schedule = 'weekly'
#     if schedule:
#         lastRunDt = pints.postgres.getMaxJobRun(engine, teamId, schedule)
#         logger.info(f'lastRunDt: {lastRunDt}')
#     if lastRunDt:
#         daysSinceLastRun = (dt - lastRunDt).days
#     if daysSinceLastRun > 0:
#         settings = pints.postgres.getSettings(engine, teamId)
#         if settings:
#             for key, value in settings['notifications'][schedule].items():
#                 if value:
#                     destinations.append(key)
#     for destination in destinations:
#         logger.info(f'destination: {destination}')
#         message = {
#             'type': destination,
#             'schedule': schedule
#             }
#         jobUuid = uuid.uuid4().hex
#         targetId = pints.postgres.addJob(engine, teamId, message, jobUuid)
#         pints.postgres.addMessage(engine, teamId, targetId, message)
        # TODO run destination

def getScheduledJobs(schedule):
    # TODO get time
    # run stripe
    # run dbt
    # run alerts
    # get time
    # if time is on the weekly run, run weekly
    # if time is on the monthly run, run monthly
    return
    
def do_some_work(jobRow):
    logger.info(f'do_some_work... {jobRow}')
    if random.choice([True, False]):
        logger.info(f'do_some_work failed... {jobRow}')
        raise Exception
    else:
        logger.info(f'do_some_work SUCCESS... {jobRow}')

def checkQueue():
    logger.info(f'checkQueue...')
    jobRow, queueRow = pints.postgres.getMessages(db.engine)
    logger.info(f'checkQueue jobRow: {jobRow}')
    if jobRow:
        try:
            do_some_work(jobRow)
            pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'complete', None)
        except Exception as e:
            pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'failed', str(e))
            # if we want the job to run again, insert a new item to the message queue with this job id
            # con.execute(sql, (queue_item['target_id'],))
    else:
        logger.info(f'no jobs to run...')
    return True