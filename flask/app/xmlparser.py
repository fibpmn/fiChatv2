from app import app
from app import camundarest
import xml.etree.ElementTree as ET
from flask_cors import cross_origin
from flask_cors import CORS
import json

CORS(app, resources={r'/*': {'origins': '*'}})

def parse(process_definition_id, form_key):
    
    res = json.loads(camundarest.get_process_xml(process_definition_id))  
    xml = res['bpmn20Xml']  # xml is stored in value of res
    tree = ET.ElementTree(ET.fromstring(xml))
    root = tree.getroot()
    find_form = root.findtext(".//userTask", form_key)
    if(find_form != ""):
        element = root.findall('.//{http://www.omg.org/spec/BPMN/20100524/MODEL}userTask')
        for child in element:
            if child.get('{http://camunda.org/schema/1.0/bpmn}formKey') == form_key:
                grandchildren = child.getchildren()
                for grandchild in grandchildren:
                    if grandchild.getchildren() != []:
                        greatgrandchildren = grandchild.getchildren()
                        if greatgrandchildren != []:
                            for greatgrandchild in greatgrandchildren:
                                greatgreatgrandchildren = greatgrandchild.getchildren()
                                model = {}
                                fields = []
                                temp = {}
                                for lastoneipromise in greatgreatgrandchildren:
                                    temp['model'] = lastoneipromise.attrib['id']
                                    temp['label'] = lastoneipromise.attrib['label']
                                    if lastoneipromise.attrib['type'] == 'boolean':
                                        temp['type'] = 'checkbox'
                                        temp['default'] = 'false'
                                        model[lastoneipromise.attrib['id']] = 'false'
                                    else:
                                        temp['type'] = 'input'
                                        temp['inputType'] = 'text'
                                        model[lastoneipromise.attrib['id']] = ''
                                    fields.append(temp)
                                    temp = {}
        schema = {'fields' : fields}
        data = {'model' : model, 'schema': schema}
        bigobj = json.dumps(data)
    return bigobj
