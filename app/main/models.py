from django.db import models
from datetime import datetime


class Protocols(models.Model):
    protocol = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Протокол"
        verbose_name_plural = 'Протоколы'

    def __str__(self):
        return '%s' % self.protocol


class CVES(models.Model):
    CVE_id = models.CharField(max_length=50)
    name = models.CharField(max_length=250)
    description = models.TextField()
    CVSS = models.FloatField()
    protocol_id = models.ForeignKey(Protocols, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Уязвимость"
        verbose_name_plural = 'Уязвимости'


class InfectionRate(models.Model):
    gradation = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name = "Градация зараженности"
        verbose_name_plural = 'Градации зараженности'


class ResultScan(models.Model):
    ip_target = models.CharField(max_length=50)
    cve_id = models.CharField(max_length=50, default="1")
    protocol = models.CharField(max_length=10, default="1")
    scan_data = models.DateTimeField(default=datetime.now())
    gradation = models.CharField(max_length=50, default="1")

    class Meta:
        verbose_name = "Результат сканирования"
        verbose_name_plural = 'Результаты сканирования'
