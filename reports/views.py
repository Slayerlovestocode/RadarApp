# reports/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from django.db.models.functions import Cast
from django.utils.timesince import timesince
from .forms import ReportForm
from .models import Report, Resource, EvidenceFile

# View for the home page (already added)
def home(request):
    # Count all approved reports for the home page stat
    approved_reports_count = Report.objects.filter(is_approved_for_map=True).count()
    return render(request, 'reports/home.html', {'approved_reports_count': approved_reports_count})

# View for submitting a new report
def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            files = request.FILES.getlist('evidence')
            for f in files:
                EvidenceFile.objects.create(report=report, file=f)

            # Redirect to a new page to show the case ID
            return redirect('submission_success', case_id=report.case_id)
    else:
        form = ReportForm()

    return render(request, 'reports/submit_report.html', {'form': form})

# View for the submission success page
def submission_success(request, case_id):
    return render(request, 'reports/submission_success.html', {'case_id': case_id})


# View for the status check input form
def check_status(request):
    error = None
    if request.method == 'POST':
        case_id_str = request.POST.get('case_id', '').strip()
        try:
            # We expect a full UUID string from the user
            report = Report.objects.get(pk=case_id_str)
            # If found, redirect to the details page
            return redirect('report_details', case_id=report.case_id)
        except (Report.DoesNotExist, ValueError):
            # If ID is not a valid UUID or not found, set an error message
            error = "Invalid Case ID. Please check the ID and try again."
            
    return render(request, 'reports/check_status.html', {'error': error})

def report_details(request, case_id):
    # Get the report object; if not found, it will return a 404 error page
    report = get_object_or_404(Report, pk=case_id)
    return render(request, 'reports/report_details.html', {'report': report})

# --- Educational Resources Views ---

def resource_landing(request):
    """Displays the main landing page for educational resources."""
    resource_types = Resource.RESOURCE_TYPE_CHOICES
    return render(request, 'reports/resource_landing.html', {'resource_types': resource_types})

def resource_list(request, resource_type):
    """Displays a list of resources for a given type."""
    resources = Resource.objects.filter(resource_type=resource_type).order_by('-created_at')
    # Get the human-readable label for the resource type
    type_label = dict(Resource.RESOURCE_TYPE_CHOICES).get(resource_type)
    return render(request, 'reports/resource_list.html', {'resources': resources, 'type_label': type_label})

# --- Heatmap Views ---

def incidents_heatmap(request):
    """Renders the heatmap page."""
    return render(request, 'reports/heatmap.html')

@cache_page(60 * 5) # Cache this view for 5 minutes
def report_locations_api(request):
    """API endpoint to provide report locations."""
    reports = Report.objects.filter(is_approved_for_map=True).exclude(latitude__isnull=True).exclude(longitude__isnull=True).values(
        'case_id', 'latitude', 'longitude', 'incident_type'
    )

    # Convert Decimal types to floats for JSON serialization
    locations = []
    for report in reports:
        report['latitude'] = float(report['latitude'])
        report['longitude'] = float(report['longitude'])
        locations.append(report)

    return JsonResponse(locations, safe=False)

def support_page(request):
    """Renders the support/donation page."""
    return render(request, 'reports/support.html')

def about_us(request):
    """Renders the About Us page."""
    return render(request, 'reports/about.html')