from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [ 
    path('', views.register, name='register'), 
    path('teste', views.register_teste, name='registerteste'), 
] 