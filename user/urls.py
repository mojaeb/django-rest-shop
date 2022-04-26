from django.urls import re_path, path
from .views import generate_registration_code, get_register_code_time, verify_code_and_register

app_name = 'users'

urlpatterns = [
    re_path(r'^suspended-registration/', generate_registration_code, name="generate-registration-code"),
    path('get-register-code-time/<int:phone_number>/', get_register_code_time, name="generate-registration-code"),
    re_path(r'^verify-code-and-register/', verify_code_and_register, name="generate-registration-code"),
]
