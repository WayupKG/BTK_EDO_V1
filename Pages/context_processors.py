from django.utils import timezone

from Documents.models import MovementOfDocument, Document
from Notification.models import Notification


def getting_info(request):
    try:
        inbox_count = MovementOfDocument.objects.filter(responsible=request.user.profile, view='Не просмотрено').count()
        notification_count = Notification.objects.filter(user=request.user.profile, view='Не просмотрено').count()
        process_count = MovementOfDocument.in_process.filter(responsible=request.user.profile).count()
        done_count = MovementOfDocument.done.filter(responsible=request.user.profile).count()
        not_executed_count = MovementOfDocument.not_executed.filter(responsible=request.user.profile).count()
    except AttributeError:
        inbox_count = 0
        notification_count = 0
        process_count = 0
        done_count = 0
        not_executed_count = 0
    date_now = timezone.now()

    return locals()



