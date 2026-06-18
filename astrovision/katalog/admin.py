from django.contrib import admin
from .models import Souhrezdí, TypObjektu, AstronomickyObjekt, Pozorovatelna, Pozorování


@admin.register(Souhrezdí)
class SouhvezdiAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'zkratka')
    search_fields = ('nazev', 'zkratka')


@admin.register(TypObjektu)
class TypObjektuAdmin(admin.ModelAdmin):
    list_display = ('ikona', 'nazev')
    search_fields = ('nazev',)


class PozorováníInline(admin.TabularInline):
    model = Pozorování
    extra = 1
    fields = ('datum', 'pozorovatelna', 'kvalita_oblohy', 'popis')


@admin.register(AstronomickyObjekt)
class AstronomickyObjektAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'katalogove_cislo', 'typ', 'souhvezdi',
                    'vzdalenost_ly', 'jasnost', 'obtiznost_pozorovani', 'je_featured')
    list_filter = ('typ', 'souhvezdi', 'obtiznost_pozorovani', 'je_featured')
    search_fields = ('nazev', 'katalogove_cislo', 'popis')
    list_editable = ('je_featured',)
    inlines = [PozorováníInline]
    fieldsets = (
        ('Základní informace', {
            'fields': ('nazev', 'katalogove_cislo', 'typ', 'souhvezdi', 'je_featured')
        }),
        ('Fyzikální vlastnosti', {
            'fields': ('vzdalenost_ly', 'jasnost', 'obtiznost_pozorovani')
        }),
        ('Popis a média', {
            'fields': ('popis', 'foto')
        }),
    )


@admin.register(Pozorovatelna)
class PozorovatelnaAdmin(admin.ModelAdmin):
    list_display = ('nazev', 'misto', 'nadmorska_vyska', 'svetelne_znecisteni')
    list_filter = ('svetelne_znecisteni',)
    search_fields = ('nazev', 'misto')


@admin.register(Pozorování)
class PozorováníAdmin(admin.ModelAdmin):
    list_display = ('objekt', 'datum', 'pozorovatelna', 'kvalita_oblohy')
    list_filter = ('kvalita_oblohy', 'pozorovatelna')
    search_fields = ('objekt__nazev', 'popis')
    date_hierarchy = 'datum'
