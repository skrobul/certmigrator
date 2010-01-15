from main.models import SSL_Associations_Form
from django.shortcuts import render_to_response

def index(request):
    """main view"""
    if request.method == "POST":
        form = SSL_Associations_Form(request.POST)
        if form.is_clean():
            filelist = get_list_from_file(form.cleaned_data['sslassoc'])
            ftp_record = form.cleaned_data['ftp_record_name']
            pem_password = form.cleaned_data['pem_password']
            commands = generate_export_commands(
                            files = filelist,
                            ftp = ftp_record,
                            pem = pem_password)
            return render_to_response('succes.html', {
                            'cmd' : commands,
                            })
        else:
            form = SSL_Associations_Form()
            return render_to_response('index.html', dict(form = form)) 
    else:
        form = SSL_Associations_Form()
        return render_to_response('index.html', dict(form = form)) 
