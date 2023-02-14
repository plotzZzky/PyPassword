from django import forms


class PwdForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title')
        self.username = kwargs.pop('username')
        self.password = kwargs.pop('password')
        self.url = kwargs.pop('url')
        super(PwdForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(
            attrs={'value': self.title, 'placeholder': 'Titulo', 'id': 'titleInput'})
        self.fields['username'].widget = forms.TextInput(
            attrs={'value': self.username, 'placeholder': 'Nome do usario', 'id': 'usernameInput'})
        self.fields['password'].widget = forms.TextInput(
            attrs={'value': self.password, 'placeholder': 'Digite a senha ou no maximo 2 numeros para o tamanho da '
                                                          'senha randomica ', 'id': 'passwordInput'})
        self.fields['url'].widget = forms.TextInput(
            attrs={'value': self.url, 'placeholder': 'Url da pagina', 'id': 'urlInput'})

    title = forms.CharField(max_length=96, label='')
    username = forms.CharField(max_length=255, label='')
    password = forms.CharField(max_length=96, label='')
    url = forms.CharField(max_length=255, label='')

