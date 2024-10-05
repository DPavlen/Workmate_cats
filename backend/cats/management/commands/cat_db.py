from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("add_group")
        call_command("add_breed")
        call_command("add_cat")