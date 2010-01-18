from django.test import TestCase
from main.views import *
example_config_file = """
configure
global warming
blah blah
ssl associate cert mychainedrsacert1 mychainedrsacert.pem
ssl associate rsakey mykey mykey.pem
some other stuff
ssl associate cert myothercert myothercert.pem
my content rules
and so on
"""
certdict = [
             {'type' : 'rsacert', 'name' : 'foo', 'filename': 'foo.pem'},
             {'type' : 'rsacert', 'name' : 'bar', 'filename': 'bar.pem'},
             {'type' : 'rsakey', 'name' : 'foobar', 'filename': 'foobar.pem'},
           ]

class MainTest(TestCase):
    def test_get_list_from_file(self):
        """
        Tests if the function is able to pickup proper filenames from a configuration file.
        """
        file_list = get_list_from_file(example_config_file)
        self.failUnless(file_list)
        self.failUnless({'type': 'cert', 'name': 'mychainedrsacert1', 'filename': 'mychainedrsacert.pem'} in file_list)
        self.failUnless({'type': 'rsakey', 'name': 'mykey', 'filename': 'mykey.pem'} in file_list)
        self.failUnlessEqual(len(file_list), 3)
    def test_generate_commands(self):
        """
        Tests if the function generates the proper commands from the given input
        """
        cmds = generate_commands(files = certdict, record_name = 'TESTRECORD', pem_password = 'test', type = 'import')
        self.failUnless(cmds)
        self.failUnless("copy ssl ftp TESTRECORD import bar.pem PEM 'test'" in cmds)
        self.failUnless("copy ssl ftp TESTRECORD import foo.pem PEM 'test'" in cmds)
        self.failUnlessEqual(len(cmds), 3)

