# -*- coding: utf-8 -*-
import tempfile
import xml.etree.cElementTree as ET

from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from miniproy.forms import *
from miniproy.xmlProcessingController import *

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        bpmn_form = LoadFileBPMN()
        grl_form = GRLData()
        context['bpmn_form'] = bpmn_form
        context['grl_form'] = grl_form
        return context

    def post(self, request, *args, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        post_values = request.POST.copy()
        bpmn_form = LoadFileBPMN(post_values, request.FILES)

        if bpmn_form.is_valid():
            file = request.FILES['file']
            result = converter(file)
            grl_form = GRLData({'file_body': result['output']})
            context['input'] = result['input']
            context['grl_form'] = grl_form
            context['success'] = "Successful convertion"
            return render(request, 'home.html', context)
        else:
            context = {'bpmn_form': bpmn_form}
            return render(request, 'home.html', context)

class DownloadGRLFile(View):

    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        grl_form = GRLData(post_values)

        if grl_form.is_valid():
            data = grl_form.cleaned_data
            grl_body = data['file_body']

            tmp = tempfile.TemporaryFile()

            tmp.write(bytes(grl_body, 'UTF-8'))
            tmp.seek(0)
            downloadable_file = FileWrapper(tmp)

            response = HttpResponse(downloadable_file, content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=grldiagram.grl'

            return response