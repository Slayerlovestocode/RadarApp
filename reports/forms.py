# reports/forms.py

from django import forms
from .models import Report, EvidenceFile

class ReportForm(forms.ModelForm):
    evidence = forms.FileField(widget=forms.FileInput(), required=False)

    class Meta:
        model = Report
        fields = ['incident_type', 'incident_datetime', 'location', 'description', 'contact_method', 'contact_info']

        # Define common Tailwind classes for form inputs
        input_classes = 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-red-500 focus:border-red-500'

        widgets = {
            'incident_type': forms.Select(attrs={'class': input_classes}),
            'incident_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': input_classes}),
            'location': forms.TextInput(attrs={'class': input_classes}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': input_classes}),
            'contact_method': forms.Select(attrs={'class': input_classes}),
            'contact_info': forms.TextInput(attrs={'class': input_classes}),
        }

        labels = {
            'incident_type': '',
            'incident_datetime': '',
            'location': '',
            'description': '',
            'contact_method': '',
            'contact_info': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['contact_method'].required = False
        self.fields['contact_info'].required = False
        self.fields['evidence'].widget.attrs.update({
            'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'
        })
        self.fields['evidence'].label = ''