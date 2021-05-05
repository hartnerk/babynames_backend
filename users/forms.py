from .models import UserCouples
from django.forms import ModelForm

class UserCouplesForm(ModelForm):
    class Meta:
        model = UserCouples
        fields = ['user_one', 'user_two']