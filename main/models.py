from django.db import models
from django import forms

type_help = """If you want to download the certificates from the loadbalancer to the FTP server, select import.
If you want to upload certificates to the loadbalancer, select export."""
sslassoc_help = """Paste the configuration of the source CSS here. Actually the lines with "ssl associate" would be enough."""

class SSL_Associations_Form(forms.Form):
   ftp_record_name = forms.CharField(max_length=31, label = "FTP record name")
   sslassoc = forms.CharField(widget = forms.Textarea(attrs = {'rows' : 10, 'cols' : '82'}), label = "SSL associations from CSS config", help_text=sslassoc_help)
   pem_password = forms.CharField(max_length=31, initial = "rack", label = "PEM password")
   type = forms.ChoiceField(choices = [('import', 'Import'), ('export', 'Export'), ('both', 'Both')],
                                          label="Action type", help_text = type_help)

