from rest_framework.response import Response
from rest_framework.views import APIView
from report.models import Report


class ReportView(APIView):
    """Report a user"""
    def post(self, request):
        reporter = request.user.id
        reportee = request.data.get("user")
        info = request.data.get("info")

        Report.objects.report(reporter, reportee, info)

        return Response("reported")
