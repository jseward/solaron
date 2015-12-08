PROTOC_EXE_NAME = "protoc.exe"
PROTOC_URL = "https://github.com/google/protobuf/releases/download/v2.6.1/protoc-2.6.1-win32.zip"
GATEWAY_DIR = "c:\dev\solaron\solaron\gateway"
PROTO_NAME = "_messages.proto"

import os.path
import urlparse
import urllib
import StringIO
import zipfile
import subprocess

if not os.path.isfile(PROTOC_EXE_NAME):
    print("{} not found... downloading from {}".format(PROTOC_EXE_NAME, PROTOC_URL))
    download_name = os.path.basename(urlparse.urlparse(PROTOC_URL).path) 
    try:
        urllib.urlretrieve(PROTOC_URL, download_name)
        with zipfile.ZipFile(download_name) as zip:
            zip.extract(PROTOC_EXE_NAME)
    finally:
        os.remove(download_name)
      
args = [PROTOC_EXE_NAME, "-I={}".format(GATEWAY_DIR), "--python_out={}".format(GATEWAY_DIR), os.path.join(GATEWAY_DIR, PROTO_NAME)]
subprocess.Popen(args)

print "Gateway Messages generated!"
