from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

def clean_email(self):
		email = self.cleaned_data.get('email')
		if ".edu" in email:
			raise forms.ValidationError("We do not accept edu emails")

CATEGORIES = ["Mexican", "Asian", "American", "Indian", "Chinese"]			

def validate_category(value):
	cat = value.capitalize()
	if not value in CATEGORIES and not cat in CATEGORIES:
		raise ValidationError("{}".format(value +"  is not a valid category"))