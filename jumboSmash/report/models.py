from django.db import models
from users.models import User


class ReportManger(models.Manager):
    def report(self, reporter, reportee, info):
        num_matched = User.objects.filter(id=reportee).exclude(status=User.BANNED).update(status=User.REPORTED)
        needs_review = True
        result = None
        if not num_matched:
            # if num_matched is 0, user was already banned (or user doesn't exist)
            needs_review = False
            result = Report.SKIPPED

        r = self.create(reporter_id=reporter, reportee_id=reportee, info=info, needs_review=needs_review, result=result)

    def review(self, request_id, action):
        r = self.get(id=request_id)
        reportee = r.reportee.id
        result = None

        if action == "ban":
            # set user to banned, skip other reports, mark this report as banned
            User.objects.filter(id=reportee, status=User.REPORTED).update(status=User.BANNED)
            self.filter(reportee=reportee, needs_review=True).exclude(id=request_id).update(needs_review=False, result=Report.SKIPPED)
            result = Report.BANNED
        elif action == "dismiss":
            # set user to active only if no other reports are active, mark this report as dismissed
            other_active = self.filter(reportee=reportee, needs_review=True).exclude(id=request_id).exists()
            if not other_active:
                User.objects.filter(id=reportee, status=User.REPORTED).update(status=User.ACTIVE)
            result = Report.DISMISSED

        r.needs_review = False
        r.result = result
        r.save()


class Report(models.Model):
    BANNED = "B"
    DISMISSED = "D"
    SKIPPED = "S"
    RESULT_CHOICES = ((BANNED, "Banned"), (DISMISSED, "Dismissed"), (SKIPPED, "Skipped"))

    reporter = models.ForeignKey(User, related_name="reporter", on_delete=models.CASCADE)
    reportee = models.ForeignKey(User, related_name="reportee", on_delete=models.CASCADE)
    info = models.TextField()
    report_time = models.DateTimeField(auto_now_add=True)
    needs_review = models.BooleanField()
    result = models.CharField(max_length=1, choices=RESULT_CHOICES, blank=True)

    objects = ReportManger()


class ReportObject(Report):
    class Meta:
        proxy = True
