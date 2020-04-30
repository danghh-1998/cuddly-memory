from django.urls import path
from .apis import *

urlpatterns = [
    path('auth/sign_in', SignInApi.as_view(), name='sign_in'),
    path('users/<int:user_id>', UserDetailApi.as_view(), name='user_detail'),
    path('users/update', UserUpdateApi.as_view(), name='user_update'),
    path('users/deactivate', UserDeactivateApi.as_view(), name='user_deactivate'),
    path('users/change_password', UserChangePasswordApi.as_view(), name='user_change_password'),
    path('users/req_reset_password', UserRequestResetPasswordApi.as_view(), name='user_req_reset_password'),
    path('users/reset_password', UserResetPassword.as_view(), name='user_reset_password'),
    path('users/create_user', UserCreateApi.as_view(), name='create_user')
]
