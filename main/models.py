from django.db import models
from django import forms



class SSL_Associations_Form(forms.Form):
   ftp_record_name = forms.CharField(max_length=31, label = "FTP record name")
   sslassoc = forms.CharField(widget = forms.Textarea, label = "SSL associations from CSS config")
   pem_password = forms.CharField(max_length=31, initial = "rack", label = "PEM password")

