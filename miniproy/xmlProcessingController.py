# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

convertion_dict = {"process": "hardgoal",
                   "subprocess": "hardgoal",
                   "pool": "actor",
                   "lane": "role",
                   "task": "task",
                   "labeledassociation": "softgoal",
                   "dataobject": "resource",
                   "gateway": "taskdescompositionlink",
                   "sequenceflow": "meansendlink",
                   "messageflow": "dependencylink"
                   }


def bpmnToGRLConvertion(bpmn_archive_path):
    try:
        bpmn_tree = ET.parse(bpmn_archive_path)
    except:
        print("El archivo especificado no existe.")
        return None

    bpmn_root = bpmn_tree.getroot()

    grl_root = ET.Element('data')
    id_count = 1

    for bpmn_element in list(bpmn_root):
        bpmn_element_tag = bpmn_element.tag
        if bpmn_element_tag in list(convertion_dict.keys()):
            new_grl_child = ET.SubElement(
                grl_root,
                convertion_dict[bpmn_element_tag]
            )
            new_grl_child.set('id', str(id_count))
            id_count += 1
            new_grl_child_name = ET.SubElement(new_grl_child, 'name')

            new_grl_child_name.text = bpmn_element.find('name').text
        else:
            print("Error, el archivo no es válido.")
            return None
    return ET.dump(grl_root)
