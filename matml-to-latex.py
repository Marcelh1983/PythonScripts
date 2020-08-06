import lxml.etree as ET
import re
import os
# copied and modified from https://dev.to/furkan_kalkan1/quick-hack-converting-mathml-to-latex-159c
def to_latex(text):
    """ Remove TeX codes in text"""
    text = re.sub(r"(\$\$.*?\$\$)", " ", text) 

    """ Find MathML codes and replace it with its LaTeX representations."""
    mml_codes = re.findall(r"(<m:math.*?<\/m:math>)", text)
    for mml_code in mml_codes:
        mml_ns = mml_code.replace('m:', '')
        mml_ns = mml_ns.replace('<math>', '<math xmlns="http://www.w3.org/1998/Math/MathML">') #Required.
        mml_dom = ET.fromstring(mml_ns)
        xslt = ET.parse("mmltex/mmltex.xsl")
        transform = ET.XSLT(xslt)
        mmldom = transform(mml_dom)
        latex_code = str(mmldom)
        text = text.replace(mml_code, '$' + latex_code + '$')
    return text

rootdir = 'C:/TMP/test/depitems'
extensions = ('.xml')

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            with open(rootdir + '/' + file, 'r') as file:
                xmlWithLatex = to_latex(file.read())
                with open(file.name, "w") as text_file:
                    text_file.write(xmlWithLatex)



