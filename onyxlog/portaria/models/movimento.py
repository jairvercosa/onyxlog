# -*- coding: ISO-8859-1 -*-
import datetime
from django.db import models

class Movimento(models.Model):
    """
    Model dos movimentos de entrada e saída de portaria
    """

    entrada = models.DateField(
        verbose_name="Entrada",
        blank=True,
        null=False    
    )

    entrada_hora = models.TimeField(
        verbose_name="Hora Entrada",
        blank=True,
        null=True,    
    )

    saida = models.DateField(
        verbose_name="Saída",
        blank=True,
        null=True    
    )

    saida_hora = models.TimeField(
        verbose_name="Hora Saída",
        blank=True,
        null=True    
    )

    liberado_por = models.CharField(
        verbose_name="Liberado por",
        help_text="Usuário que liberou a entrada.",
        max_length=80,
        blank=True,
        null=True
    )

    obs = models.TextField(
        verbose_name="Obs",
        blank=True,
        null=True
    )

    codigo = models.CharField(
        verbose_name="Código",
        max_length=20,
        blank=True,
        null=False,
        default=''
    )

    motivo = models.ForeignKey(
        'portaria.Motivo',
        verbose_name="Motivo da Visita",
        blank=False,
        null=True,
        on_delete=models.PROTECT
    )

    planta = models.ForeignKey(
        'cadastros.Planta',
        verbose_name="Planta de Operação",
        blank=False,
        null=False,
        default=1
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.entrada:
                self.entrada = datetime.datetime.now()
                self.entrada_hora = datetime.datetime.now().time()

            self.codigo = str(self.entrada.year) + str(self.entrada.month) + str(self.entrada.day)
            self.codigo = self.codigo + str(self.entrada_hora.hour) + str(self.entrada_hora.minute) + str(self.entrada_hora.second)
        elif not self.saida:
            self.saida = datetime.datetime.now()
            self.saida_hora = datetime.datetime.now().time()
            self.save()

        super(Movimento, self).save(*args, **kwargs)

    class Meta:
        app_label="portaria"
