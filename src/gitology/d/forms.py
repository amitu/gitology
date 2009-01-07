from django import forms
from django.core.mail import send_mail
from django.conf import settings

from gitology.d import recaptcha_forms

class CommentForm(recaptcha_forms.RecaptchaForm): 
    name = forms.CharField(max_length=100)
    url = forms.URLField(required=False)
    email = forms.EmailField(required=False)
    comment = forms.CharField(widget=forms.Textarea)

    def save(self, document): 
        d = self.cleaned_data.get
        document.replies.append(
            author_name = d("name"),
            email = d("email"),
            url = d("url"),
            comment_content = d("comment"),
        )
        if settings.DEBUG: return
        send_mail(
            'New comment by %s' % d("name"), 
            "www.amitu.com%s" % document.meta.url, 
            'upadhyay+gitology@gmail.com',
            ['upadhyay@gmail.com'], fail_silently=False
        )

