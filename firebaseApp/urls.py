from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn, name= 'signIn'),
    path('postsign', views.postsign, name='postsign'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('createreport', views.createreport, name='createreport'),
    path('postcreate', views.postcreate, name='postcreate'),
    path('checkreport', views.checkreport, name='checkreport'),
    path('post_report', views.post_report, name='post_report'),
]
