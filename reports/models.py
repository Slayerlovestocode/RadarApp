# reports/models.py

import uuid
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from django.db import models

class Report(models.Model):
    # Choices for the incident type dropdown
    INCIDENT_TYPE_CHOICES = [
        ('Verbal Harassment', 'Verbal Harassment'),
        ('Physical Assault', 'Physical Assault'),
        ('Workplace Discrimination', 'Workplace Discrimination'),
        ('Online Hate Speech', 'Online Hate Speech'),
    ]
    

    # Status choices
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Resolved', 'Resolved'),
    ]

    # Fields for the model
    case_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPE_CHOICES)
    incident_datetime = models.DateTimeField(help_text="Please use the format: YYYY-MM-DD HH:MM:SS")
    location = models.CharField(max_length=255, help_text="Enter a specific address or city in Switzerland.")
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields for coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_index=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_index=True)
    is_approved_for_map = models.BooleanField(default=False, db_index=True)
    severity_level = models.IntegerField(default=1, help_text="1=Low, 2=Medium, 3=High", db_index=True)

    # Optional contact information
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('telegram', 'Telegram'),
    ]
    contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES, blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Geocode the location to get lat/lng before saving
        if self.location and (self.latitude is None or self.longitude is None):
            geolocator = Nominatim(user_agent="racism_radar")
            # Restrict search to Switzerland
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            location_data = geocode(self.location, country_codes="CH")
            
            if location_data:
                self.latitude = location_data.latitude
                self.longitude = location_data.longitude

        super().save(*args, **kwargs)

    def __str__(self):
        # This helps identify reports in the Django admin area
        return f"CASE-{str(self.case_id).split('-')[0].upper()}"


class EvidenceFile(models.Model):
    report = models.ForeignKey(Report, related_name='evidence_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='evidence/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidence for {self.report}"
    

class Resource(models.Model):
    # Choices for the resource type dropdown
    RESOURCE_TYPE_CHOICES = [
        ('QURAN', 'Quranic Verse'),
        ('HADITH', 'Hadith'),
        ('ARTICLE', 'Article'),
        ('BIOGRAPHY', 'Historical Figure'),
        ('PROPHET', "Prophet's Life Lesson"),
    ]

    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES, default='ARTICLE')
    content = models.TextField()
    source = models.CharField(max_length=100, blank=True, help_text="e.g., Quran 49:13, Bukhari, or author's name")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
