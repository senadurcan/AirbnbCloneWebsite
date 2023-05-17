from django.forms import ModelForm
from .models import *

class HesapForm(ModelForm):
    class Meta:
        model = Profil
        fields = ['isim','soyisim','meslek','telefon','profilresim']
    def __init__(self,*args,**kwargs):
        super(HesapForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
 