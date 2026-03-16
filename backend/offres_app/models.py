from django.db import models

class Offre(models.Model):
    intitule = models.CharField(max_length=500)
    entreprise = models.CharField(max_length=300, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    type_contrat = models.CharField(max_length=100, blank=True, null=True)
    date_publication = models.DateField(blank=True, null=True)
    competences = models.TextField(blank=True, null=True)
    secteur = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-date_publication']
        verbose_name = 'Offre'
        verbose_name_plural = 'Offres'

    def __str__(self):
        return f"{self.intitule} - {self.entreprise}"