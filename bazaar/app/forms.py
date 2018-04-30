from django import forms
from dal_select2.widgets import ModelSelect2Multiple
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.helper import FormHelper
from app.models import Tag, Advertisement

from django import forms
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
# from app.models import 

# class HorizontalCheckboxRenderer(forms.CheckboxSelectMultiple.renderer):
#     def render(self):
#         id_ = self.attrs.get('id', None)
#         start_tag = format_html('<div id="{0}">', id_) if id_ else '<div>'
#         output = [start_tag]
#         for widget in self:
#             output.append(format_html(u'<span>{0}</span>', force_text(widget)))
#         output.append('</span>')
#         return mark_safe('\n'.join(output))

class SignUpForm(forms.Form):
	name = forms.CharField(max_length = 100)
	username = forms.CharField(max_length = 100)
	email = forms.CharField(max_length = 100)
	phone = forms.IntegerField()
	password = forms.CharField(widget = forms.PasswordInput())
	image = forms.ImageField()
	#tags = forms.ModelMultipleChoiceField(
	#	queryset = Tag.objects.all(),
	#	widget = forms.CheckboxSelectMultiple(),
	#	help_text = "<strong>Note:</strong> Select relevant tags from the above.",

#	)
	def __init__(self, *args, **kwargs):		
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'name',
			'username',
			'email',
			'phone',
			'password',
			'image',
			'tags',
			Submit('submit', u'Submit', css_class='btn btn-success'), 
	)

class AdForm(forms.Form):
	title= forms.CharField(max_length = 100)
	description= forms.CharField(max_length = 200)
	price =forms.FloatField()
	image = forms.ImageField()
	tags = forms.ModelMultipleChoiceField(
		queryset = Tag.objects.all(),
		widget = forms.CheckboxSelectMultiple(),
		help_text = "<strong>Note:</strong> Select relevant tags from the above.",
	)
	def __init__(self, *args, **kwargs):		
		super(AdForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'title',
			'description',
			'price',
			'image',
            'tags',
			Submit('submit', u'Submit', css_class='btn btn-success'), 
	)


class AddTagForm(forms.Form):
	tag = forms.CharField(max_length = 100)
	def __init__(self, *args, **kwargs):		
		super(AddTagForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'tag',
			Submit('submit', u'Add', css_class='btn btn-success'), 
	)
class RemoveTagForm(forms.Form):
	tags = forms.ModelMultipleChoiceField(
		queryset = Tag.objects.all(),
		widget = forms.CheckboxSelectMultiple(),
		help_text = "<strong>Note:</strong> Select relevant tags to remove.",

	)
	def __init__(self, *args, **kwargs):		
		super(RemoveTagForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'tags',
			Submit('submit', u'Remove', css_class='btn btn-success'), 
	)


class BidForm(forms.Form):
	bid = forms.FloatField()
	comment=forms.CharField(required=False)
	def __init__(self, *args, **kwargs):		
		super(BidForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'bid',
			'comment',
			Submit('submit', u'Add', css_class='btn btn-success'), 
	)