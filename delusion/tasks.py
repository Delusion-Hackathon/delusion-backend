from datetime import timedelta
from celery import shared_task
from celery.utils.log import get_task_logger

from django.utils import timezone
from delusion.company.models import Message, Ticket

logger = get_task_logger(__name__)


@shared_task
def check_ticket_status():
    logger.info("The sample task just ran.")
    
    tickets = Ticket.objects.filter(
        created_at__lte=timezone.now()-timedelta(days=3),
        status=True,
        activity_status=False
    )
    tickets.update(status=False, activity_status=False)
