from django import forms


class LoadFileBPMN(forms.Form):
    file = forms.FileField(help_text='Only .bpmn files')

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

class GRLData(forms.Form):
    file_body = forms.CharField(widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        super(GRLData,self).__init__(*args,**kwargs)
        for key in self.fields:
            self.fields[key].required = True
            self.fields[key].widget.attrs['required'] = 'True'

