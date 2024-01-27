from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from datetime import datetime, timedelta
from rentcar_backend.settings import env
from users.models import EmailCode
from reserve.models import Reserve, ReserveStatus


def expire_email_code():
    EmailCode.objects.filter(
        status=True,
        updated_at__lte=datetime.now(
            tz=pytz.utc) - timedelta(minutes=env('EXPIRE_EMAIL_CODE', cast=int))
    ).update(status=False)


def reject_reserve_requests():
    Reserve.objects.filter(
        reserve_status=ReserveStatus.PENDING,
        created_at__lte=datetime.now(
            tz=pytz.utc)-timedelta(hours=env('REJECT_RESERVE_REQUEST_HOURS', cast=int))
    ).update(reserve_status=ReserveStatus.REJECTED)


def main():
    scheduler = BackgroundScheduler(timezone='MST')
    scheduler.add_job(expire_email_code, 'interval', seconds=30)
    scheduler.add_job(reject_reserve_requests, 'interval', seconds=30)
    scheduler.start()
