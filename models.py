from django import forms
from django.core.checks import messages
from django.db import models
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.core.validators import MaxLengthValidator, RegexValidator
from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from datetime import datetime
from django.db.models.fields import related
from rest_framework import status, permissions
import uuid
from django.db.models import Q, query
from django.template.defaultfilters import default, slugify

from django.db.models.signals import post_save
from django.dispatch import receiver


class ThreadManager(models.Manager):
    def by_user(self, user):
        
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): 
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False


User_Type= [
    ('P', 'User'),
    ('D', 'Doctor'),
    ('S', 'PSP')
    ]

class Profile(models.Model):
    userprofile= models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=30, blank=True, default="")
    profile_name=  models.CharField(max_length=50, blank=True, default="") 
    user_type = models.CharField(max_length=30, blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.id:
            self.user_name = self.userprofile.username
            self.profile_name = self.userprofile.first_name +" "+ self.userprofile.last_name
        super(Profile, self).save(*args, **kwargs)
         
    def __str__(self):
                return "%s %s" % (str(self.pk), self.userprofile.username)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(userprofile=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




class AppUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default="")
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    Name = models.CharField(max_length=50, error_messages={'Incomplete':"Enter your Full Name"}, default="")
    phone = models.CharField(max_length=10, error_messages={'incomplete': 'Enter a phone Number.'}, default="")
    dob= models.CharField(max_length=12, default="")
    state = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    address = models.TextField(max_length=100, default="")
    profileImg = models.ImageField(null=True, blank=True, upload_to="images/user")
    zip_code = models.CharField(max_length=6,error_messages={'incomplete': 'Enter a ZIP code.'}, default="")
    date = models.DateField(auto_now=True)
    friends = models.ManyToManyField(User , blank=True, related_name='users_doctor', default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(AppUser, self).save(*args, **kwargs)
         
    def __str__(self):
                return "%s %s" % (str(self.pk), self.Name)


    


# validators=[RegexValidator(r'^[0-9]{10}+$', 'Enter a valid Phone Number.')]
# validators=[RegexValidator(r'^[0-9]{6}+$', 'Enter a valid zip code.')]

    # def save(self, *args, **kwargs):
    #     # self.full_name = User.get_full_name()
    #     self.dob = datetime.strptime(self.dob, "%Y-%m-%d").date()
    #     super(AppUser, self).save(*args, **kwargs)
    


class UserDoctor(models.Model):
    userdoc = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default="")
    Name = models.CharField(max_length=50, error_messages={'Incomplete':"Enter your Full Name"}, default="")
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    phone = models.CharField(max_length=10, error_messages={'incomplete': 'Enter a phone Number.'}, default="")
    dob= models.CharField(max_length=12, default="")
    state = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    address = models.TextField(max_length=100, default="")
    profileImg = models.ImageField(null=True, blank=True, upload_to="images/doctor", default="")
    zip_code = models.CharField(max_length=6,error_messages={'incomplete': 'Enter a ZIP code.'}, default="")
    desc = models.TextField(blank=True, null=True,  default="")
    spcl = models.CharField(max_length=100, blank=True, null=True,  default="")
    consult_fees = models.IntegerField(default=0, null=True)
    apnt_fees = models.IntegerField(blank=True, null=True,  default=0)
    Time_from = models.TimeField(null=True, blank=True,  default="00:00:00.000000")
    Time_to = models.TimeField(null=True, blank=True,  default="00:00:00.000000")
    availability = models.BooleanField(default="")
    clinic_add = models.CharField(max_length=300, default="")
    date = models.DateField(auto_now=True)
    friends = models.ManyToManyField(User , blank=True, related_name='doctors_patient')

    default_permissions = ()
    permissions = ("is_doctor", "is a doctor")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.userdoc)
        super(UserDoctor, self).save(*args, **kwargs)
        
    def __str__(self):
        return "%s %s" % (str(self.pk), self.Name)

class Ambulance(models.Model):
    useramb = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default="")
    Name = models.CharField(max_length=50, error_messages={'Incomplete':"Enter your Full Name"}, default="")
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    phone = models.CharField(max_length=10, error_messages={'incomplete': 'Enter a phone Number.'}, default="")
    vehicle_reg= models.CharField(max_length=12, default="")
    state = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    address = models.TextField(max_length=400, default="")
    profileImg = models.ImageField(null=True, blank=True, upload_to="images/ambulance")
    zip_code = models.CharField(max_length=6,error_messages={'incomplete': 'Enter a ZIP code.'}, default="")
    owner_name= models.TextField(blank=True, null=True,  default="")
    wic_charge = models.IntegerField(default=0, null=True)
    availability = models.BooleanField(default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.userdoc)
        super(Ambulance, self).save(*args, **kwargs)
        
    def __str__(self):
        return "%s %s" % (str(self.Name), self.vehicle_reg)

# class PatDoctor(models.Model):
#     first  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='PatDoc_first')
#     slug = models.SlugField(max_length = 250, null = True, blank = True)
#     second = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='PatDoc_second')
#     doctor =  models.ForeignKey(UserDoctor, on_delete=models.CASCADE)
#     user_pat =models.ForeignKey(AppUser, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now=True)

#     objects= ThreadManager()

#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.id)
#         super(PatDoctor, self).save(*args, **kwargs)
    
#     def __str__(self):
#         return "%s %s" % ((self.first), self.second)
    

# class Messages(models.Model):
#     thread = models.ForeignKey(PatDoctor, on_delete=models.CASCADE)
#     slug = models.SlugField(max_length = 250, null = True, blank = True)
#     problem = models.TextField(null=True, blank=True)
#     message = models.TextField(default="")
#     image = models.ImageField(null = True, blank=True, upload_to="images/messages")
#     file = models.FileField(null=True, blank=True, upload_to="files/")
#     date = models.DateTimeField(auto_now=True)


#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.thread)
#         super(Messages, self).save(*args, **kwargs)
    
#     def __str__(self):
#         return "%s %s" % (self.pk, self.thread)
    


class Hospital(models.Model):
    userhospital = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True,  default="")
    name = models.CharField(max_length=100,  default="")
    state = models.CharField(max_length=50,  default="")
    city = models.CharField(max_length=50,  default="")
    profileImg = models.ImageField(null=True, blank=True, upload_to="images/hospitals")
    address = models.TextField(max_length=300,  default="")
    total_bes = models.IntegerField(default=0)
    available_bed = models.IntegerField(default=0)
    booking_price = models.IntegerField(default=0)
    availability = models.BooleanField(default="", blank=True, null=True)
    friends = models.ManyToManyField(User , blank=True, related_name='hospitals_patient')

    class Meta:
       ordering = ('-id', )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.userhospital)
        super(Hospital, self).save(*args, **kwargs)

    def __str__(self):
       return self.name


class Patholab(models.Model):
    userpatho = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    name = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, error_messages={'incomplete': 'Enter a phone Number.'}, default="")
    test_price = models.JSONField(null=True, blank=True)
    profileImg = models.ImageField(null=True, blank=True, upload_to="images/Patholab")
    address = models.TextField(max_length=300, default="")
    sample = models.JSONField(null=True, blank=True)
    friends = models.ManyToManyField(User , blank=True, related_name='patholabs_patient')
    availability = models.BooleanField(default="", blank=True, null=True)

    class Meta:
       ordering = ('-id', )
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.userpatho)
        super(Patholab, self).save(*args, **kwargs)

    def __str__(self):
       return self.name

    # json=username, testname, price, reportgiven


class Collector(models.Model):
    usercollector = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    name = models.CharField(max_length=50,  default="")
    state = models.CharField(max_length=50,  default="")
    phone = models.CharField(max_length=10, error_messages={'incomplete': 'Enter a phone Number.'},blank=True, null=True, default="")
    city = models.CharField(max_length=50,  default="")
    profileImg = models.ImageField(null=True, blank=True, upload_to="images/collector")
    patholab = models.ManyToManyField(Patholab, null=True, blank=True)
    sample_collected = models.JSONField( default={})
    total_amount = models.IntegerField(blank=True, null=True,  default=0)
    availability = models.BooleanField(default="", blank=True, null=True)
    date = models.DateField(auto_now=True)

    class Meta:
       ordering = ('-id', )
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.usercollector)
        super(Collector, self).save(*args, **kwargs)

    def __str__(self):
       return self.name

    # json=username, testname

class Transaction(models.Model):
    generatedid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Transaction')
    payee = models.ForeignKey(User, on_delete=models.DO_NOTHING ,related_name='payee_name')
    payeeuser =  models.CharField(max_length=30, blank=True)
    payeename = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='receiver_name')
    receiveruser = models.CharField(max_length=30, blank=True)
    receivername = models.CharField(max_length=50, blank=True)
    amount = models.IntegerField(default=0, blank=True)
    mode = models.CharField(max_length=50, blank=True)
    transactionid = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
    

    class Meta:
       ordering = ('-date', )
    def save(self, *args, **kwargs):
        self.slug = slugify(self.generatedid)
        if not self.id:
            self.payeename = self.payee.first_name +" "+ self.payee.last_name
            self.payeeuser = self.payee.username
            self.receivername = self.receiver.first_name +" "+ self.receiver.last_name
            self.receiveruser = self.receiver.username
        super(Transaction, self).save(*args, **kwargs)

    
    def __str__(self):
       return "%s %s" % (self.payee, self.generatedid)
    # trans_user = models.ForeignKey(AppUser, on_delete=DO_NOTHING, related_name="user_transaction")
    # trans_doctor = models.ForeignKey(UserDoctor, on_delete=DO_NOTHING, related_name="doctor_transaction")
    # trans_patho = models.ForeignKey(Patholab, on_delete=DO_NOTHING, related_name="transaction_patho")
    # trans_collector = models.ForeignKey(Collector,on_delete=DO_NOTHING, related_name="collector_transaction")
    # trans_hospital = models.ForeignKey(Hospital, on_delete=DO_NOTHING, related_name="hospital_transaction")
    
class AddRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user',on_delete=models.CASCADE)
    fromuser = models.CharField(max_length=50, blank=True)
    fromusername = models.CharField(max_length=25, blank=True)
    to_user = models.ForeignKey(User, related_name='to_user',on_delete=models.CASCADE)
    touser = models.CharField(max_length=50, blank=True)
    tousername = models.CharField(max_length=25, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.fromuser = self.from_user.first_name +" "+ self.from_user.last_name
            self.fromusername = self.from_user.username
            self.touser = self.to_user.first_name +" "+ self.to_user.last_name
            self.tousername = self.to_user.username
        super(AddRequest, self).save(*args, **kwargs)


class Prescription(models.Model):
    from_user = models.ForeignKey(User, related_name='from_doctor', on_delete=models.CASCADE)
    fromuser = models.CharField(max_length=50, blank=True)
    fromusername = models.CharField(max_length=25, blank=True)
    for_user = models.ForeignKey(User,  related_name='for_patient', on_delete=models.CASCADE)
    foruser = models.CharField(max_length=50, blank=True)
    forusername = models.CharField(max_length=25, blank=True)
    date = models.DateField(auto_now=True)
    medpres = models.JSONField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.id:
            self.fromuser = self.from_user.first_name +" "+ self.from_user.last_name
            self.fromusername = self.from_user.username
            self.foruser = self.for_user.first_name +" "+ self.for_user.last_name
            self.forusername = self.for_user.username
        super(Prescription, self).save(*args, **kwargs)

class FaqBlog(models.Model):
    byuser = models.ForeignKey(User,on_delete=models.CASCADE)
    byusername = models.CharField(max_length=25, blank=True)
    byfullname = models.CharField(max_length=25, blank=True)
    category = models.CharField(max_length=50, default="")
    question = models.TextField(default="")
    Answer = models.JSONField(null=True, blank=True)
    date = models.DateField(auto_now_add=True,null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.byusername = self.byuser.username
            self.byfullname = self.byuser.first_name +" "+ self.byuser.last_name
        super(FaqBlog, self).save(*args, **kwargs)
# class Contact(models.Model):
#     user = models.ForeignKey(User, related_name='friends')
#     friends = models.ManyToManyField('self', blank=True)

#     def __str__(self):
#         return self.user.username

# class Message(models.Model):
#     contact = models.ForeignKey(Contact, related_name='messages' , on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.contact.user.username

# class Chat(models.Model):
#     participants = models.ManyToManyField(Contact, related_name='chats')
#     messages = models.ManyToManyField(Message, blank=True)   

#     def last_10_messages(self):
#         return self.messages.objects.order_by('-timestamp').all()[:10]

#     def __str__(self):
#         return "{}".format(self.pk)

    




    
