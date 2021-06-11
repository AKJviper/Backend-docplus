from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from DocPlus.settings import JWT_AUTH
from django.db import models, reset_queries
from rest_framework.views import APIView
from DocPlus.models import *
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, response, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.views.generic import DetailView, ListView
from django.conf import settings
from django.db.models import Q
from datetime import datetime
from django.db.models import Value as V
from django.db.models.functions import Concat
import jwt
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes , permission_classes
from rest_framework import status, permissions, parsers, filters
from .serializers import *
from rest_framework import authentication , exceptions
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import FileUploadParser, JSONParser
from django.views.decorators.csrf import csrf_exempt



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
    search_fields = ['userdoc__username', 'Name', 'city', 'state']

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
    search_fields = ['user', 'Name', 'slug']

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
    search_fields = ['service_area','city', 'state']

class HospitalList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Hospital.objects.all()
    serializer_class = HospitalSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'state']


class PatholabList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Patholab.objects.all()
    serializer_class = PatholabSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name','city', 'state']

class CollectorList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Collector.objects.all()
    serializer_class = CollectorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'state']


class TransactionList(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = ['transactionid', 'payee', 'receiver', 'date']
    search_fields = ['generateid','payee','receiver','transactionid','date']

class TransactionList(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset= Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['generateid','payee','receiver','transactionid','date']

    def get_object(self):
        transId = self.kwargs["transId"]
        return get_object_or_404(Transaction, transactionid=transId)

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

# @api_view(['POST'])
# def mainUser_create(request):
  

#     if request.method == 'POST':
#         serializer = UserSerializerWithToken(data=request.data)
#         if serializer.is_valid():
#             print(request.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
            
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.User_type = request.data.User_type
#     user.save()
    # elif request.method == 'PUT':
    #     serializer = User(recData, data=request.data,context={'request': request}).data
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

   

    
@parser_classes([MultiPartParser])
@api_view(['GET', 'POST'])
def user_detail(request, pk):
    try:
        user = User.objects.get(username=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        
        data_res = AppUser.objects.filter(user__username=pk)
        serializer = AppUserSerializer(data_res, context={'request': request}, many=True).data
        return Response(serializer)





   
   
#     elif request.method == 'POST':
#         # print(request.data)
#         serializer = AppUserSerializer(data=request.data)
#         if serializer.is_valid():
#             print(request.data)
            
#             serializer.save()
#             return Response(AppUserSerializer.data,  status=status.HTTP_201_CREATED)
            
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def get_object(self, request, pk):
    #     user = get_object_or_404(User, id=pk)
    #     obj, created  = AppUser.objects.get_or_create(
    #             user=user)
    #     if obj == None:
    #         raise Http404
    #     return obj

    # permission_classes = (permissions.AllowAny,)
    # def post(self, request, pk):
        
    #     if self.request.method == 'POST':
    #         serializer = AppUserSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(status=status.HTTP_201_CREATED)

    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
        
@api_view(['POST', 'PUT', 'FILES'])
@permission_required('AppUser.can_update')
def update_user(request, pk):
    try:
        recData = AppUser.objects.get(pk=pk)
    except AppUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = AppUserSerializer(recData, data=request.data,context={'request': request}).data
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([permissions.IsAuthenticated])
@permission_required(['AppUser.can_delete'])
@login_required
@api_view(['DELETE'])
def delete_user(request, pk):
    try:
        recData = AppUser.objects.get(pk=pk)
    except AppUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        recData.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










@permission_classes([permissions.AllowAny],)
@api_view(['GET', 'POST'])   
def doctor_list(request):
    if request.method == 'GET':
        res_data = UserDoctor.objects.all()

        serializer = UserDoctorSerializer(res_data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserDoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@permission_classes([permissions.AllowAny])
@api_view(['GET', 'POST', 'PUT'])
@parser_classes([MultiPartParser])
def doctor_detail(request, pk):
    try:
        userdoc = User.objects.get(pk=pk)
    except AppUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data_res = UserDoctor.objects.filter(userdoc=userdoc)
        serializer = UserDoctorSerializer(data_res, context={'request': request}, many=True).data
        return Response(serializer)

    elif request.method == 'PUT':
        serializer = UserDoctor(data=request.data,context={'request': request}).data
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)


@permission_required('UserDoctor.is_doctor')
@parser_classes([MultiPartParser])
@login_required
def update_doctor(request, pk):
    try:
        recData = UserDoctor.objects.get(pk=pk)
    except UserDoctor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        res_data = UserDoctor.objects.filter(pk="5")

        serializer = UserDoctorSerializer(res_data, context={'request': request}, many=True).data

        return Response(serializer)
    
    elif request.method == 'PUT':
        serializer = UserDoctor(recData, data=request.data,context={'request': request}).data
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recData.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# @login_required
# def messages_list(request):
#     if request.method == 'GET':
#         data = Messages.objects.all()
#         serializer = MessagesSerializer(data, context={'request': request}, many=True).data
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = MessagesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
            
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# @login_required
# def messages_detail(request, pk):
#     try:
#         recData = Messages.objects.get(pk=pk)
#     except Messages.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         data_res = Messages.objects.filter(pk=pk)

#         serializer = MessagesSerializer(data_res, context={'request': request}, many=True).data

#         return Response(serializer)

#     elif request.method == 'POST':
#         serializer = MessagesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_201_CREATED)
            
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#     if request.method == 'PUT':
#         serializer = Messages(recData, data=request.data,context={'request': request}).data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         recData.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)





# class IndexView(ListView):
#     model=AppUser
#     template_name='home.html'


# class DoctorDetailView(DetailView):
#     model =AppUser
#     all_models_dict = {
#         "template_name": "profile.html",
#         "queryset": AppUser.objects.all(),
#         "extra_context" : {"doctor_view" : UserDoctor.objects.all(),
                           
#                            }
#     }


# def search_doctors(request):
#     if request.method == "POST":
#         searched = request.POST.get('searched')
#         doctors = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name')).\
#                 filter(full_name__icontains=searched).filter(appuser__user_type='D')
#         return render(request, 'search_doctors.html', {'searched':searched,'doctors':doctors})
#     else:
#         return render(request, 'search_doctors.html', {})





# def mylogin(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')

#             # user = authenticate(username=username, password=password)
#             # if user is not None:
#             #     login(request, user)
#             #     return render(request, template_name='dashboard.html')
#             user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
#             userlog = authenticate(username=user, password=password)
#             if userlog is not None:
#                 login(request, user)
#                 messages.info(request, f"You are now logged in as {username}.")
#                 # return render(request, template_name='dashboard.html')
#                 return response(user)
#             else:
#                 messages.error(request,"Fill the credentials correctly")
#         else:
#             messages.error(request,"Invalid username or password.")
#     form = LoginForm()
#     return render(request, 'login.html', context={"form":form})
    
# @login_required(login_url='login/')   
# def userDetail(request):
#     if request.method == 'POST':
#         user_form = RegisterForm(request.POST)
#         doctor_form = DoctorForm(request.POST)
#         if user_form.is_valid() or doctor_form.is_valid():
#             form1=user_form.save(commit=False)
#             form1.recorded_by = request.user
#             form2 = doctor_form.save(commit=False)
#             form2.form1 = form1
#             form1.save()
#             form2.save()
#             UserDoctor.User = request.user
#             return redirect('dashboard')
            
#     else:
#         user_form = RegisterForm()
#         doctor_form = DoctorForm()

#     context = {'register_form': user_form , 'doctor_form': doctor_form} 
#     return render(request, 'detail_fill1.html', context)

# @api_view(['GET'])
# @login_required
# def isDoctor(request):
#     if(request.method == 'GET'):
        
#         # data_res = AppUser.objects.filter(city="Bhagalpur", )
#         # serializer = AppUserSerializer(data_res, context={'request': request}, many=True).data
#         data_res = AppUser.objects.filter(user_type="D")
#         serializer = AppUserSerializer(data_res, context={'request': request}, many=True).data
#         return Response(serializer)


        




def registration(request):
    return HttpResponse("We are at registration page")

def about(request):
    return  HttpResponse("We are at about page")

def search(request):
    return  HttpResponse("We are at search page")


def contact(request):
    if request.method=="POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message', '')
        print(name, email, phone, message)
    return render(request, 'contact.html')


def bookapp(request):
    return  HttpResponse("We are at book appointment page")


def consult(request):
    return HttpResponse("We are at consult page")


def presList(request):
    return HttpResponse("We are at prescription list page")


def header(request):
    return render(request, 'header.html')
    

def dashboard(request):
    return render(request, 'dashboard.html')



# def user_register(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('userinfo')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})
@permission_classes([permissions.AllowAny],)
@api_view(['GET', 'POST'])   
def hospital_list(request):
    if request.method == 'GET':
        res_data = Hospital.objects.all()

        serializer = HospitalSerializer(res_data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@login_required
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def hospital_detail(request, user):
    try:
        userhospital = User.objects.filter(username=user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data_res = Hospital.objects.filter(userhospital=userhospital)
        serializer = HospitalSerializer(data_res, context={'request': request}, many=True).data
        return Response(serializer)



@permission_classes([permissions.AllowAny],)
@api_view(['GET', 'POST'])   
def patholab_list(request):
    if request.method == 'GET':
        res_data = Patholab.objects.all()

        serializer = PatholabSerializer(res_data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatholabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@permission_classes([permissions.AllowAny])
@api_view(['GET'])
def patholab_detail(request, user):
    try:
        userpatho = User.objects.filter(username=user)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data_res = Patholab.objects.filter(userhospital=userpatho)
        serializer = UserDoctorSerializer(data_res, context={'request': request}, many=True).data
        return Response(serializer)

