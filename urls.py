"""DocPlus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('admin/', admin.site.urls),
    re_path(r'^api/users/$', UserList.as_view()),
    re_path(r'^api/usersearch/$', Alluser.as_view()),
    # re_path(r'^api/usertype/$', views.update_profile),
    # re_path(r'^api/usercreate/$', views.mainUser_create),
    re_path(r'^api/Doctor/$', DoctorList.as_view()),
    re_path(r'^api/detail/Doctor/(?P<slug>.*)/$', DoctorDetail.as_view()),
    # re_path(r'^api/doctor/(?P<pk>.*)/$',views.doctor_detail),
    re_path(r'^api/user/(?P<username>.*)/$', MainUserDetail.as_view()),
    re_path(r'^api/Patient/$', AppUserList.as_view()),
    re_path(r'^api/Hospital/$', HospitalList.as_view()),
    re_path(r'^api/detail/Patient/(?P<slug>.*)/$', AppUserDetail.as_view()),
    re_path(r'^api/detail/Hospital/(?P<slug>.*)/$', HospitalDetail.as_view()),
    re_path(r'^api/Ambulance/$', AmbulanceList.as_view()),
    re_path(r'^api/detail/Ambulance/(?P<slug>.*)/$', AmbulanceDetail.as_view()),
    re_path(r'^api/profile/$', ProfileList.as_view()),
    re_path(r'^api/usertype/(?P<user_name>.*)/$', ProfileDetail.as_view()),
    re_path(r'^api/allrequest/$', FriendList.as_view()),
    re_path(r'^api/userrequest/(?P<from_user>.*)$', FriendRequestDetail.as_view()),
    re_path(r'^api/Patholab/$', PatholabList.as_view()),
    re_path(r'^api/FaqBlog/$', FaqBlogList.as_view()),
    re_path(r'^api/detail/FaqBlog/(?P<byusername>.*)/$',  PatholabDetail.as_view()),
    re_path(r'^api/detail/Patholab/(?P<slug>.*)/$',  PatholabDetail.as_view()),
    re_path(r'^api/Prescription/$',  PrescriptionList.as_view()),
    re_path(r'^api/Collector/$', CollectorList.as_view()),
    re_path(r'^api/detail/Collector/(?P<slug>.*)/$', CollectorDetail.as_view()),
    re_path(r'^api/faq/$', FaqBlogList.as_view()),
    re_path(r'^api/detail/faq/(?P<pk>.*)/$', FaqBlogDetail.as_view()),
    # re_path(r'^api/detail/Collector/(?P<slug>.*)/$', CollectorDetail.as_view()),
    re_path(r'^api/transaction/$', TransactionList.as_view()),
    re_path(r'^api/detail/transaction/(?P<generatedid>.*)/$', TransactionDetail.as_view()),
    re_path(r'^api/detail/contact/(?P<date>.*)/$', Contactdetail.as_view()),
     re_path(r'^api/contact/$',  Contactlist.as_view()),
    re_path(r'^api/user_transaction/(?P<user>.*)/$', views.user_transaction),
    re_path(r'^api/rcv_transaction/(?P<user>.*)/$', views.rcv_transaction),
    # re_path(r'^api/doctor/$', views.doctor_list),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^send_request/(?P<fromu>.*)/(?P<to>.*)/$', views.send_request),
    re_path(r'^list_pres/(?P<user>.*)/$', views.list_pres),
    re_path(r'^delete_pres/(?P<presid>.*)/$', views.delete_pres),
    re_path(r'^request_list/(?P<userid>.*)/$', views.requestlist),
    re_path(r'^delete_request/(?P<my_id>.*)/(?P<userid>.*)/$', views.delete_request),
    re_path(r'^api/(?P<username>.*)/update/$', views.UserUpdateAPIView.as_view(), name='UserUpdateAPIView'),
    path('api/appuser/<int:pk>', AppUserDetail.as_view()),
    path('token-auth/', obtain_jwt_token),
    path('token-auth/refresh', refresh_jwt_token),
    path('currentuser/', views.currentuser),
    path('chat/', include('chat.urls')),
    path('pay/', views.start_payment, name="start_payment"),
    path('handlepayment/', views.handlepayment, name="handlepayment"),
    
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
