from django.contrib import admin
from register.models import Profile
from django.contrib.auth.models import Group


admin.site.site_header = 'Admin Pure Beurre' # Change page title
admin.site.register(Profile)
admin.site.unregister(Group) # delete group 