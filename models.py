import uuid
import datetime
from django.db import models
from users.models import Company
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class WebhookForwarderPollCfg(models.Model):
    EMAIL_PROVIDERS = [
        ("sg", "Sendgrid"),
    ]

    created_at = models.DateTimeField(editable=False, default=datetime.datetime.utcnow, null=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, related_name='wh_pollcfg_company_fk')
    email_provider = models.CharField(max_length=4, null=False, choices=EMAIL_PROVIDERS)
    secret = models.CharField(max_length=36, default=uuid.uuid4, null=True)

    class Meta:
        db_table = 'webhook_forwarder_poll_cfg'


class WebhookForwarderPollEndpoint(models.Model):
    created_at = models.DateTimeField(editable=False, default=datetime.datetime.utcnow, null=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, related_name='wh_pollendpoint_company_fk')
    forward_endpoint = models.URLField(max_length=300, null=True)
    is_active = models.BooleanField(default=True, null=False)
    position = models.SmallIntegerField(default=1, choices=[(1, "1"), (2, "2"), (3, "3")], null=False)

    class Meta:
        db_table = 'webhook_forwarder_poll_endpoint'
        constraints = [
            models.UniqueConstraint(fields=['company_id', 'position'], name="wf_pollendpoint_cidpost_uniq")
        ]


def _zero24():
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def _empty():
    return []


class DailyForwardStats(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=False, related_name='wh_dailydorwarddtats_company_fk')
    created_at = models.DateTimeField(editable=False, null=False)

    q1_h00 = models.IntegerField(default=0, null=False)
    q1_h01 = models.IntegerField(default=0, null=False)
    q1_h02 = models.IntegerField(default=0, null=False)
    q1_h03 = models.IntegerField(default=0, null=False)
    q1_h04 = models.IntegerField(default=0, null=False)
    q1_h05 = models.IntegerField(default=0, null=False)
    q1_h06 = models.IntegerField(default=0, null=False)
    q1_h07 = models.IntegerField(default=0, null=False)
    q1_h08 = models.IntegerField(default=0, null=False)
    q1_h09 = models.IntegerField(default=0, null=False)
    q1_h10 = models.IntegerField(default=0, null=False)
    q1_h11 = models.IntegerField(default=0, null=False)
    q1_h12 = models.IntegerField(default=0, null=False)
    q1_h13 = models.IntegerField(default=0, null=False)
    q1_h14 = models.IntegerField(default=0, null=False)
    q1_h15 = models.IntegerField(default=0, null=False)
    q1_h16 = models.IntegerField(default=0, null=False)
    q1_h17 = models.IntegerField(default=0, null=False)
    q1_h18 = models.IntegerField(default=0, null=False)
    q1_h19 = models.IntegerField(default=0, null=False)
    q1_h20 = models.IntegerField(default=0, null=False)
    q1_h21 = models.IntegerField(default=0, null=False)
    q1_h22 = models.IntegerField(default=0, null=False)
    q1_h23 = models.IntegerField(default=0, null=False)

    q2_h00 = models.IntegerField(default=0, null=False)
    q2_h01 = models.IntegerField(default=0, null=False)
    q2_h02 = models.IntegerField(default=0, null=False)
    q2_h03 = models.IntegerField(default=0, null=False)
    q2_h04 = models.IntegerField(default=0, null=False)
    q2_h05 = models.IntegerField(default=0, null=False)
    q2_h06 = models.IntegerField(default=0, null=False)
    q2_h07 = models.IntegerField(default=0, null=False)
    q2_h08 = models.IntegerField(default=0, null=False)
    q2_h09 = models.IntegerField(default=0, null=False)
    q2_h10 = models.IntegerField(default=0, null=False)
    q2_h11 = models.IntegerField(default=0, null=False)
    q2_h12 = models.IntegerField(default=0, null=False)
    q2_h13 = models.IntegerField(default=0, null=False)
    q2_h14 = models.IntegerField(default=0, null=False)
    q2_h15 = models.IntegerField(default=0, null=False)
    q2_h16 = models.IntegerField(default=0, null=False)
    q2_h17 = models.IntegerField(default=0, null=False)
    q2_h18 = models.IntegerField(default=0, null=False)
    q2_h19 = models.IntegerField(default=0, null=False)
    q2_h20 = models.IntegerField(default=0, null=False)
    q2_h21 = models.IntegerField(default=0, null=False)
    q2_h22 = models.IntegerField(default=0, null=False)
    q2_h23 = models.IntegerField(default=0, null=False)

    q3_h00 = models.IntegerField(default=0, null=False)
    q3_h01 = models.IntegerField(default=0, null=False)
    q3_h02 = models.IntegerField(default=0, null=False)
    q3_h03 = models.IntegerField(default=0, null=False)
    q3_h04 = models.IntegerField(default=0, null=False)
    q3_h05 = models.IntegerField(default=0, null=False)
    q3_h06 = models.IntegerField(default=0, null=False)
    q3_h07 = models.IntegerField(default=0, null=False)
    q3_h08 = models.IntegerField(default=0, null=False)
    q3_h09 = models.IntegerField(default=0, null=False)
    q3_h10 = models.IntegerField(default=0, null=False)
    q3_h11 = models.IntegerField(default=0, null=False)
    q3_h12 = models.IntegerField(default=0, null=False)
    q3_h13 = models.IntegerField(default=0, null=False)
    q3_h14 = models.IntegerField(default=0, null=False)
    q3_h15 = models.IntegerField(default=0, null=False)
    q3_h16 = models.IntegerField(default=0, null=False)
    q3_h17 = models.IntegerField(default=0, null=False)
    q3_h18 = models.IntegerField(default=0, null=False)
    q3_h19 = models.IntegerField(default=0, null=False)
    q3_h20 = models.IntegerField(default=0, null=False)
    q3_h21 = models.IntegerField(default=0, null=False)
    q3_h22 = models.IntegerField(default=0, null=False)
    q3_h23 = models.IntegerField(default=0, null=False)

    l_h00 = models.IntegerField(default=0, null=False)
    l_h01 = models.IntegerField(default=0, null=False)
    l_h02 = models.IntegerField(default=0, null=False)
    l_h03 = models.IntegerField(default=0, null=False)
    l_h04 = models.IntegerField(default=0, null=False)
    l_h05 = models.IntegerField(default=0, null=False)
    l_h06 = models.IntegerField(default=0, null=False)
    l_h07 = models.IntegerField(default=0, null=False)
    l_h08 = models.IntegerField(default=0, null=False)
    l_h09 = models.IntegerField(default=0, null=False)
    l_h10 = models.IntegerField(default=0, null=False)
    l_h11 = models.IntegerField(default=0, null=False)
    l_h12 = models.IntegerField(default=0, null=False)
    l_h13 = models.IntegerField(default=0, null=False)
    l_h14 = models.IntegerField(default=0, null=False)
    l_h15 = models.IntegerField(default=0, null=False)
    l_h16 = models.IntegerField(default=0, null=False)
    l_h17 = models.IntegerField(default=0, null=False)
    l_h18 = models.IntegerField(default=0, null=False)
    l_h19 = models.IntegerField(default=0, null=False)
    l_h20 = models.IntegerField(default=0, null=False)
    l_h21 = models.IntegerField(default=0, null=False)
    l_h22 = models.IntegerField(default=0, null=False)
    l_h23 = models.IntegerField(default=0, null=False)

    last_errors = ArrayField(
        models.CharField(max_length=100, null=False),
        null=False,
        default=_empty
    )

    # Successful
    s_h00 = models.IntegerField(default=0, null=False)
    s_h01 = models.IntegerField(default=0, null=False)
    s_h02 = models.IntegerField(default=0, null=False)
    s_h03 = models.IntegerField(default=0, null=False)
    s_h04 = models.IntegerField(default=0, null=False)
    s_h05 = models.IntegerField(default=0, null=False)
    s_h06 = models.IntegerField(default=0, null=False)
    s_h07 = models.IntegerField(default=0, null=False)
    s_h08 = models.IntegerField(default=0, null=False)
    s_h09 = models.IntegerField(default=0, null=False)
    s_h10 = models.IntegerField(default=0, null=False)
    s_h11 = models.IntegerField(default=0, null=False)
    s_h12 = models.IntegerField(default=0, null=False)
    s_h13 = models.IntegerField(default=0, null=False)
    s_h14 = models.IntegerField(default=0, null=False)
    s_h15 = models.IntegerField(default=0, null=False)
    s_h16 = models.IntegerField(default=0, null=False)
    s_h17 = models.IntegerField(default=0, null=False)
    s_h18 = models.IntegerField(default=0, null=False)
    s_h19 = models.IntegerField(default=0, null=False)
    s_h20 = models.IntegerField(default=0, null=False)
    s_h21 = models.IntegerField(default=0, null=False)
    s_h22 = models.IntegerField(default=0, null=False)
    s_h23 = models.IntegerField(default=0, null=False)

    last_hour_with_examples = models.SmallIntegerField(default=-1, null=False)
    total_incoming_messages = models.SmallIntegerField(default=0, null=False)

    def get_failures_hourly(self):
        return [
            self.q2_h00 + self.q3_h00 + self.l_h00,
            self.q2_h01 + self.q3_h01 + self.l_h01,
            self.q2_h02 + self.q3_h02 + self.l_h02,
            self.q2_h03 + self.q3_h03 + self.l_h03,
            self.q2_h04 + self.q3_h04 + self.l_h04,
            self.q2_h05 + self.q3_h05 + self.l_h05,
            self.q2_h06 + self.q3_h06 + self.l_h06,
            self.q2_h07 + self.q3_h07 + self.l_h07,
            self.q2_h08 + self.q3_h08 + self.l_h08,
            self.q2_h09 + self.q3_h09 + self.l_h09,
            self.q2_h10 + self.q3_h10 + self.l_h10,
            self.q2_h11 + self.q3_h11 + self.l_h11,
            self.q2_h12 + self.q3_h12 + self.l_h12,
            self.q2_h13 + self.q3_h13 + self.l_h13,
            self.q2_h14 + self.q3_h14 + self.l_h14,
            self.q2_h15 + self.q3_h15 + self.l_h15,
            self.q2_h16 + self.q3_h16 + self.l_h16,
            self.q2_h17 + self.q3_h17 + self.l_h17,
            self.q2_h18 + self.q3_h18 + self.l_h18,
            self.q2_h19 + self.q3_h19 + self.l_h19,
            self.q2_h20 + self.q3_h20 + self.l_h20,
            self.q2_h21 + self.q3_h21 + self.l_h21,
            self.q2_h22 + self.q3_h22 + self.l_h22,
            self.q2_h23 + self.q3_h23 + self.l_h23
        ]

    class Meta:
        db_table = 'webhook_forwarder_daily_forward_stats'

        constraints = [
            models.UniqueConstraint(fields=['company_id', 'created_at'], name="wh_dailyforwardstats_uniq"),
        ]


class LatestForwardExamples(models.Model):
    company = models.OneToOneField(Company, on_delete=models.PROTECT, null=False, related_name='wh_latestforwardexamples_company_fk')
    created_at = models.DateTimeField(editable=True, null=False)
    ex1 = models.CharField(max_length=1024, null=True)
    ex2 = models.CharField(max_length=1024, null=True)
    ex3 = models.CharField(max_length=1024, null=True)
    ex4 = models.CharField(max_length=1024, null=True)
    circular_pointer_0to3 = models.SmallIntegerField(default=0, null=False)

    class Meta:
        db_table = 'webhook_forwarder_latest_forward_examples'
