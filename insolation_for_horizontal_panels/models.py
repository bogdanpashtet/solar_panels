from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator


class Stations(models.Model):
    id = models.BigAutoField(primary_key=True)
    station_name = models.CharField('Название', max_length=50)
    region = models.CharField('Регион', max_length=50)
    latitude = models.DecimalField('Широта', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    longitude = models.DecimalField('Долгота', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])

    def __str__(self):
        return self.station_name

    class Meta:
        verbose_name = 'Station'
        verbose_name_plural = 'Stations'


class BaseMonth(models.Model):
    class Meta:
        abstract = True

    station_id = models.OneToOneField(Stations, on_delete=models.CASCADE, primary_key=True)
    month_1 = models.DecimalField('month_1', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_2 = models.DecimalField('month_2', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_3 = models.DecimalField('month_3', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_4 = models.DecimalField('month_4', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_5 = models.DecimalField('month_5', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_6 = models.DecimalField('month_6', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_7 = models.DecimalField('month_7', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_8 = models.DecimalField('month_8', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_9 = models.DecimalField('month_9', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_10 = models.DecimalField('month_10', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_11 = models.DecimalField('month_11', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])
    month_12 = models.DecimalField('month_12', max_digits=10, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.00'))])


class BaseHour(BaseMonth):
    class Meta:
        abstract = True

    hour_num = models.PositiveIntegerField('hour_num', validators=[MinValueValidator(1)])


# Альбедо
class Albedo(BaseMonth):
    pass


# Суммарная месячная солнечная радиация
class DiffuseMonthlySolarRadiation(BaseMonth):
    pass


class DirectMonthlySolarRadiation(BaseMonth):
    pass


class TotalMonthlySolarRadiation(BaseMonth):
    pass


# Суммарная суточная солнечная радиация
class DiffuseDailySolarRadiation(BaseMonth):
    pass


class DirectDailySolarRadiation(BaseMonth):
    pass


class TotalDailySolarRadiation(BaseMonth):
    pass


# Суммарная часовая солнечная радиация
class DiffuseHourlySolarRadiation(BaseHour):
    pass


class DirectHourlySolarRadiation(BaseHour):
    pass


class TotalHourlySolarRadiation(BaseHour):
    pass

