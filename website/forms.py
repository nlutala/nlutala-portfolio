from django import forms
from multiupload.fields import MultiFileField


class PDFMergerForm(forms.Form):
    formFileMultiple = MultiFileField(label="Attachments", min_num=2)
    mergedFileName = forms.CharField(label="Merged file name", required=False)
    