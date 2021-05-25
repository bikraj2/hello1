from django.urls import path
from btm import views

app_name= 'btm'

urlpatterns=[
path('register',views.register,name='register'),
path('user_login',views.user_login,name='user_login')
]
