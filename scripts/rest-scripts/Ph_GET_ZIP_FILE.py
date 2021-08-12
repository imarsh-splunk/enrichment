import requests
import zipfile

zip_url = "http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip"
r = requests.get(zip_url).content

zip_path = "/tmp/top-1m.csv.zip"
zfile = open(zip_path, 'wb')
zfile.write(r)
zfile.close()

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall()

