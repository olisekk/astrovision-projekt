from django.db import models
from django.utils import timezone


class Souhrezdí(models.Model):
    """Souhvězdí, ve kterém se objekt nachází."""
    nazev = models.CharField("Název", max_length=100)
    zkratka = models.CharField("Zkratka IAU", max_length=5)
    popis = models.TextField("Popis", blank=True)

    class Meta:
        verbose_name = "Souhvězdí"
        verbose_name_plural = "Souhvězdí"
        ordering = ['nazev']

    def __str__(self):
        return f"{self.nazev} ({self.zkratka})"


class TypObjektu(models.Model):
    """Typ astronomického objektu (galaxie, mlhovina, hvězdokupa…)."""
    nazev = models.CharField("Název typu", max_length=100)
    ikona = models.CharField("Ikona (emoji)", max_length=10, default="⭐")
    popis = models.TextField("Popis", blank=True)

    class Meta:
        verbose_name = "Typ objektu"
        verbose_name_plural = "Typy objektů"
        ordering = ['nazev']

    def __str__(self):
        return self.nazev


class AstronomickyObjekt(models.Model):
    """Hlavní datový objekt – hvězda, galaxie, mlhovina apod."""
    OBTIZNOST_CHOICES = [
        (1, "⭐ Snadný"),
        (2, "⭐⭐ Střední"),
        (3, "⭐⭐⭐ Náročný"),
        (4, "⭐⭐⭐⭐ Expert"),
    ]

    nazev = models.CharField("Název", max_length=200)
    katalogove_cislo = models.CharField("Katalogové číslo (Messier / NGC)", max_length=30, blank=True)
    typ = models.ForeignKey(TypObjektu, on_delete=models.PROTECT,
                            verbose_name="Typ objektu", related_name='objekty')
    souhvezdi = models.ForeignKey(Souhrezdí, on_delete=models.PROTECT,
                                  verbose_name="Souhvězdí", related_name='objekty')
    popis = models.TextField("Popis")
    vzdalenost_ly = models.FloatField("Vzdálenost (světelné roky)", null=True, blank=True)
    jasnost = models.FloatField("Zdánlivá jasnost (mag)", null=True, blank=True)
    obtiznost_pozorovani = models.IntegerField("Obtížnost pozorování",
                                               choices=OBTIZNOST_CHOICES, default=1)
    foto = models.ImageField("Fotografie", upload_to='objekty/', blank=True, null=True)
    datum_pridani = models.DateTimeField("Datum přidání", default=timezone.now)
    je_featured = models.BooleanField("Doporučený objekt", default=False)

    class Meta:
        verbose_name = "Astronomický objekt"
        verbose_name_plural = "Astronomické objekty"
        ordering = ['nazev']

    def __str__(self):
        return f"{self.nazev} [{self.katalogove_cislo}]" if self.katalogove_cislo else self.nazev


class Pozorovatelna(models.Model):
    """Pozorovatelna / lokalita vhodná pro astronomii."""
    nazev = models.CharField("Název", max_length=200)
    misto = models.CharField("Místo", max_length=200)
    nadmorska_vyska = models.IntegerField("Nadmořská výška (m)", null=True, blank=True)
    popis = models.TextField("Popis", blank=True)
    svetelne_znecisteni = models.IntegerField("Světelné znečištění (Bortle 1–9)",
                                               choices=[(i, i) for i in range(1, 10)], default=5)
    web = models.URLField("Web", blank=True)

    class Meta:
        verbose_name = "Pozorovatelna"
        verbose_name_plural = "Pozorovatelny"
        ordering = ['nazev']

    def __str__(self):
        return self.nazev


class Pozorování(models.Model):
    """Záznam o konkrétním pozorování objektu."""
    objekt = models.ForeignKey(AstronomickyObjekt, on_delete=models.CASCADE,
                               verbose_name="Objekt", related_name='pozorovani')
    pozorovatelna = models.ForeignKey(Pozorovatelna, on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      verbose_name="Pozorovatelna", related_name='pozorovani')
    datum = models.DateField("Datum pozorování")
    popis = models.TextField("Poznámky z pozorování", blank=True)
    kvalita_oblohy = models.IntegerField("Kvalita oblohy (1–5)",
                                          choices=[(i, i) for i in range(1, 6)], default=3)
    foto = models.ImageField("Fotografie z pozorování", upload_to='pozorovani/', blank=True, null=True)

    class Meta:
        verbose_name = "Pozorování"
        verbose_name_plural = "Pozorování"
        ordering = ['-datum']

    def __str__(self):
        return f"{self.objekt.nazev} – {self.datum}"
