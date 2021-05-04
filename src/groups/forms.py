from django import forms


class GroupForm(forms.Form):
    name = forms.CharField(label='', max_length=50, widget=forms.TextInput(
        attrs={
            'placeholder': 'Group name'
        }
    ))
    overview = forms.CharField(
        label='', widget=forms.Textarea(
            attrs={
                # 'rows': 10, 'cols': 20,
                'class': 'mt-2',
                'placeholder': 'Write a short overview about your group...'
            }))
