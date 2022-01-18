from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import CreateUserView, LoginUserView, UserView, LogoutView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
