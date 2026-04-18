from django.core.management.commands.makemessages import Command as BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        options["no_location"] = True
        super().handle(*args, **options)