from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Order model for customer's order and status


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__'


# User Authentication Form
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Customer Form
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
