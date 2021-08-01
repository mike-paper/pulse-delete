import pints
from logger import logger
import datetime
import random
import sqlalchemy
import json
import pytz
import uuid
import os
from metrics import metrics
from app import app, db


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

PAPER_DO_NOT_START_SCHEDULER = int(os.environ.get('PAPER_DO_NOT_START_SCHEDULER', 0)) > 0


def startScheduler(engine):
    logger.info(f'startScheduler? {(not PAPER_DO_NOT_START_SCHEDULER)}')
    if PAPER_DO_NOT_START_SCHEDULER:
        # runWeekly()
        logger.info(f'not starting scheduler...')
        return False
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
        'max_instances': 3,
        'misfire_grace_time': 60
    }
    scheduler = BackgroundScheduler(
        # daemon=True, 
        jobstores=jobstores, 
        executors=executors, 
        job_defaults=job_defaults, 
        timezone=pytz.utc
        )
    scheduler.start()
    checkQueueJob = scheduler.add_job(checkQueue, trigger='interval', seconds=60)
    # testSchedJob = scheduler.add_job(testSched, trigger='interval', seconds=10)
    hourlyJob = scheduler.add_job(func=runHourly, trigger='cron', minute=45, second=30)
    weeklyJob = scheduler.add_job(func=runWeekly, kwargs={'engine': engine}, trigger='cron', day_of_week='mon', hour=8, minute=30, second=0)
    return True
    
    

def runHourly():
    logger.info(f'runHourly...')
    with app.app_context():
        teams = pints.postgres.getTeams(db.engine)
        # teams = [team for team in teams if team['id'] == 5]
        for team in teams:
            logger.info(f"team {team['id']}...")
            jobUuids = fullRefresh(db.engine, team['id'])
            settings = pints.postgres.getSettings(db.engine, team['id'])
            if settings['notifications'].get('alerts', {}).get('slack', False):
                dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')
                details = {
                    'status': 'pending',
                    'dependencies': jobUuids,
                    'type': 'sendNotifications',
                    'maxCreatedOn': dt,
                    'maxCanceledOn': dt,
                }
                jobUuid = uuid.uuid4().hex
                targetId = pints.postgres.addJob(db.engine, team['id'], details, jobUuid)
                messageId = pints.postgres.addMessage(db.engine, team['id'], targetId, details, jobUuid)
                logger.info(f'runHourly messageId... {messageId}')
        return True

def runWeekly():
    teams = pints.postgres.getTeams(db.engine)
    # teams = [team for team in teams if team['id'] == 5]
    for team in teams:
        runWeeklyTeam(db.engine, team['id'])

def runWeeklyTeam(engine, teamId):
    logger.info(f'runWeeklyTeam... {teamId}')
    settings = pints.postgres.getSettings(engine, teamId)
    logger.info(f'runWeeklyTeam settings... {settings}')
    if settings['notifications'].get('weekly', {}).get('slack', False):
        toSlack = metrics.getSlackMsg(engine, teamId)
        slackInfo = pints.postgres.getSlackInfo(engine, teamId)
        pints.slack.weekly(toSlack, slackInfo['bot_token'])
    return True

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
    logger.info(f'testSched...')
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
                    lastJob = pints.postgres.getLastJob(db.engine, jobRow['team_id'], 'sendNotifications')
                    if not lastJob:
                        logger.info(f'adding first lastJob...')
                        dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')
                        details = {
                            'maxCreatedOn': dt,
                            'maxCanceledOn': dt,
                            'type': 'sendNotifications',
                            'status': 'complete',
                        }
                        jobUuid = uuid.uuid4().hex
                        pints.postgres.addJob(db.engine, jobRow['team_id'], details, jobUuid)
                        lastJob = pints.postgres.getLastJob(db.engine, jobRow['team_id'], 'sendNotifications')
                    logger.info(f'sendNotifications lastJob: {lastJob}')
                    alerts = pints.postgres.getAlerts(db.engine, jobRow['team_id'], lastJob)
                    logger.info(f'sendNotifications alerts: {alerts}')
                    for alert in alerts:
                        logger.info(f'sendNotifications alert: {alert}')
                        # TODO send alert
                        # pints.postgres.updateMessage(db.engine, alert['message_id'], {'status': 'sent'})
                        settings = pints.postgres.getSettings(db.engine, jobRow['team_id'])
                        d = {
                            'email': alert['email'],
                            'mrr': alert['mrr'],
                            'prev_mrr': alert['prev_mrr'],
                            'msg': f"Originally signed up on {alert['customer_created_on2']} ({alert['created_days_ago']} days to convert)",
                            'slackChannel': settings['notifications']['slackChannel']
                        }
                        slackInfo = pints.postgres.getSlackInfo(db.engine, jobRow['team_id'])
                        if alert['alert_type'] == 'canceled':
                            pints.slack.churnAlert(d, slackInfo['bot_token'])
                        else:
                            pints.slack.customerAlert(d, slackInfo['bot_token'])
                    dt = datetime.datetime.utcnow().isoformat().replace('T', ' ')
                    details = {
                        'maxCreatedOn': dt,
                        'maxCanceledOn': dt,
                    }
                    pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'complete', None, details)
            except Exception as e:
                logger.error(f'checkQueue error: {str(e)}')
                pints.postgres.updateJobStatus(db.engine, queueRow['target_id'], 'error', str(e), None)
                raise e
                # if we want the job to run again, insert a new item to the message queue with this job id
                # con.execute(sql, (queue_item['target_id'],))
        else:
            logger.info(f'no jobs to run...')
            gettingJobs = False
        return True