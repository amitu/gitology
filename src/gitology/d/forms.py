from django import forms
from django.core.mail import send_mail
from django.conf import settings

from gitology.d import recaptcha_forms

class CommentForm(recaptcha_forms.RecaptchaForm): 
    name = forms.CharField(max_length=100)
    url = forms.URLField(required=False)
    follow = forms.BooleanField(required=False, initial=True)
    email = forms.EmailField(required=False)
    comment = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        d = self.cleaned_data.get
        if d("follow") and not d("email"):
            raise forms.ValidationError("Email is required if you want to follow discussion")
        return d("email")

    def save(self, document): 
        d = self.cleaned_data.get
        document.replies.append(
            author_name = d("name"),
            email = d("email"),
            url = d("url"),
            comment_content = d("comment"),
            follow = d("follow"),
        )
        send_mail(
            'New comment by %s' % d("name"), 
            "www.amitu.com%s" % document.meta.url, 
            "no-reply@amitu.com", document.replies.get_followers(),
            fail_silently=False
        )
        if settings.DEBUG: return
        email = d("email")
        if not email: email = "upadhyay+gitology@gmail.com"
        send_mail(
            'New comment by %s' % d("name"), 
            "www.amitu.com%s" % document.meta.url, 
            email, ['upadhyay@gmail.com'], 
            fail_silently=False
        )

