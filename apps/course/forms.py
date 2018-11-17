from django import forms
from ..operation.models import CourseComments


class AddCommentForm(forms.Form):
    comments = forms.CharField()
    course_id = forms.CharField()

