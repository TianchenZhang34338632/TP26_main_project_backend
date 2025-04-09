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


class VicPostcodeScore(models.Model):
    postcode = models.IntegerField(primary_key=True)
    geometry = models.TextField()
    total_accidents = models.IntegerField()
    total_people = models.IntegerField()
    serious_injuries = models.IntegerField()
    minor_injuries = models.IntegerField()
    traffic_score = models.FloatField()

    class Meta:
        db_table = 'vic_postcode_score'
        managed = False
        # Disable automatic primary keys id
        auto_created = True
        # Prevent Django from adding default sorting
        ordering = []
