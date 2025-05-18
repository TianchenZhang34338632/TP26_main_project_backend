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
    crime_score = models.FloatField()
    facility_count = models.IntegerField()
    class Meta:
        db_table = 'vic_traffic_crime_merge'
        managed = False
        # Disable automatic primary keys id
        auto_created = True
        # Prevent Django from adding default sorting
        ordering = []

class VicCrimeScore(models.Model):
    postcode = models.IntegerField(primary_key=True)
    geometry = models.TextField()
    Total_Offences = models.IntegerField()
    Severe_Offences = models.IntegerField()
    Severe_Offence_Rate = models.FloatField()
    Composite_Score = models.FloatField()
    Crime_Score = models.IntegerField()
    class Meta:
        db_table = 'vic_crime_score'
        managed = False
        # Disable automatic primary keys id
        auto_created = True
        # Prevent Django from adding default sorting
        ordering = []

class UVData(models.Model):
    date_time = models.DateTimeField()
    lat = models.FloatField()
    lon = models.FloatField()
    uv_index = models.FloatField()

    class Meta:
        db_table = 'uv_data'
        managed = False

    def __str__(self):
        return f"{self.date_time} - UV {self.uv_index}"

class Facility(models.Model):
    ftype = models.CharField(max_length=100)
    featsubtyp = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    name_label = models.CharField(max_length=200)
    state = models.CharField(max_length=10)
    longitude = models.FloatField()
    latitude = models.FloatField()
    class Meta:
        db_table = 'facilities'
        managed = False

class AccidentData(models.Model):
    accident_no = models.CharField(max_length=20, primary_key=True)
    accident_date = models.DateField()
    accident_time = models.TimeField()
    accident_type = models.IntegerField()
    accident_type_desc = models.CharField(max_length=100)
    day_of_week = models.IntegerField()
    day_week_desc = models.CharField(max_length=20)
    dca_code = models.IntegerField()
    dca_desc = models.CharField(max_length=200)
    light_condition = models.IntegerField()
    node_id = models.IntegerField()
    no_of_vehicles = models.IntegerField()
    no_persons_killed = models.IntegerField()
    no_persons_inj_2 = models.IntegerField()
    no_persons_inj_3 = models.IntegerField()
    no_persons_not_inj = models.IntegerField()
    no_persons = models.IntegerField()
    police_attend = models.IntegerField()
    road_geometry = models.IntegerField()
    road_geometry_desc = models.CharField(max_length=50)
    severity = models.IntegerField()
    speed_zone = models.IntegerField()
    rma = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'accident_data'
        managed = False

class AccidentPersonData(models.Model):
    accident_no = models.CharField(max_length=20)
    person_id = models.CharField(max_length=10)
    vehicle_id = models.CharField(max_length=5)
    sex = models.CharField(max_length=1)
    age_group = models.CharField(max_length=20)
    inj_level = models.IntegerField()
    inj_level_desc = models.CharField(max_length=50)
    seating_position = models.CharField(max_length=5)
    helmet_belt_worn = models.FloatField(null=True)
    road_user_type = models.IntegerField()
    road_user_type_desc = models.CharField(max_length=50)
    licence_state = models.CharField(max_length=5, null=True)
    taken_hospital = models.CharField(max_length=1, null=True)
    ejected_code = models.FloatField(null=True)

    class Meta:
        db_table = 'accident_person_data'
        managed = False

class TrafficFeature(models.Model):
    postcode = models.IntegerField(primary_key=True)
    total_accidents = models.IntegerField()
    avg_severity = models.FloatField()
    total_people = models.IntegerField()
    serious_injuries = models.IntegerField()
    minor_injuries = models.IntegerField()
    total_acc_score = models.FloatField()
    serious_inj_rate = models.FloatField()
    serious_inj_score = models.FloatField()
    geometry = models.TextField()

    class Meta:
        db_table = 'traffic_features'
        managed = False

class CrimeFeature(models.Model):
    postcode = models.IntegerField(primary_key=True, db_column='Postcode')
    total_offences = models.IntegerField()
    severe_offences = models.IntegerField()
    severe_offence_rate = models.FloatField()
    total_off_score = models.FloatField()
    severe_off_score = models.FloatField()
    geometry = models.TextField()

    class Meta:
        db_table = 'crime_features'
        managed = False

class MergedExploreTable(models.Model):
    postcode = models.IntegerField(primary_key=True)
    total_accidents = models.IntegerField()
    avg_severity = models.FloatField()
    total_people = models.IntegerField()
    serious_injuries = models.IntegerField()
    minor_injuries = models.IntegerField()
    total_acc_score = models.FloatField()
    serious_inj_rate = models.FloatField()
    serious_inj_score = models.FloatField()
    total_offences = models.IntegerField()
    severe_offences = models.IntegerField()
    severe_offence_rate = models.FloatField()
    total_off_score = models.FloatField()
    severe_off_score = models.FloatField()
    geometry = models.TextField()
    geom_polygon = models.TextField()
    facility_count = models.IntegerField()

    class Meta:
        db_table = 'merged_explore_table'
        managed = False
