from django import forms

from gitology.d import recaptcha_forms

class CommentForm(recaptcha_forms.RecaptchaForm): 
    name = forms.CharField(max_length=100)
    url = forms.URLField(required=False)
    email = forms.EmailField(required=False)
    comment = forms.CharField(widget=forms.Textarea)

    def save(self, post): 
        d = self.cleaned_data.get
        post["document"].replies.append(
            author_name = d("name"),
            email = d("email"),
            url = d("url"),
            comment_content = d("comment"),
        )
