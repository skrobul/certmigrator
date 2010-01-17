from main.models import SSL_Associations_Form
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    """main view"""
    if request.method == "POST":
        form = SSL_Associations_Form(request.POST)
        if form.is_valid():
            filelist = get_list_from_file(form.cleaned_data['sslassoc'])
            ftp_record = form.cleaned_data['ftp_record_name']
            pem_password = form.cleaned_data['pem_password']
            commands = generate_export_commands(
                            files = filelist,
                            record_name = ftp_record,
                            pem_password = pem_password)
            return render_to_response('success.html', {
                            'cmd' : commands,
                            },
                            context_instance=RequestContext(request))
        else:
            return render_to_response('index.html', dict(form = form),
                            context_instance=RequestContext(request)) 
    else:
        form = SSL_Associations_Form()
        return render_to_response('index.html', dict(form = form), 
                            context_instance=RequestContext(request)) 

def get_list_from_file(src):
    """
    Parses "ssl associate" config lines from the CSS.
    Args:   string buffer containing CSS configuration
    Returns: list of .pem files
    """
    import re
    ssl_entry_regexp = re.compile("^ssl associate (rsacert|rsakey) (?P<name>\w+) (?P<filename>\w+\.pem)")
    certs = []
    for line in src.split("\n"):
        ret = ssl_entry_regexp.match(line)
        if ret:
            certs.append(ret.groupdict())
    return certs

def generate_export_commands(files, record_name, pem_password):
    """Generates configuration file that can be uploaded to the CSS as a 
    startup file and then merged with running config in result importing
    all SSL files the loadbalancer.
    Args: 
        files - list of dicitionaries representing SSL files in 
                following format:
                [
                 {'type' : 'rsacert', 'name' : 'foo', 'filename': 'foo.pem'},
                 {'type' : 'rsacert', 'name' : 'bar', 'filename': 'bar.pem'},
                 {'type' : 'rsakey', 'name' : 'foobar', 'filename': 'foobar.pem},
                ]
        record_name - name of the FTP record which will be used in the
                      configuration of CSS for importing certificates from
                      external FTP server.
        pem_password - the password which was used for encryption of
                       certificates or private keys.
    """
    # shorter version
    #["copy ssl ftp %s import %s PEM '%s'" % (record_name, file['filename'], pem_password) for file in files ]
    # but uglier...
    cmdlist = [] 
    for file in files:
        cmdlist.append("copy ssl ftp %s import %s PEM '%s'" % (record_name, file['filename'], pem_password))
    print cmdlist
        
