from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import AstronomickyObjekt, TypObjektu, Souhrezdí, Pozorovatelna, Pozorování


def index(request):
    """Úvodní stránka."""
    featured = AstronomickyObjekt.objects.filter(je_featured=True).select_related('typ', 'souhvezdi')[:3]
    celkem_objektu = AstronomickyObjekt.objects.count()
    celkem_pozorovani = Pozorování.objects.count()
    typy = TypObjektu.objects.annotate(pocet=Count('objekty')).filter(pocet__gt=0)
    posledni_pozorovani = Pozorování.objects.select_related('objekt', 'pozorovatelna').order_by('-datum')[:5]
    return render(request, 'katalog/index.html', {
        'featured': featured,
        'celkem_objektu': celkem_objektu,
        'celkem_pozorovani': celkem_pozorovani,
        'typy': typy,
        'posledni_pozorovani': posledni_pozorovani,
    })


def objekty_seznam(request):
    """Výpis všech astronomických objektů s filtrováním."""
    objekty = AstronomickyObjekt.objects.select_related('typ', 'souhvezdi').all()

    # Filtrování
    q = request.GET.get('q', '')
    typ_id = request.GET.get('typ', '')
    souhvezdi_id = request.GET.get('souhvezdi', '')
    obtiznost = request.GET.get('obtiznost', '')

    if q:
        objekty = objekty.filter(
            Q(nazev__icontains=q) | Q(katalogove_cislo__icontains=q) | Q(popis__icontains=q)
        )
    if typ_id:
        objekty = objekty.filter(typ_id=typ_id)
    if souhvezdi_id:
        objekty = objekty.filter(souhvezdi_id=souhvezdi_id)
    if obtiznost:
        objekty = objekty.filter(obtiznost_pozorovani=obtiznost)

    typy = TypObjektu.objects.all()
    souhvezdi_list = Souhrezdí.objects.all()

    return render(request, 'katalog/objekty_seznam.html', {
        'objekty': objekty,
        'typy': typy,
        'souhvezdi_list': souhvezdi_list,
        'q': q,
        'typ_id': typ_id,
        'souhvezdi_id': souhvezdi_id,
        'obtiznost': obtiznost,
        'obtiznosti': AstronomickyObjekt.OBTIZNOST_CHOICES,
    })


def objekt_detail(request, pk):
    """Detailní náhled na jeden astronomický objekt."""
    objekt = get_object_or_404(
        AstronomickyObjekt.objects.select_related('typ', 'souhvezdi'), pk=pk
    )
    pozorovani = objekt.pozorovani.select_related('pozorovatelna').all()
    souvisejici = AstronomickyObjekt.objects.filter(
        souhvezdi=objekt.souhvezdi
    ).exclude(pk=pk).select_related('typ')[:4]
    return render(request, 'katalog/objekt_detail.html', {
        'objekt': objekt,
        'pozorovani': pozorovani,
        'souvisejici': souvisejici,
    })


def pozorovateny_seznam(request):
    """Výpis pozorovatelen."""
    pozorovateny = Pozorovatelna.objects.annotate(pocet=Count('pozorovani')).order_by('svetelne_znecisteni')
    return render(request, 'katalog/pozorovateny_seznam.html', {
        'pozorovateny': pozorovateny,
    })


def pozorovatelna_detail(request, pk):
    """Detail pozorovatelny."""
    pozorovatelna = get_object_or_404(Pozorovatelna, pk=pk)
    pozorovani = pozorovatelna.pozorovani.select_related('objekt').order_by('-datum')[:10]
    return render(request, 'katalog/pozorovatelna_detail.html', {
        'pozorovatelna': pozorovatelna,
        'pozorovani': pozorovani,
    })
