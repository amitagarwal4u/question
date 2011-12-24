from django import forms

TOPIC_CHOICES = (
            ('general', 'General enquiry'),
            ('bug', 'Bug report'),
            ('suggestion', 'Suggestion'),
        )

class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(initial="Replace with your feedback")
    sender = forms.EmailField(required=False)
    def __unicode__(self):
        return self.topic
