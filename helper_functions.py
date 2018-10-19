import re
import unicodedata
import ntpath
import html

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def clean(s):
    if s is not None:
        s = html.unescape(s)
        s = replaceTabSpacesNewLineBySpaces(s)
        s = replaceNewLineBySpaces(s)
        s = removeWeirdSpaces(s)
        s = removeDoubleSpaces(s)
        s = removeDoubleSpaces(s)
        s = s.strip()
        return s
    return ''


def get_end_clean(elem):
    if elem is not None:
        elem_name = elem.tag.replace(
            '{http://www.imsglobal.org/xsd/imsqti_v2p1}', '')
        if elem_name == 'img':
            return path_leaf(elem.attrib['src'])
        else:
            return clean(elem.text)


def removeDoubleSpaces(s):
    return re.sub(' +', ' ', s)


def replaceTabSpacesNewLineBySpaces(s):
    return re.sub(r'\s+', ' ', s)


def replaceNewLineBySpaces(s):
    return s.replace('\n', ' ').replace('\r', '')


def removeWeirdSpaces(s):
    s = unicodedata.normalize("NFKD", s)
    return s

def is_child_of(parents, child):
    for parent in parents:
        for elem in parent.findall(".//*"):
            if elem == child:
                return True
    return False
