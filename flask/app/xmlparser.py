from app import app
from app import camundarest
from xmler import dict2xml
from dicttoxml import dicttoxml
import xml.etree.ElementTree as ET
from flask_cors import cross_origin
from flask_cors import CORS
import codecs
import json
CORS(app, resources={r'/*': {'origins': '*'}})

global bpmn, camunda
bpmn = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
camunda = 'http://camunda.org/schema/1.0/bpmn'

ET.register_namespace(bpmn, 'http://www.omg.org/spec/BPMN/20100524/MODEL')


def something(key):  # fali parametar form_key
    # key = "PrijavaZavrsnogRada"
    res = camundarest.get_process_xml(key)  # res gets dictionary
    xml = res['bpmn20Xml']  # xml is stored in value of res
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()
    form_key = "prijava_teme"  # formKey is needed for form identification
    find_form = root.findtext(".//userTask", form_key)
    if(find_form != ""):
        element = root.find('.//{http://camunda.org/schema/1.0/bpmn}formData')
        model = {}
        fields = []
        temp = {}
        for child in element.iter():
            if(child.attrib != {}):
                if(child.attrib['id']):
                    temp['model'] = child.attrib['id']
                    temp['label'] = child.attrib['label']
                    if child.attrib['type'] == 'boolean':
                        temp['type'] = 'checkbox'
                        temp['default'] = 'false'
                        model[child.attrib['id']] = 'false'
                    else:
                        temp['type'] = 'input'
                        temp['inputType'] = 'text'
                        model[child.attrib['id']] = ''
                    fields.append(temp)
                    temp = {}
                    print(model)
        schema1 = {'fields' : fields}
        bigobj1 = {'model' : model, 'schema': schema1}
        bigobj = json.dumps(bigobj1, ensure_ascii=False).encode('utf-8')
    return bigobj
