from events.models import *
from django import forms
# class NoteForm(forms.ModelForm):
# 	class Meta:
# 		model = Note
# 		fields ='__all__'
from ckeditor.widgets import CKEditorWidget
class NoteForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Note
		fields = '__all__'


from django.contrib.auth.models import User  

 

class SupportForm(forms.ModelForm): 
	# email=forms.CharField(max_length=128,  required=False, widget=forms.EmailInput())
	image=forms.FileField(max_length=128,  required=False, )
	class Meta():

		model = SpiritualSupportRequest
		fields = ('name',"description","image")


# from upload_validator import FileTypeValidator
from django.core.exceptions import ValidationError
def file_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 9 MiB.')


class TeamEditionForm(forms.ModelForm): 
	image=forms.FileField(  required=False)#,  validators=[file_size],)

	class Meta:
		model = Teamedition
		fields=["title","content","image"]
		# fields = '__all__'




# from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

# # # # Apply summernote to specific fields.
# class NoteForm2(forms.Form):
#     foo = forms.CharField(widget=SummernoteWidget()) 


# class FormFromSomeModel(forms.ModelForm):
#     class Meta:
#         model = SomeModel
#         widgets = {
#             'foo': SummernoteWidget(),
#             'bar': SummernoteInplaceWidget(),
#         }