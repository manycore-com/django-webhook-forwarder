import hashlib
import traceback
from typing import Dict
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import View
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from webhook_forwarder.forms import ESPConfigForm
from webhook_forwarder.models import WebhookForwarderPollCfg, WebhookForwarderPollEndpoint
from utils import now


class ConfigureESP(LoginRequiredMixin, View):
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
            initial = {}
            for endpoint in WebhookForwarderPollEndpoint.objects.filter(company_id=request.user.company_id).order_by('position'):  # type: WebhookForwarderPollEndpoint
                initial['forward_endpoint' + str(endpoint.position)] = endpoint.forward_endpoint
                initial['is_active' + str(endpoint.position)] = endpoint.is_active

            arg["form"] = ESPConfigForm(initial=initial)

            try:
                obj = WebhookForwarderPollCfg.objects.get(company_id=request.user.company_id)
                self.calc_url(obj, arg)
            except ObjectDoesNotExist as o:
                pass

            return render(request, 'webhook-forwarder/configure_esp.html', arg)
        except Exception as ex:
            messages.error(request, "Page failed: " + str(ex))
            print(traceback.format_exc())
            return render(request, 'empty.html')

    def post(self,
             request: HttpRequest,
             *args, **kwargs) -> HttpResponse:
        try:
            self.request = request
            self.arg = arg = {}
            arg["form"] = form = ESPConfigForm(request.POST)
            if form.is_valid():
                row = None
                try:
                    row = WebhookForwarderPollCfg.objects.get(company_id=request.user.company_id)
                    self.calc_url(row, arg)
                except ObjectDoesNotExist as ex:
                    row = WebhookForwarderPollCfg(company_id=request.user.company_id)
                    row.email_provider = WebhookForwarderPollCfg.EMAIL_PROVIDERS[0][0]
                row.save()

                rows = {}  # type: Dict[int, WebhookForwarderPollEndpoint]
                for endpoint in WebhookForwarderPollEndpoint.objects.filter(company_id=request.user.company_id).order_by('id'):  # type: WebhookForwarderPollEndpoint
                    rows[endpoint.position] = endpoint

                if form.get_forward_endpoint1():
                    if 1 not in rows:
                        rows[1] = WebhookForwarderPollEndpoint(company_id=request.user.company_id, created_at=now(), position=1)
                    rows[1].forward_endpoint = form.get_forward_endpoint1()
                    rows[1].is_active = form.get_is_active1()
                    rows[1].save()
                else:
                    if 1 in rows:
                        rows[1].delete()

                if form.get_forward_endpoint2():
                    if 2 not in rows:
                        rows[2] = WebhookForwarderPollEndpoint(company_id=request.user.company_id, created_at=now(), position=2)
                    rows[2].forward_endpoint = form.get_forward_endpoint2()
                    rows[2].is_active = form.get_is_active2()
                    rows[2].save()
                else:
                    if 2 in rows:
                        rows[2].delete()

                if form.get_forward_endpoint3():
                    if 3 not in rows:
                        rows[3] = WebhookForwarderPollEndpoint(company_id=request.user.company_id, created_at=now(), position=3)
                    rows[3].forward_endpoint = form.get_forward_endpoint3()
                    rows[3].is_active = form.get_is_active3()
                    rows[3].save()
                else:
                    if 3 in rows:
                        rows[3].delete()

                messages.success(request, "saved")
                return redirect('/webhook-forwarder/configure-esp/')

            return render(request, 'webhook-forwarder/configure_esp.html', arg)
        except Exception as ex:
            messages.error(request, "Page failed: " + str(ex))
            print(traceback.format_exc())
            return render(request, 'webhook-forwarder/empty.html')

    def calc_url(self, conf: WebhookForwarderPollCfg, arg):
        hashme = settings.SIMPLE_HASH_PASSWORD + str(conf.company_id)
        simpleHash = hashlib.sha256(hashme.encode('utf-8')).hexdigest()[:32]
        safeHash = hashlib.sha256(conf.secret.encode('utf-8')).hexdigest()[:32]
        arg['webhook_uri'] = settings.GCP_WEBHOOK_BASE + 'v1/' + conf.email_provider + "/" + str(conf.company_id) + "/" + simpleHash + "/" + safeHash + "/"

