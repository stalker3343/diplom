from django.contrib import admin
from .models import CVES, InfectionRate, Protocols, ResultScan


@admin.register(CVES)
class CVEAdmin(admin.ModelAdmin):
    list_display = ('id', 'CVE_id', 'name', 'CVSS', "protocol_id")
    list_filter = ('CVE_id', 'CVSS')
    search_fields = ("CVE_id", )
    ordering = ('-id', )


@admin.register(InfectionRate)
class InfectionRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'gradation', 'description')
    ordering = ('-id',)


@admin.register(Protocols)
class ProtocolsAdmin(admin.ModelAdmin):
    list_display = ('id', 'protocol')
    ordering = ('-id',)


@admin.register(ResultScan)
class ResultScanAdmin(admin.ModelAdmin):
    list_display = ('id', "ip_target", 'cve_id', 'protocol', 'scan_data', "gradation")
    list_filter = ("ip_target", 'cve_id', "protocol", "gradation")
    search_fields = ("ip_target", "cve_id",)
    ordering = ('-id',)
