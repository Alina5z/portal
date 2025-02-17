from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'photo', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class RequestStatusForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'rejection_reason']
        widgets = {
            'rejection_reason': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        rejection_reason = cleaned_data.get('rejection_reason')

        if status == 'rejected' and not rejection_reason:
            raise forms.ValidationError(
                "При отказе в заявке следует указать причину"
            )
