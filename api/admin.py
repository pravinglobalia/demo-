from django.contrib import admin
from .models import User, Zone, Notification, Activity, Score, Invitation,Package,Purchasepackage


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','first_name','last_name','is_superuser','phone','primary_user']


class ZoneDisplay(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'description']


class NotificationDisplay(admin.ModelAdmin):

    list_display = ['id', 'to_user', 'name',
                    'description', 'zone', 'from_user']

    # def zone_description(self,obj):
    #     return obj.zone.description
    # def zone_name(self,obj):
    #     return obj.zone.name


class ActivityDisplay(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']


class ScoreDisplay(admin.ModelAdmin):
    list_display = ['id', 'score', 'hours',
                    'minitus', 'seconds', 'user', 'activity_name']

    def activity_name(self, obj):
        return obj.activity.name


class InvitationDisplay(admin.ModelAdmin):
    list_display = ['id', 'from_to', 'email']

class PackageDisplay(admin.ModelAdmin):
    list_display = ['id','name','price','account','activity']

class PurchasepackageDisplay(admin.ModelAdmin):
    list_display = ['id','user','package_name']

    def package_name(self,obj):
        return obj.package.name

admin.site.register(User, UserAdmin)
admin.site.register(Zone, ZoneDisplay)
admin.site.register(Score, ScoreDisplay)
admin.site.register(Activity, ActivityDisplay)
admin.site.register(Invitation, InvitationDisplay)
admin.site.register(Notification, NotificationDisplay)
admin.site.register(Package,PackageDisplay)
admin.site.register(Purchasepackage,PurchasepackageDisplay)
