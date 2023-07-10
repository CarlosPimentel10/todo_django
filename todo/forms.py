from django import forms

class TaskForm(forms.Form):
    task = forms.CharField(max_length=250)
