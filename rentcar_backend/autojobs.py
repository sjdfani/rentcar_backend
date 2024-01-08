from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from datetime import datetime, timedelta
from rentcar_backend.settings import env
from users.models import EmailCode


def expire_email_code():
    EmailCode.objects.filter(
        status=True,
        updated_at__lte=datetime.now(
            tz=pytz.utc) - timedelta(minutes=env('EXPIRE_EMAIL_CODE', cast=int))
    ).update(status=False)
    pass


def main():
    scheduler = BackgroundScheduler(timezone='MST')
    scheduler.add_job(expire_email_code, 'interval', seconds=30)
    scheduler.start()
