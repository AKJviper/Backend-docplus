from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from DocPlus.settings import JWT_AUTH
from django.db import models, reset_queries
from rest_framework.views import APIView
from DocPlus.models import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Value as V
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes , permission_classes
from rest_framework import status, permissions, filters
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import Checksum
import os


class UserList(APIView):
    permission_classes = ([permissions.IsAuthenticated])
    def get(self, request):
        if self.request.method == 'GET':
            data_res = User.objects.filter(username=request.user)

            serializer = UserSerializer(data_res, context={'request': request}, many=True).data

            return Response(serializer)    


    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Alluser(ListAPIView):
    queryset= User.objects.all()
    serializer_class = AllUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

class ProfileList(ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset= Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user_name', "profile_name"]

class ProfileDetail(RetrieveUpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field='user_name'

class DoctorList(ListCreateAPIView):
    queryset= UserDoctor.objects.all()
    serializer_class = UserDoctorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [ 'name', 'city', 'state', 'address']

class FriendList(ListCreateAPIView):
    queryset= AddRequest.objects.all()
    serializer_class = AddRequestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['from_user', 'pk']



class DoctorDetail(RetrieveUpdateAPIView):
    # parser_classes=(MultiPartParser,)
    queryset = UserDoctor.objects.all()
    serializer_class = UserDoctorSerializer
    lookup_field='slug'


class MainUserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field='username'



class MainUserList(ListCreateAPIView):
    queryset= User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name']


class AppUserList(ListCreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    queryset= AppUser.objects.all()
    serializer_class = AppUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user', 'name', 'slug']

class HospitalDetail(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Hospital.objects.all()
    serializer_class = HospitalSerializer
    lookup_field='slug'


class AmbulanceDetail(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Ambulance.objects.all()
    serializer_class = AmbulanceSerializer
    lookup_field='slug'

class AmbulanceList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Ambulance.objects.all()
    serializer_class = AmbulanceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['address','city', 'state']

class HospitalList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'state', 'address']


class PatholabList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Patholab.objects.all()
    serializer_class = PatholabSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','city', 'state', 'address']

class CollectorList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Collector.objects.all()
    serializer_class = CollectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city']


class TransactionDetail(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field = 'generatedid'
   
    # def get_object(self):
    #     transId = self.kwargs["transId"]
    #     return get_object_or_404(Transaction, transactionid=transId)
        
class TransactionList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['generateid','payee','receiver','transactionid','date']

    

class AppUserDetail(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    lookup_field = 'slug'

class PatholabDetail(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Patholab.objects.all()
    serializer_class = PatholabSerializer
    lookup_field = 'slug'

class CollectorDetail(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Collector.objects.all()
    serializer_class = CollectorSerializer
    lookup_field = 'slug'

class FriendRequestDetail(RetrieveUpdateDestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset = AddRequest.objects.all()
    serializer_class = AddRequestSerializer
    # lookup_field = 'from_user'

class FriendRequestList(ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset= AddRequest.objects.all()
    serializer_class = AddRequestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [ 'fromuser']


class PrescriptionList(ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset= Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [ 'forusername', 'fromusername']

class Contactlist(ListCreateAPIView):
    permission_classes=[permissions.AllowAny]
    queryset= ContactForm.objects.all()
    serializer_class =ContactSerializer

class Contactdetail(RetrieveAPIView):
    permission_classes=[permissions.AllowAny]
    queryset= ContactForm.objects.all()
    serializer_class =ContactSerializer
    lookup_field='date'

@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def list_pres(request, user):
    if request.method == 'GET':
        data = Prescription.objects.filter(forusername = user)

        serializer = PrescriptionSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def user_transaction(request, user):
    if request.method == 'GET':
        data = Transaction.objects.filter(payee = user)

        serializer = TransactionSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

# @permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def rcv_transaction(request, user):
    if request.method == 'GET':
        data = Transaction.objects.filter(receiveruser = user)

        serializer = TransactionSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@permission_classes([permissions.IsAuthenticated])
@api_view(['DELETE'])
def delete_pres(request, presid):
    if request.method == 'DELETE':
        data = Prescription.objects.get(id=presid)
        data.delete()
        return HttpResponse("Request Deleted")
    else:
        return HttpResponse("Request already deleted")

@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def requestlist(request, userid):
    if request.method == 'GET':
        data = AddRequest.objects.filter(to_user = userid)

        serializer = AddRequestSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@permission_classes([permissions.IsAuthenticated])
@api_view(['DELETE'])
def delete_request(request,my_id, userid):
    if request.method == 'DELETE':
        data = AddRequest.objects.get(to_user = my_id , from_user = userid)
        data.delete()
        return HttpResponse("Request Deleted")
    else:
        return HttpResponse("Request already deleted")



class FaqBlogList(ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset= FaqBlog.objects.all()
    serializer_class = FaqBlogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [ 'category', 'byusername', 'question']

class FaqBlogDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = FaqBlog.objects.all()
    serializer_class = FaqBlogSerializer

class RegisterView(viewsets.ModelViewSet):
   serializer_class = UserSerializer
   get_queryset = User.objects.all()
   def post(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      if user:
         return Response({
            "user": UserSerializer(user,
               context=self.get_serializer_context()).data
         })
      return Response



@api_view(['GET'])
def currentuser(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
def send_request(request, fromu , to):
        if request.method == 'POST':
           from_user = User.objects.get(id=fromu)
           to_user = User.objects.get(id=to)
           add_request, created = AddRequest.objects.get_or_create(from_user = from_user, to_user=to_user)
           if created:
                return HttpResponse('Request Sent')
       
        return HttpResponse('Request already sent')

@login_required
@permission_classes([permissions.IsAuthenticated,])
def accept_request(request, sender_username):
    try:
        add_request = AddRequest.objects.get(from_user=sender_username)
    except AddRequest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # sender = User.objects.get(username = Acceptor.from_user)
    #     if add_request.to_user == request.user:

    # accepter = AddRequest.objects.get(to_user=request.user)
    if add_request.to_user == request.user:
        acceptor =UserDoctor.objects.get(userdoc=request.user)
        acceptor.friends.add(add_request.from_user)
        sender = AppUser.objects.get(user=add_request.from_user)
        sender.friends.add(add_request.to_user)
        add_request.delete()
        return HttpResponse('Request Accepted')
    else:
        return HttpResponse('Request not Accepted')



def userDelete(request):
    try:
        recData = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        recData.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = UserUpdateSerialier
    lookup_field = 'username'

    def get_object(self):
        username = self.kwargs["username"]
        return get_object_or_404(User, username=username)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


# @permission_classes([permissions.IsAuthenticated])
@parser_classes([MultiPartParser])
@api_view(['GET', 'POST'])
def user_all(request):
    if request.method == 'GET':
        data = AppUser.objects.all()

        serializer = AppUserSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors)



# Create your views here.


@api_view(['POST'])
def start_payment(request):
    # request.data is coming from frontend
   
    print(request.data)
    uid= request.data['payeeslug']
    userp = User.objects.get(username=uid)
    payee=userp
    rcv = request.data['receiverslug']
    usero = User.objects.get(username=rcv)
    receiver= usero
    puid = request.data['puid']
    amount = request.data['amount']
    mode = request.data['mode']

    # we are saving an order instance (keeping isPaid=False)
    order = Transaction.objects.create(payee=payee, receiver=receiver, amount=amount, puid=puid, mode=mode)

    serializer = TransactionSerializer(order)
    # we have to send the param_dict to the frontend
    # these credentials will be passed to paytm order processor to verify the business account
    param_dict = {
        'MID': os.environ.get('MERCHANTID'),
        'ORDER_ID': str(order.generatedid),
        'TXN_AMOUNT': str(amount),
        'CUST_ID': payee,
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/api/handlepayment/',
        # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
    }

    # create new checksum (unique hashed string) using our merchant key with every paytm payment
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, os.environ.get('MERCHANTKEY'))
    # send the dictionary with all the credentials to the frontend
    return Response({'param_dict': param_dict})


@api_view(['POST'])
def handlepayment(request):
    checksum = ""
    # the request.POST is coming from paytm
    form = request.POST

    response_dict = {}
    order = None  # initialize the order varible with None

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            checksum = form[i]

        if i == 'ORDERID':
            # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
            order = Transaction.objects.get(id=form[i])

    # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
    verify = Checksum.verify_checksum(response_dict, os.environ.get('MERCHANTKEY'), checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            # if the response code is 01 that means our transaction is successfull
            print('order successful')
            # after successfull payment we will make isPaid=True and will save the order
            order.isPaid = True
            order.save()
            # we will render a template to display the payment status
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            return render(request, 'paytm/paymentstatus.html', {'response': response_dict})




