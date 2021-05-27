import json
from google.cloud.pubsub_v1 import SubscriberClient
from google.oauth2 import service_account
from google.cloud import pubsub_v1
from django.views.generic.base import View
from google.api_core.exceptions import DeadlineExceeded
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django import db


class DummyRow:

    def __init__(self, created_at):
        self.created_at = created_at
        self.id = None
        self.last_errors = []


class ForwardingDashboardAjax(LoginRequiredMixin, View):
    login_url = "/login/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None
        self.arg = None

    def get(self,
            request: HttpRequest,
            *args, **kwargs) -> HttpResponse:
        try:
            self.request = request
            self.arg = arg = {}

            company_id = request.user.company_id

            db.connections.close_all()
            credentials = service_account.Credentials.from_service_account_info(settings.GOOGLE_CREDENTIALS_DICT)
            pubsub_client = SubscriberClient(credentials=credentials)
            subscription = "projects/" + settings.PROJECT_ID + "/subscriptions/" + settings.PUBSUB_FORWARD_Q1
            pull_response = pubsub_client.pull(subscription=subscription, max_messages=10, timeout=4)  # type: pubsub_v1.types.PullResponse
            ackus = []

            for m in pull_response.received_messages:  # type: pubsub_v1.types.ReceivedMessage
                ackus.append(m.ack_id)

            if ackus:
                ack_deadline_seconds = 0
                pubsub_client.modify_ack_deadline(
                    request={
                        "subscription": subscription,
                        "ack_ids": ackus,
                        "ack_deadline_seconds": ack_deadline_seconds,
                    }
                )

            messages = []
            for m in pull_response.received_messages:  # type: pubsub_v1.types.ReceivedMessage
                datastruct = json.loads(m.message.data.decode('utf-8'))
                if 'CompanyID' in datastruct:
                    if company_id == datastruct['CompanyID']:
                        messages.append(datastruct)

            return JsonResponse(data={'ok': True, 'q1': messages})

        except DeadlineExceeded as ex:
            return JsonResponse(data={'ok': True, 'q1': []})
        except Exception as ex:
            return JsonResponse(status=400, data={'ok': False, 'msg': 'Error: ' + str(ex)})



