import os.path
import urlparse
import urllib
import StringIO
import zipfile
import subprocess

PROTOC_EXE_NAME = "protoc.exe"
PROTOC_URL = "https://github.com/google/protobuf/releases/download/v2.6.1/protoc-2.6.1-win32.zip"
GATEWAY_DIR = os.path.abspath("..\solaron\gateway")
PROTO_NAMES = ["_messages.proto"]

if not os.path.isfile(PROTOC_EXE_NAME):
    print("{} not found... downloading from {}".format(PROTOC_EXE_NAME, PROTOC_URL))
    download_name = os.path.basename(urlparse.urlparse(PROTOC_URL).path) 
    try:
        urllib.urlretrieve(PROTOC_URL, download_name)
        with zipfile.ZipFile(download_name) as zip:
            zip.extract(PROTOC_EXE_NAME)
    finally:
        os.remove(download_name)

for proto_name in PROTO_NAMES:
    proto_path = os.path.join(GATEWAY_DIR, proto_name)
    print("Generating {}".format(proto_path))
    args = [PROTOC_EXE_NAME, "-I={}".format(GATEWAY_DIR), "--python_out={}".format(GATEWAY_DIR), proto_path]
    subprocess.Popen(args)

print("Gateway messages generated!")
