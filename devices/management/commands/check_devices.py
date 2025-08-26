from django.core.management.base import BaseCommand
from devices.utils import update_device_status

class Command(BaseCommand):
    help = 'Check and update status of all network devices'

    def handle(self, *args, **options):
        self.stdout.write('Checking device status...')
        update_device_status()
        self.stdout.write(
            self.style.SUCCESS('Successfully updated device statuses')
        )
