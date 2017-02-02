from django.forms import forms


class LoadFileBPMN(forms.Form):
    file = forms.FileField(help_text='Solo archivos .bpmn')

    def clean_archivo(self):
        file = self.cleaned_data.get('archivo', False)
        #filetype = file.content_type
        #if not filetype in ["text/csv","application/vnd.ms-excel"]:
        #   raise forms.ValidationError("El archivo no es .BPMN ")
        return file

    def __init__(self,*args,**kwargs):
        super(LoadFileBPMN,self).__init__(*args,**kwargs)
        self.fields['file'].widget.attrs['accept'] = '.bpmn'
        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'