from rest_framework.response import Response
from .tasks.tasks import tasks

from .models import CVES, ResultScan, InfectionRate, Protocols
from .serializers import CVESSerializer, ResultScanSerializer, InfectionRateSerializer, ProtocolsSerializer, \
    ScanSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet


def define_targets():
    from django.conf import settings
    content_from_file = open(str(settings.BASE_DIR) + '/result.txt', "r").read().split("\n")
    return [(str(ind), element) for ind, element in enumerate(content_from_file)]


def get_cves():
    cves = CVES.objects.all()
    return [(str(elem.id), elem.CVE_id) for elem in cves]


def get_elem_for_task(elem_form: tuple, key: str):
    for elem in elem_form:
        # print(elem[0],key)
        if elem[0].find(key):
            return elem[1]


class ScanAPI(ModelViewSet):
    queryset = ResultScan.objects.all()
    serializer_class = ResultScanSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ScanSerializer
        return ResultScanSerializer

    def create(self, request, *args, **kwargs):
        serializer = ScanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip_targets = tuple(define_targets())
        cve_list = tuple(get_cves())
        # print(cve_list)

        ip_target = get_elem_for_task(ip_targets, serializer.data["ip_target"])
        cve = get_elem_for_task(cve_list, serializer.data["cve"])
        cve = "CVE-2022-21907"
        # ip_target = "192.168.1.103"
        ip_target = "192.168.1.103"
        values_from_cve = CVES.objects.filter(CVE_id=cve).values()[0]

        protocol = str(Protocols.objects.get(pk=values_from_cve.get("protocol_id_id")))
        result_task = tasks.get(values_from_cve.get("name"))(ip_target, False)
        gradation = InfectionRate.objects.filter(pk=result_task).values()[0].get("gradation")
        result_scan = ResultScan.objects.create(ip_target=ip_target, cve_id=cve, protocol=protocol, gradation=gradation)
        result_scan.save()
        return Response(data=ResultScanSerializer(instance=result_scan).data)


class CvesAPI(ModelViewSet):
    queryset = CVES.objects.all()
    serializer_class = CVESSerializer


class InfectionRateAPI(ModelViewSet):
    queryset = InfectionRate.objects.all()
    serializer_class = InfectionRateSerializer


class ProtocolAPI(ModelViewSet):
    queryset = Protocols.objects.all()
    serializer_class = ProtocolsSerializer


class Targets(ModelViewSet):
    def list(self, request, *args, **kwargs):
        targets = define_targets()
        cves = get_cves()

        data = {
            "targets": targets,
            "cves": cves
        }

        return Response(data=data)
