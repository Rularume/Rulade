from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime, timedelta
from django.utils.translation import gettext_lazy as _

BOOLEAN_CHOICES = ((True, _('Yes')),(False, _('No')),)

class Client(models.Model):
    """
    Represents the main entity, the company or organization being audited.
    
    This model serves as the central anchor for all EASM (External Attack 
    Surface Management) assets. Domains, IPs, and vulnerabilities will 
    ultimately link back to a Client.
    """
    name = models.CharField(max_length=255, verbose_name=_("Client Name"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Creation Date"))
    is_active = models.BooleanField(default=True, choices=BOOLEAN_CHOICES, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

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
    class PlanChoices(models.TextChoices):
        BASIC = 'basic', _('Basic')
        PRO = 'pro', _('Pro')
        ENTERPRISE = 'enterprise', _('Enterprise')

    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='subscription',verbose_name=_("Client"))
    plan = models.CharField(max_length=20, choices=PlanChoices.choices, default=PlanChoices.BASIC,verbose_name=_("Plan"))
    start_date = models.DateTimeField(default=localtime, verbose_name=_("Start Date"))
    expiration_date = models.DateTimeField(default=localtime()+timedelta(days=365), verbose_name=_("Expiration Date"))
    
    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def is_active(self):
        if self.expiration_date:
            return localtime() <= self.expiration_date
        return True
    
    def __str__(self):
        return f"{self.client.name} - {self.get_plan_display()}"

class Customer(models.Model):
    """
    Profile for standard users belonging to a single client organization.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile',verbose_name=_("Django User"))
    client = models.ForeignKey(Client, on_delete=models.CASCADE,verbose_name=_("Primary Client Organization"))

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return f"{self.user.username} ({self.client.name})"

class Analyst(models.Model):
    """ 
    Profile for internal security experts managing multiple clients.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='analyst_profile',verbose_name=_("Django User"))
    managed_clients = models.ManyToManyField(Client, blank=True, related_name='managed_by_analysts',verbose_name=_("Managed Clients"))

    class Meta:
        verbose_name = _("Analyst")
        verbose_name_plural = _("Analysts")

    def __str__(self):
        return f"{self.user.username}"