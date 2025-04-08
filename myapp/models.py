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

from django.db import models

class AccidentNode(models.Model):
    accident_no = models.CharField(max_length=20, primary_key=True)
    node_id = models.CharField(max_length=20)
    node_type = models.CharField(max_length=10)
    amg_x = models.IntegerField()
    amg_y = models.IntegerField()
    lga_name = models.CharField(max_length=50)
    lga_name_all = models.CharField(max_length=50)
    deg_urban_name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    postcode_crash = models.IntegerField()

    class Meta:
        db_table = 'accident_node'
        managed = False
        # Disable automatic primary keys id
        auto_created = True
        # Prevent Django from adding default sorting
        ordering = []

    def __str__(self):
        return self.accident_no