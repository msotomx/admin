from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import ArticuloAyuda

@login_required
def ayuda_home(request):
    # Redirige al primer artículo activo (o muestra una portada)
    first = ArticuloAyuda.objects.using('default').filter(activo=True).order_by("categoria", "orden").first()
    if first:
        return redirect("ayuda:articulo", slug=first.slug)
    return render(request, "ayuda/home.html")

@login_required
def articulo(request, slug):
    articulo = get_object_or_404(ArticuloAyuda, slug=slug, activo=True)

    # Menú lateral
    articulos = ArticuloAyuda.objects.using('default').filter(activo=True).order_by("categoria", "orden", "titulo")
    menu = {}
    for a in articulos:
        menu.setdefault(a.categoria, []).append(a)

    return render(request, "ayuda/articulo.html", {
        "articulo": articulo,
        "menu": menu,
    })
