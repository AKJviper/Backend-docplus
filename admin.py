from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.checks import messages
from .models import *

admin.site.register(UserDoctor)
admin.site.register(AppUser)
admin.site.register(Hospital)
admin.site.register(Patholab)
admin.site.register(Collector)
admin.site.register(Transaction)
admin.site.register(AddRequest)
admin.site.register(Profile)
admin.site.register(Ambulance)
admin.site.register(FaqBlog)
admin.site.register(ContactForm)
admin.site.register(Prescription)