from django.contrib import admin
from .models import Client, Subscription, Customer, Analyst

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('client', 'plan', 'start_date', 'expiration_date', 'is_currently_active')
    list_filter = ('plan',)
    
    def is_currently_active(self, obj):
        return obj.is_active()
    
    is_currently_active.boolean = True 
    is_currently_active.short_description = "Active?"

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'client')
    search_fields = ('user__username', 'client__name')

class AnalystAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

admin.site.register(Client)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Analyst, AnalystAdmin)