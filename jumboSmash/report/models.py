from django.core.exceptions import ValidationError
from django.db import models
from users.models import User
import logging


class ReportManger(models.Manager):
    def report(self, reporter, reportee, info):
        if self.filter(reporter=reporter, reportee=reportee, needs_review=True).exists():
            logging.warning("Report already exists for user %d from user %d that needs review.", reportee, reporter)
            raise ValidationError("Report already exists for user %d from user %d that needs review." % (reportee, reporter))

        reportee_user = User.objects.get(id=reportee)
        needs_review = True
        result = None

        if reportee_user.status == User.BANNED:
            needs_review = False
            result = Report.SKIPPED
        else:
            reportee_user.status = User.REPORTED
            reportee_user.save()

        r = self.create(reporter_id=reporter, reportee_id=reportee, info=info, needs_review=needs_review, result=result)

    def ban(self, report_id):
        r = self.get(id=report_id)
        reportee = r.reportee.id

        # set user to banned, skip other reports, mark this report as banned
        User.objects.filter(id=reportee, status=User.REPORTED).update(status=User.BANNED)
        self.filter(reportee=reportee, needs_review=True).exclude(id=report_id).update(needs_review=False, result=Report.SKIPPED)

        r.needs_review = False
        r.result = Report.BANNED
        r.save()

    def dismiss(self, report_id):
        r = self.get(id=report_id)
        reportee = r.reportee.id

        # set user to active only if no other reports are active, mark this report as dismissed
        other_active = self.filter(reportee=reportee, needs_review=True).exclude(id=report_id).exists()
        if not other_active:
            User.objects.filter(id=reportee, status=User.REPORTED).update(status=User.ACTIVE)

        r.needs_review = False
        r.result = Report.DISMISSED
        r.save()


class Report(models.Model):
    BANNED = "B"
    DISMISSED = "D"
    SKIPPED = "S"
    RESULT_CHOICES = ((BANNED, "Banned"), (DISMISSED, "Dismissed"), (SKIPPED, "Skipped"))

    # conditional constraint on unique reporter and reportee for reports that need review enforced
    # at object manager report level. if this becomes cumbersome, set needs_review to nullable and
    # needs_review = False --> needs_review = NULL since null is not checked as unique
    reporter = models.ForeignKey(User, related_name="reporter", on_delete=models.CASCADE)
    reportee = models.ForeignKey(User, related_name="reportee", on_delete=models.CASCADE)
    info = models.TextField()
    report_time = models.DateTimeField(auto_now_add=True)
    # needs_review vs reviewed boolean:
    # a skipped report was not reviewed but it does not need review
    needs_review = models.BooleanField()
    result = models.CharField(max_length=1, choices=RESULT_CHOICES, blank=True, null=True)

    objects = ReportManger()


class ReviewReport(Report):
    class Meta:
        proxy = True
