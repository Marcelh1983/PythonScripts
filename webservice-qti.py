from flask import Flask, request, make_response
import xml.etree.ElementTree as ET
import zipfile
import io
import time
import os
app=Flask(__name__)

@app.route("/uploadQtiPackage", methods=['GET', 'POST'])
def upload_packagefile():
    f = request.files['file']
    if not f:
        return "No file"
    filename = 'working-directory/qti-package' + time.strftime("%Y%m%d-%H%M%S") + '.zip'
    with open(filename,'wb') as new_file:
        new_file.write(f.stream.read())
    package_folder = os.path.splitext(filename)[0]
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(package_folder)
    zip_ref.close()
    
    ns = {'d': 'http://www.imsglobal.org/xsd/imscp_v1p1'}
    manifest = ET.parse(package_folder + '/imsmanifest.xml').getroot()
    items = manifest.findall(".//d:resource[@type='imsqti_item_xmlv2p1']", ns)
    item_codes = [item.attrib['href'] for item in items]
    print('item codes: ' + '\n'.join(item_codes))
    response = make_response('ok')
    return response


if __name__ == "__main__":
    app.run()