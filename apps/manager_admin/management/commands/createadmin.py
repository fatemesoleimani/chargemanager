from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = "Create initial admin (superuser) account"

    def handle(self, *args, **options):
        username = getattr(settings, "ADMIN_USERNAME", None)
        password = getattr(settings, "ADMIN_PASSWORD", None)

        if not username or not password:
            self.stdout.write(
                self.style.ERROR(
                    "ADMIN_USERNAME or ADMIN_PASSWORD is not set in settings."
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Admin user '{username}' already exists."
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin user '{username}' created successfully."
            )
        )
