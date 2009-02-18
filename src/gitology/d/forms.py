# imports # {{{
from django import forms
from django.core.mail import send_mail
from django.conf import settings

from gitology.d import recaptcha_forms
# }}}

# EditWikiForm # {{{
class EditWikiForm(recaptcha_forms.RecaptchaForm):
    content = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(max_length=100)
    log = forms.CharField(max_length=100)
    edit = forms.CharField(initial="true", widget=forms.HiddenInput)

    def __init__(self, request, document, *args, **kw):
        super(EditWikiForm, self).__init__(*args, **kw)
        self.fields["name"].initial = request.session.get("stored_name")
        self.fields["content"].initial = document.raw_index
        self.request = request
        self.document = document

    def save(self): 
        d = self.cleaned_data.get
        self.document.raw_index = d("content")
# }}}

# CommentForm # {{{
class CommentForm(recaptcha_forms.RecaptchaForm): 
    name = forms.CharField(max_length=100)
    url = forms.URLField(required=False)
    follow = forms.BooleanField(required=False, initial=True)
    email = forms.EmailField(required=False)
    comment = forms.CharField(widget=forms.Textarea)

    def __init__(self, request, document, *args, **kw):
        super(CommentForm, self).__init__(*args, **kw)
        self.fields["name"].initial = request.session.get("stored_name")
        self.fields["url"].initial = request.session.get("stored_url")
        self.fields["email"].initial = request.session.get("stored_email")
        self.request = request
        self.document = document
    
    def clean_email(self):
        d = self.cleaned_data.get
        if d("follow") and not d("email"):
            raise forms.ValidationError("Email is required if you want to follow discussion")
        return d("email")

    # save # {{{
    def save(self): 
        d = self.cleaned_data.get

        self.document.replies.append(
            author_name = d("name"),
            email = d("email"),
            url = d("url"),
            comment_content = d("comment"),
            follow = d("follow"),
        )

        self.request.session["stored_name"] = d("name")
        self.request.session["stored_url"] = d("url")
        self.request.session["stored_email"] = d("email")

        send_mail(
            'New comment by %s' % d("name"), 
            "www.amitu.com%s" % self.document.meta.url, 
            "no-reply@amitu.com", list(
                set(self.document.replies.get_followers())
            ),
            fail_silently=False
        )

        if settings.DEBUG: return

        email = d("email")
        if not email: email = "upadhyay+gitology@gmail.com"
        send_mail(
            'New comment by %s' % d("name"), 
            "www.amitu.com%s" % self.document.meta.url, 
            email, ['upadhyay@gmail.com'], 
            fail_silently=False
        )
        # }}}
# }}}
