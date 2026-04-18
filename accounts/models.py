from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime, timedelta

class Client(models.Model):
    """
    Represents the main entity, the company or organization being audited.
    
    This model serves as the central anchor for all EASM (External Attack 
    Surface Management) assets. Domains, IPs, and vulnerabilities will 
    ultimately link back to a Client.
    """
    name = models.CharField(max_length=255, verbose_name="Client Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return self.name

class Subscription(models.Model):
    """
    Manages the billing tier, technical limitations, and validity period for a specific Client.
    Attributes:
        client (OneToOneField): The associated client.
        plan (CharField): The tier of the subscription (e.g., basic, pro, enterprise).
        max_assets (IntegerField): The maximum number of assets this client can scan.
        start_date (DateTimeField): The exact date and time the subscription becomes active.
        expiration_date (DateTimeField): The date and time the subscription ends (if null, the subscription is lifetime).
    """
    PLAN_CHOICES = (
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    )
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basic')
    start_date = models.DateTimeField(default=localtime, verbose_name="Start Date")
    expiration_date = models.DateTimeField(default=localtime()+timedelta(days=365),verbose_name="Expiration Date")
    
    def is_active(self):
        """ Checks if the subscription is still valid at the current time."""
        if self.expiration_date:
            return localtime() <= self.expiration_date
        return True
    
    def __str__(self):
        return f"{self.client.name} - {self.get_plan_display()}"

class Customer(models.Model):
    """
    Profile for standard users belonging to a single client organization.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile',verbose_name="Django User")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.client.name})"

class Analyst(models.Model):
    """ 
    Profile for internal security experts managing multiple clients.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analyst_profile',verbose_name="Django User")
    managed_clients = models.ManyToManyField(Client, blank=True, related_name='managed_by_analysts',verbose_name="Managed Clients")

    def __str__(self):
        return f"{self.user.username}"