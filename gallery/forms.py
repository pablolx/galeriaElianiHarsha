from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label="Nome", max_length=120)
    email = forms.EmailField(label="E-mail")
    subject = forms.CharField(label="Assunto", max_length=160)
    message = forms.CharField(
        label="Mensagem",
        widget=forms.Textarea(attrs={"rows": 6}),
    )

    def clean_subject(self):
        return " ".join(self.cleaned_data["subject"].splitlines())
