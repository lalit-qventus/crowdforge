from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.tasks.models import Task, TaskStatus


class Command(BaseCommand):
    help = "Expire task claims that have passed their claim_expires_at deadline"

    def handle(self, *args, **options):
        now = timezone.now()
        expired = Task.objects.filter(
            claim_expires_at__lt=now,
            status=TaskStatus.CLAIMED,
        ).update(
            status=TaskStatus.OPEN,
            assignee=None,
            claimed_at=None,
            claim_expires_at=None,
        )
        self.stdout.write(f"Expired {expired} task claim(s)")
