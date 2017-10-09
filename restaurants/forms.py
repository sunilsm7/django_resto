from django import forms
from .models import RestaurantLocations
from .validators import validate_category

class RestaurantCreateForm(forms.Form):
	name 		= forms.CharField()
	city		= forms.CharField(required=False)
	location 	= forms.CharField(required=False)
	category 	= forms.CharField(required=False)

	def clean_name(self):
		name = self.cleaned_data.get("name")
		if name == "Hello":
			raise forms.ValidationError("Not a valid name")
		return name

class RestaurantLocationCreateForm(forms.ModelForm):
	#email = forms.EmailField()
	#category = forms.CharField(required=False, validators=[validate_category])
	class Meta:
		model = RestaurantLocations
		fields = [
			'name',
			'city',
			'location',
			'category',
		]

	def clean_name(self):
		name = self.cleaned_data.get("name")
		if name == "Hello":
			raise forms.ValidationError("Not a valid name")
		return name

	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
	# 	if ".edu" in email:
	# 		raise forms.ValidationError("We do not accept edu emails")
	# 	return email


class RestaurantSearchForm(forms.Form):
  #CHOICES = (('', 'Reservation_Status',), ('Confirmed', 'Confirmed',), ('Waiting', 'Waiting',))
	name 		= forms.CharField(required=False)
	city		= forms.CharField(required=False)
	location 	= forms.CharField(required=False)
	category 	= forms.CharField(required=False)