from django.db import models
from users.models import User

class ReportManger(models.Manager):
    pass

class Report (models.Model):
    reporter = models.ForeignKey(User, related_name="reporter", on_delete=models.CASCADE)
    reportee = models.ForeignKey(User, related_name="reportee", on_delete=models.CASCADE)
    info = models.TextField()

    objects = ReportManger()
