import lxml.etree as ET
import re
import os
import zipfile
from py_asciimath.translator.translator import (
    ASCIIMath2MathML,
    ASCIIMath2Tex,
    MathML2Tex,
    Tex2ASCIIMath
)

# copied and modified from https://dev.to/furkan_kalkan1/quick-hack-converting-mathml-to-latex-159c


def convert_mathml(itemXml, latex):
    formulaCount = 0
    formulaExceptionCount = 0

    # mathml2tex = MathML2Tex()
    # """ Remove TeX codes in text"""
    # itemXml = re.sub(r"(\$\$.*?\$\$)", " ", itemXml)
    """ Find MathML codes and replace it with its LaTeX representations."""
    mml_codes = re.findall(r"(<m:math.*?<\/m:math>)", itemXml)
    for mml_code in mml_codes:
        mml_ns = mml_code.replace('m:', '')
        # Required.
        mml_ns = mml_ns.replace(
            '<math>', '<math xmlns="http://www.w3.org/1998/Math/MathML">')
        mml_dom = ET.fromstring(mml_ns)
        # mml_ns = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\r\n<!DOCTYPE math PUBLIC \"-//W3C//DTD MathML 2.0//EN\" \"http://www.w3.org/Math/DTD/mathml2/mathml2.dtd\">\r\n' + mml_ns
        # latex_code = mathml2tex.translate(
        #     mml_ns, network=True, from_file=False,)
        mmldom = transform(mml_dom)
        formulaCount = formulaCount + 1
        latex_code =  '$' + str(mmldom) + '$'
  
        if latex:
            itemXml = itemXml.replace(mml_code, latex_code)
        else:
            try:
                latex_code = latex_code.replace('[\\', '[ \\')
                l = latex_code.decode('utf-8')
                # latex_code = latex_code.encode(encoding='ascii',errors='ignore')
                ascii_math = tex2ASCIIMath.translate(l)
                itemXml = itemXml.replace(mml_code, ascii_math)
            except Exception as e: 
                formulaExceptionCount = formulaExceptionCount + 1
                print("An exception occurred while converting LaTeX to ASCII Math: ")
                print(f'mathML:{mml_code}')
                print(f'LaTeX:{latex_code}')
                # print(e)
                     
    return itemXml, formulaCount, formulaExceptionCount

def convert_mathml_in_package(file: str, latex: bool):
    # copy file to working directory
    # filename = 'working-directory/qti-package' + \
    #     time.strftime("%Y%m%d-%H%M%S") + '.zip'
    # with open(filename, 'wb') as new_file:
    #     new_file.write(f.stream.read())
    package_folder = os.path.splitext(file)[0]
    # unzip package
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall(package_folder)
    zip_ref.close()

    # open manifest file
    manifest = ET.parse(package_folder + '/imsmanifest.xml').getroot()
    ns = {'d': 'http://www.imsglobal.org/xsd/imscp_v1p1'}
    # xpath to get all items in package
    item_refs = manifest.findall(
        ".//d:resource[@type='imsqti_item_xmlv2p2']", ns)
    item_codes = [item_ref.attrib['href'] for item_ref in item_refs]
    formulaCount = 0
    formulaExceptions = 0

    # loop through all item references
    for item_ref in item_codes:
        # , encoding='utf-8'
        with open(package_folder + '/' + item_ref, 'r', encoding='utf-8') as file:
            xmlWithLatex, c, e  = convert_mathml(file.read(), latex)
            formulaCount = formulaCount + c
            formulaExceptions = formulaExceptions + e
            with open(file.name, "w", encoding='utf-8') as text_file:
                print('processing ' + item_ref)
                text_file.write(xmlWithLatex)
    return formulaCount, formulaExceptions

xslt = ET.parse("mmltex/mmltex.xsl")
transform = ET.XSLT(xslt)
tex2ASCIIMath = Tex2ASCIIMath(log=False, inplace=True)
covertedFormulas, formulaExceptions = convert_mathml_in_package('C:/TMP/test/WiskundeA.zip', False)
print('converted: ' + str(covertedFormulas) + ' exeptions: ' + str(formulaExceptions)) 
        # open item xml file
        # item = ET.parse(package_folder + '/' + item_ref).getroot()

# rootdir = 'C:/TMP/test/depitems'
# extensions = ('.xml')

# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         ext = os.path.splitext(file)[-1].lower()
#         if ext in extensions:
#             with open(rootdir + '/' + file, 'r') as file:
#                 xmlWithLatex = convert_mathml(file.read(), True)
#                 with open(file.name, "w") as text_file:
#                     text_file.write(xmlWithLatex)



