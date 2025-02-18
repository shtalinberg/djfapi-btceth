from django.db import models
from django.utils import timezone


class Currency(models.Model):
    name = models.CharField(verbose_name='Currency name', max_length=20, unique=True)
    created_at = models.DateTimeField(verbose_name='Created', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "currency"
        verbose_name_plural = "currencies"


class Provider(models.Model):
    name = models.CharField(verbose_name='Provider name', max_length=50)
    api_key = models.CharField(verbose_name='API key', max_length=200)
    created_at = models.DateTimeField(verbose_name='created', auto_now_add=True)

    def __str__(self):
        return self.name


class Block(models.Model):
    currency = models.ForeignKey(
        Currency,
        verbose_name='Currency',
        on_delete=models.CASCADE,
        related_name='blocks',
    )
    provider = models.ForeignKey(
        Provider,
        verbose_name='Provider',
        on_delete=models.CASCADE,
        related_name='blocks',
    )
    block_number = models.BigIntegerField(verbose_name='Block Number')
    block_created_at = models.DateTimeField(
        verbose_name='Block created', null=True, blank=True
    )
    created_at = models.DateTimeField(verbose_name='created', default=timezone.now)

    def __str__(self):
        return f"{self.currency.name} Block #{self.block_number}"

    class Meta:
        ordering = ['-block_number']
        unique_together = ['currency', 'block_number']
        verbose_name = "block"
