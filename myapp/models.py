from django.db import models


class PositionDetail(models.Model):
    # Define fields according to the actual table structure
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'position_detail'  # table name


class PreviousUVIndex(models.Model):
    # Define fields according to the actual table structure
    uv_value = models.FloatField()
    recorded_at = models.DateTimeField()
    position = models.ForeignKey(PositionDetail, on_delete=models.CASCADE)

    class Meta:
        db_table = 'previous_uv_index'  # table name

class ProcessedAvgMonthlyUV(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    avg_uv_index = models.FloatField()

    class Meta:
        db_table = 'processed_avg_monthly_uv'  # Matches your existing table name
        managed = False  # Important: tells Django this table already exists
        # Disable automatic primary keys id
        auto_created = True
        # Declaring Joint Primary Keys
        unique_together = (('year', 'month', 'lat', 'lon'),)
        # Prevent Django from adding default sorting
        ordering = []

