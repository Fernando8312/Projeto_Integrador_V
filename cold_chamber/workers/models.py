from django.db import models
from django.utils import timezone

class Worker(models.Model):
    name = models.CharField(max_length=100)
    tag_uid = models.CharField(max_length=20, unique=True)  # UID do cartão RFID
    max_exposure_minutes = models.PositiveIntegerField(
        default=3,
        verbose_name="Tempo Máximo (minutos)"
    )  # Limite de exposição

    def __str__(self):
        return self.name

class AccessRecord(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    exposure_duration = models.FloatField(null=True, blank=True)  # Em minutos

    def save(self, *args, **kwargs):
        # Calcula a duração da exposição ao salvar
        if self.exit_time:
            self.exposure_duration = (self.exit_time - self.entry_time).total_seconds() / 60
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.worker.name} - {self.entry_time}"
    
    @property
    def current_exposure(self):
        if self.exit_time:
            return None  # Já saiu
        delta = timezone.now() - self.entry_time
        return delta.total_seconds()