# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import tempfile
from django.shortcuts import render
from django.views.generic import TemplateView

from miniproy.forms import LoadFileBPMN

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


def converter(bpmn_archive_path):
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
    return {"output": ET.tostring(grl_root), "input": ET.tostring(bpmn_root)}


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        form = LoadFileBPMN()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        post_values = request.POST.copy()
        form = LoadFileBPMN(post_values, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            result = converter(file)
            context['input'] = result['input']
            context['output'] = result['output']
            context['success'] = "Successful convertion"
            return render(request, 'home.html', context)
        else:
            context = {'form': form}
            return render(request, 'home.html', context)
