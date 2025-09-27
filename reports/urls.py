# reports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Main landing page
    path('', views.home, name='home'),

    # Report submission and status check
    path('submit/', views.submit_report, name='submit_report'),
    path('submission-success/<uuid:case_id>/', views.submission_success, name='submission_success'),
    path('check-status/', views.check_status, name='check_status'),
    path('report/<uuid:case_id>/', views.report_details, name='report_details'),

    # Heatmap and its data API
    path('heatmap/', views.incidents_heatmap, name='incidents_heatmap'),
    path('api/report-locations/', views.report_locations_api, name='report_locations_api'),

    # Educational Resources
    path('guidance/', views.resource_landing, name='resource_landing'),
    path('guidance/<str:resource_type>/', views.resource_list, name='resource_list'),

    # Support/Donation Page
    path('support/', views.support_page, name='support_page'),

    # About Us Page
    path('about/', views.about_us, name='about_us'),
]