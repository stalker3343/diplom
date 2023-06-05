from rest_framework import serializers
from .models import Protocols, CVES, ResultScan, InfectionRate


class ProtocolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocols
        fields = "__all__"


class CVESSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVES
        fields = "__all__"


class ResultScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultScan
        fields = "__all__"


class ScanSerializer(serializers.Serializer):
    ip_target = serializers.CharField(max_length=50)
    cve = serializers.CharField(max_length=50)


class InfectionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfectionRate
        fields = "__all__"
