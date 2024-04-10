from django import forms


class NewArticleForm(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6"}
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control col-md-10",
                'rows': 8,
            }
        )
    )


class EditArticleForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control col-md-10",
                'rows': 8,
            }
        )
    )
