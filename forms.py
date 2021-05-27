from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit
from django import forms


class ESPConfigForm(forms.Form):

    # email_provider = forms.CharField(
    #     label='Email Service Provider',
    #     widget=forms.Select(choices=WebhookForwarderPollCfg.EMAIL_PROVIDERS),
    #     required=True
    # )

    forward_endpoint1 = forms.CharField(
        label='Forward Endpoint 1',
        max_length=300,
        required=False,
        help_text='Optional: If set, all incoming webhook events are forwarded to this endpoint.'
    )

    is_active1 = forms.BooleanField(
        label='Is Active',
        required=False,
        help_text='If there are too many forwarding errors, forwarding will be disabled.'
    )

    forward_endpoint2 = forms.CharField(
        label='Forward Endpoint 2',
        max_length=300,
        required=False,
        help_text='Optional: If set, all incoming webhook events are forwarded to this endpoint too.'
    )

    is_active2 = forms.BooleanField(
        label='Is Active',
        required=False,
        help_text='If there are too many forwarding errors, forwarding will be disabled.'
    )

    forward_endpoint3 = forms.CharField(
        label='Forward Endpoint 2',
        max_length=300,
        required=False,
        help_text='Optional: If set, all incoming webhook events are forwarded to this endpoint as well.'
    )

    is_active3 = forms.BooleanField(
        label='Is Active',
        required=False,
        help_text='If there are too many forwarding errors, forwarding will be disabled.'
    )

    def get_email_provider(self):
        return "sg"
        # return self.cleaned_data['email_provider']

    def get_forward_endpoint1(self):
        return self.cleaned_data['forward_endpoint1']

    def get_is_active1(self):
        return self.cleaned_data['is_active1']

    def get_forward_endpoint2(self):
        return self.cleaned_data['forward_endpoint2']

    def get_is_active2(self):
        return self.cleaned_data['is_active2']

    def get_forward_endpoint3(self):
        return self.cleaned_data['forward_endpoint3']

    def get_is_active3(self):
        return self.cleaned_data['is_active3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            'forward_endpoint1',
            'is_active1',
            'forward_endpoint2',
            'is_active2',
            'forward_endpoint3',
            'is_active3',

            ButtonHolder(
                Submit('post', 'Post', css_class='btn-primary')
            )
        )

