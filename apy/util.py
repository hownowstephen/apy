from xml.etree.ElementTree import Element, SubElement, tostring

def DictToXML(data,root='data'):
    root =  Element(root)
    for (field, val) in data.iteritems():
        SubElement(root, field).text = val
    return tostring(root)