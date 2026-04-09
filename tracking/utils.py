from datetime import timedelta

from django.utils import timezone

from .models import VisitaRegistro
from django.contrib.gis.geoip2.base import GeoIP2

BOT_SIGNATURES = [
    "bot",
    "crawler",
    "spider",
    "facebookexternalhit",
    "whatsapp",
    "slurp",
    "bingpreview",
    "python-requests",
    "curl",
    "wget",
    "headless",
    "monitor",
    "uptime",
]


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def es_bot_request(user_agent: str) -> bool:
    if not user_agent:
        return True

    ua = user_agent.lower()
    return any(firma in ua for firma in BOT_SIGNATURES)


def obtener_ciudad_pais(ip):
    try:
        g = GeoIP2()
        data = g.city(ip)
        ciudad = data.get("city", "") or ""
        pais = data.get("country_name", "") or ""
        return ciudad, pais
    except Exception:
        return "", ""


def registrar_visita_registro(request):
    ahora = timezone.now()
    ultima_visita = request.session.get("ultima_visita_registro")

    if ultima_visita:
        try:
            ultima = timezone.datetime.fromisoformat(ultima_visita)
            if timezone.is_naive(ultima):
                ultima = timezone.make_aware(
                    ultima,
                    timezone.get_current_timezone()
                )

            if ahora - ultima < timedelta(minutes=30):
                return
        except Exception:
            pass

    ip = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    referrer = request.META.get("HTTP_REFERER", "")
    path = request.path
    es_bot = es_bot_request(user_agent)

    ciudad = ""
    pais = ""

    if not es_bot and ip and ip not in ("127.0.0.1", "::1"):
        ciudad, pais = obtener_ciudad_pais(ip)

    VisitaRegistro.objects.create(
        ip=ip,
        ciudad=ciudad,
        pais=pais,
        user_agent=user_agent,
        referrer=referrer,
        es_bot=es_bot,
        path=path,
    )

    request.session["ultima_visita_registro"] = ahora.isoformat()
