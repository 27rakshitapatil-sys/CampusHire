from django import forms


class ApplicationForm(forms.Form):

    name = forms.CharField(
        required=True,
        error_messages={
            'required': 'Full Name is required.'
        }
    )

    email = forms.EmailField(
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.'
        }
    )

    phone = forms.CharField(
        required=True,
        error_messages={
            'required': 'Phone Number is required.'
        }
    )

    resume = forms.FileField(
        required=True,
        error_messages={
            'required': 'Resume is required.'
        }
    )

    cover_letter = forms.CharField(
        required=True,
        error_messages={
            'required': 'Cover Letter is required.'
        }
    )