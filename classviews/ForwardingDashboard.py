import traceback
import datetime
import datetime_truncate
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from webhook_forwarder.models import DailyForwardStats, WebhookForwarderPollCfg, WebhookForwarderPollEndpoint, LatestForwardExamples


class DummyRow:

    def __init__(self, created_at):
        self.created_at = created_at
        self.id = None
        self.last_errors = []

    @staticmethod
    def get_failures_hourly(self):
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


class ForwardingDashboard(LoginRequiredMixin, View):
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

            arg["pollCfg"] = pollCfg = WebhookForwarderPollCfg.objects.get(company_id=request.user.company_id)

            isActive = False
            for row in WebhookForwarderPollEndpoint.objects.filter(company_id=request.user.company_id):  # type: WebhookForwarderPollEndpoint
                if row.is_active:
                    isActive = True
            arg["isActive"] = isActive

            arg['sorted_array'] = sorted_array = []

            array_of_dates = []
            a_date = datetime_truncate.truncate_day(datetime.datetime.utcnow() - datetime.timedelta(days=3))
            while a_date < datetime.datetime.utcnow():
                array_of_dates.append(a_date)
                a_date += datetime.timedelta(days=1)

            loaded = {}
            for x in DailyForwardStats.objects.filter(company_id=request.user.company_id,
                                                      created_at__gte=array_of_dates[0]):  # type: DailyForwardStats
                loaded[datetime_truncate.truncate_day(x.created_at)] = x

            for aDate in array_of_dates:
                if aDate in loaded:
                    sorted_array.append(loaded[aDate])
                else:
                    sorted_array.append(DummyRow(aDate))

            arg["yday"] = yday = array_of_dates[-2:][0]
            arg["today"] = today = array_of_dates[-2:][1]

            if yday not in loaded:
                arg["yday_events_received"] = 0
                arg["yday_forwarded_ok"] = 0
                arg["yday_forwarded_nok"] = 0
            else:
                x = loaded[yday]
                arg["yday_events_received"] = x.total_incoming_messages
                arg["yday_forwarded_ok"] = (
                        x.s_h00 + x.s_h01 + x.s_h02 + x.s_h03 + x.s_h04 + x.s_h05 + x.s_h06 + x.s_h07 + x.s_h08 + x.s_h09 + x.s_h10 + x.s_h11 +
                        x.s_h12 + x.s_h13 + x.s_h14 + x.s_h15 + x.s_h16 + x.s_h17 + x.s_h18 + x.s_h19 + x.s_h20 + x.s_h21 + x.s_h22 + x.s_h23
                )
                arg["yday_forwarded_nok"] = (
                        x.q2_h00 + x.q2_h01 + x.q2_h02 + x.q2_h03 + x.q2_h04 + x.q2_h05 + x.q2_h06 + x.q2_h07 + x.q2_h08 + x.q2_h09 + x.q2_h10 + x.q2_h11 +
                        x.q2_h12 + x.q2_h13 + x.q2_h14 + x.q2_h15 + x.q2_h16 + x.q2_h17 + x.q2_h18 + x.q2_h19 + x.q2_h20 + x.q2_h21 + x.q2_h22 + x.q2_h23 +
                        x.q3_h00 + x.q3_h01 + x.q3_h02 + x.q3_h03 + x.q3_h04 + x.q3_h05 + x.q3_h06 + x.q3_h07 + x.q3_h08 + x.q3_h09 + x.q3_h10 + x.q3_h11 +
                        x.q3_h12 + x.q3_h13 + x.q3_h14 + x.q3_h15 + x.q3_h16 + x.q3_h17 + x.q3_h18 + x.q3_h19 + x.q3_h20 + x.q3_h21 + x.q3_h22 + x.q3_h23 +
                        x.l_h00 + x.l_h01 + x.l_h02 + x.l_h03 + x.l_h04 + x.l_h05 + x.l_h06 + x.l_h07 + x.l_h08 + x.l_h09 + x.l_h10 + x.l_h11 +
                        x.l_h12 + x.l_h13 + x.l_h14 + x.l_h15 + x.l_h16 + x.l_h17 + x.l_h18 + x.l_h19 + x.l_h20 + x.l_h21 + x.l_h22 + x.l_h23
                )

            if today not in loaded:
                arg["today_events_received"] = 0
                arg["today_forwarded_ok"] = 0
                arg["today_forwarded_nok"] = 0
            else:
                x = loaded[today]
                arg["today_events_received"] = x.total_incoming_messages
                arg["today_forwarded_ok"] = (
                        x.s_h00 + x.s_h01 + x.s_h02 + x.s_h03 + x.s_h04 + x.s_h05 + x.s_h06 + x.s_h07 + x.s_h08 + x.s_h09 + x.s_h10 + x.s_h11 +
                        x.s_h12 + x.s_h13 + x.s_h14 + x.s_h15 + x.s_h16 + x.s_h17 + x.s_h18 + x.s_h19 + x.s_h20 + x.s_h21 + x.s_h22 + x.s_h23
                )
                arg["today_forwarded_nok"] = (
                        x.q2_h00 + x.q2_h01 + x.q2_h02 + x.q2_h03 + x.q2_h04 + x.q2_h05 + x.q2_h06 + x.q2_h07 + x.q2_h08 + x.q2_h09 + x.q2_h10 + x.q2_h11 +
                        x.q2_h12 + x.q2_h13 + x.q2_h14 + x.q2_h15 + x.q2_h16 + x.q2_h17 + x.q2_h18 + x.q2_h19 + x.q2_h20 + x.q2_h21 + x.q2_h22 + x.q2_h23 +
                        x.q3_h00 + x.q3_h01 + x.q3_h02 + x.q3_h03 + x.q3_h04 + x.q3_h05 + x.q3_h06 + x.q3_h07 + x.q3_h08 + x.q3_h09 + x.q3_h10 + x.q3_h11 +
                        x.q3_h12 + x.q3_h13 + x.q3_h14 + x.q3_h15 + x.q3_h16 + x.q3_h17 + x.q3_h18 + x.q3_h19 + x.q3_h20 + x.q3_h21 + x.q3_h22 + x.q3_h23 +
                        x.l_h00 + x.l_h01 + x.l_h02 + x.l_h03 + x.l_h04 + x.l_h05 + x.l_h06 + x.l_h07 + x.l_h08 + x.l_h09 + x.l_h10 + x.l_h11 +
                        x.l_h12 + x.l_h13 + x.l_h14 + x.l_h15 + x.l_h16 + x.l_h17 + x.l_h18 + x.l_h19 + x.l_h20 + x.l_h21 + x.l_h22 + x.l_h23
                )

            # This is to load last few events:
            try:
                obj = LatestForwardExamples.objects.get(company_id=request.user.company_id)
                arg["eventExample1"] = obj.ex1
                arg["eventExample2"] = obj.ex2
                arg["eventExample3"] = obj.ex3
                arg["eventExample4"] = obj.ex4
            except ObjectDoesNotExist as ex:
                arg["eventExample1"] = None
                arg["eventExample2"] = None
                arg["eventExample3"] = None
                arg["eventExample4"] = None

            return render(request, 'webhook-forwarder/forwarding_dashboard.html', arg)
        except ObjectDoesNotExist as ex:
            messages.warning(request,
                             "Forwarding has not been <a href=\"/webhook-forwarder/configure-esp/\">configured yet</a>.")
            return render(request, 'webhook-forwarder/empty.html')
        except Exception as ex:
            print(traceback.format_exc())
            messages.error(request, "Page failed: " + str(ex))
            return render(request, 'webhook-forwarder/empty.html')
