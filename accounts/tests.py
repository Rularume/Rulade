from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client, Subscription, Customer, Analyst

class EASMProfilesTests(TestCase):
    """
    Test suite for the user profiles and client associations.
    """
    
    def setUp(self):
        """
        Creates base data before running tests.
        """
        # 1. Create EASM Clients
        self.client_1 = Client.objects.create(name="Wayne Enterprises")
        self.client_2 = Client.objects.create(name="Stark Industries")

        # 2. Create Django Base Users (Authentication part)
        self.base_user_bruce = User.objects.create_user(username="bruce", password="superpassword123")
        self.base_user_alfred = User.objects.create_user(username="alfred", password="superpassword123")

    def test_customer_profile_creation(self):
        """
        Test that a Customer profile successfully links a Django User to a single Client.
        """
        customer = Customer.objects.create(
            user=self.base_user_bruce,
            client=self.client_1
        )
        
        self.assertEqual(customer.user.username, "bruce")
        self.assertEqual(customer.client.name, "Wayne Enterprises")

    def test_analyst_profile_creation(self):
        """
        Test that an Analyst profile can manage multiple Clients using the ManyToMany field.
        """
        analyst = Analyst.objects.create(
            user=self.base_user_alfred
        )
        
        # Adding managed clients
        analyst.managed_clients.add(self.client_1, self.client_2)
        
        self.assertEqual(analyst.managed_clients.count(), 2)
        self.assertIn(self.client_1, analyst.managed_clients.all())
        self.assertEqual(analyst.user.username, "alfred")