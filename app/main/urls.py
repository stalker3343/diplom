from . import views
from rest_framework.routers import SimpleRouter
app_name = "main"

router = SimpleRouter()

router.register("cves", views.CvesAPI, basename="cves")
router.register("protocols", views.ProtocolAPI, basename="protocols")
router.register("rates", views.InfectionRateAPI, basename="rates")
router.register("scans", views.ScanAPI, basename="scans")
router.register("targets", views.Targets, basename="targets")
urlpatterns = router.urls
