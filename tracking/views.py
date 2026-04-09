from django.shortcuts import render

# Create your views here.
from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from .models import VisitaRegistro
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def tracking_list(request):
    qs = VisitaRegistro.objects.using("default").all().order_by("-fecha_hora")

    fecha_inicio = request.GET.get("fecha_inicio", "").strip()
    fecha_fin = request.GET.get("fecha_fin", "").strip()
    es_bot = request.GET.get("es_bot", "").strip()
    q = request.GET.get("q", "").strip()

    if fecha_inicio:
        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fi_dt = timezone.make_aware(
                datetime.combine(fi, time.min),
                timezone.get_current_timezone()
            )
            qs = qs.filter(fecha_hora__gte=fi_dt)
        except ValueError:
            pass

    if fecha_fin:
        try:
            ff = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            ff_dt = timezone.make_aware(
                datetime.combine(ff, time.max),
                timezone.get_current_timezone()
            )
            qs = qs.filter(fecha_hora__lte=ff_dt)
        except ValueError:
            pass

    if es_bot == "si":
        qs = qs.filter(es_bot=True)
    elif es_bot == "no":
        qs = qs.filter(es_bot=False)

    if q:
        qs = qs.filter(
            Q(ip__icontains=q) |
            Q(ciudad__icontains=q) |
            Q(pais__icontains=q) |
            Q(user_agent__icontains=q) |
            Q(referrer__icontains=q) |
            Q(path__icontains=q)
        )

    paginator = Paginator(qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "es_bot": es_bot,
        "q": q,
        "total": qs.count(),
    }
    return render(request, "tracking/tracking_list.html", context)

from datetime import datetime, time

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from .models import VisitaRegistro


@login_required
def reporte_visitas_por_ciudad(request):
    qs = VisitaRegistro.objects.using("default").all()

    fecha_inicio = request.GET.get("fecha_inicio", "").strip()
    fecha_fin = request.GET.get("fecha_fin", "").strip()
    incluir_bots = request.GET.get("incluir_bots", "").strip()

    if fecha_inicio:
        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fi_dt = timezone.make_aware(
                datetime.combine(fi, time.min),
                timezone.get_current_timezone()
            )
            qs = qs.filter(fecha_hora__gte=fi_dt)
        except ValueError:
            pass

    if fecha_fin:
        try:
            ff = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            ff_dt = timezone.make_aware(
                datetime.combine(ff, time.max),
                timezone.get_current_timezone()
            )
            qs = qs.filter(fecha_hora__lte=ff_dt)
        except ValueError:
            pass

    if incluir_bots != "si":
        qs = qs.filter(es_bot=False)

    reporte = (
        qs.exclude(ciudad__isnull=True)
          .exclude(ciudad__exact="")
          .values("ciudad", "pais")
          .annotate(total_visitas=Count("id"))
          .order_by("-total_visitas", "ciudad")
    )

    context = {
        "reporte": reporte,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "incluir_bots": incluir_bots,
        "total_ciudades": len(reporte),
        "total_visitas": sum(item["total_visitas"] for item in reporte),
    }
    return render(request, "tracking/reporte_visitas_por_ciudad.html", context)
