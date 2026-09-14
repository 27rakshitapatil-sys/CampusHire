from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:

        model = Job

        fields = [
            "recruiter",
            "title",
            "description",
            "requirements",
            "skills",
            "location",
            "salary",
            "job_type",
            "deadline",
        ]

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Enter job description"
                }
            ),

            "requirements": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Enter job requirements"
                }
            ),

            "skills": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Example: Python, Django, SQL"
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

        }