from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from rest_framework.views import APIView
from report.models import Report
import logging


class ReportView(APIView):
    """Report a user"""
    def post(self, request):
        reporter = int(request.user.id)
        reportee = int(request.data.get("user"))
        info = request.data.get("info")
        data = { "detail": "Reported." }

        try:
            Report.objects.report(reporter, reportee, info)
        except ObjectDoesNotExist:
            data["detail"] = "User being reported not found."
            return Response(data, status=HTTP_404_NOT_FOUND)
        except ValidationError:
            data["detail"] = "Your previous report for this user is being reviewed."
            return Response(data, status=HTTP_409_CONFLICT)

        return Response(data)
