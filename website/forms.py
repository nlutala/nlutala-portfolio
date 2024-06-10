from django import forms


class PDFMergerForm(forms.Form):
    formFileMultiple = forms.FileField()
    mergedFileName = forms.CharField(label="Merged file name")
    