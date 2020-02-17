from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import re_path, reverse
from report.models import Report, ReportObject


class ReportObjectAdmin(admin.ModelAdmin):
    list_display = ["reporter", "reportee", "report_time", "needs_review", "result"]
    ordering = ["-needs_review", "-report_time"]
    search_fields = ["reporter__email", "reportee__email", "info"]
    fields = ["reporter", "reportee", "info", "report_time", "needs_review", "result"]
    readonly_fields = ["report_time"]


class ReportAdmin(ReportObjectAdmin):
    list_display = ["reporter", "reportee", "report_time", "needs_review"]
    ordering = ["-needs_review", "report_time"]
    readonly_fields = ["reporter", "reportee", "info", "report_time", "needs_review", "result"]

    def get_queryset(self, request):
        return self.model.objects.filter(needs_review=True)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<report_id>.+)/ban/$',
                self.admin_site.admin_view(self.ban),
                name='report-ban',
            ),
            re_path(
                r'^(?P<report_id>.+)/dismiss/$',
                self.admin_site.admin_view(self.dismiss),
                name='report-dismiss',
            ),
        ]
        return custom_urls + urls

    def ban(self, request, report_id, *args, **kwargs):
        Report.objects.review(report_id, "ban")
        return HttpResponseRedirect(reverse("admin:report_report_changelist"))

    def dismiss(self, request, report_id, *args, **kwargs):
        Report.objects.review(report_id, "dismiss")
        return HttpResponseRedirect(reverse("admin:report_report_changelist"))


admin.site.register(ReportObject, ReportObjectAdmin)
admin.site.register(Report, ReportAdmin)