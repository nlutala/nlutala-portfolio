from django import forms
from multiupload.fields import MultiFileField


class PDFMergerForm(forms.Form):
    uploadedFiles = MultiFileField()
    mergedFilename = forms.CharField(label="Merged file name", required=False)
