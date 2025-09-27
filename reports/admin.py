from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Report, Resource, EvidenceFile

# To make the admin more powerful, we can add custom actions.
@admin.action(description='Mark selected reports as Reviewed')
def mark_as_reviewed(modeladmin, request, queryset):
    """
    Custom admin action to change the status of selected reports.
    """
    queryset.update(status='reviewed')

class EvidenceFileInline(admin.TabularInline):
    """
    An inline for evidence files that provides a preview of the uploaded content.
    This is a huge UX improvement for admins.
    """
    model = EvidenceFile
    extra = 1
    # Add a preview for the file, especially useful for images.
    readonly_fields = ('uploaded_at', 'file_preview',)
    fields = ('file', 'file_preview', 'uploaded_at',)

    def file_preview(self, obj):
        # Check if the file has a URL and is an image type
        if obj.file and hasattr(obj.file, 'url'):
            # Simple check for image extensions
            if any(obj.file.url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150" height="auto" /></a>', obj.file.url)
        return "No Preview"
    file_preview.short_description = 'File Preview'

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('case_id_link', 'incident_type', 'colored_status', 'has_evidence_icon', 'is_approved_for_map', 'severity_level', 'created_at')
    list_filter = ('status', 'incident_type', 'is_approved_for_map', 'severity_level')
    search_fields = ('case_id', 'description', 'location')
    list_editable = ('is_approved_for_map', 'severity_level',)
    readonly_fields = ('case_id', 'created_at', 'incident_datetime', 'location', 'description', 'contact_method', 'contact_info')
    
    # Add the custom action here
    actions = [mark_as_reviewed]
    
    # Customise the layout of the detail view for better organization
    fieldsets = (
        ('Case Management', {
            'fields': ('case_id', 'status', 'is_approved_for_map', 'severity_level')
        }),
        ('Incident Details', {
            'classes': ('collapse',), # Make this section collapsible
            'fields': ('incident_type', 'incident_datetime', 'location', 'description', 'created_at')
        }),
        ('Contact Information', {
            'classes': ('collapse',),
            'fields': ('contact_method', 'contact_info')
        }),
    )
    
    inlines = [EvidenceFileInline]

    def case_id_link(self, obj):
        # Make the case_id clickable, leading to the detail view
        url = reverse('admin:reports_report_change', args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.case_id)
    case_id_link.short_description = 'Case ID'
    case_id_link.admin_order_field = 'case_id'

    def has_evidence_icon(self, obj):
        # Display a boolean checkmark icon instead of "Yes"/"No"
        return obj.evidence_files.exists()
    has_evidence_icon.short_description = 'Evidence'
    has_evidence_icon.boolean = True # This tells Django to render it as an icon

    def colored_status(self, obj):
        # Add colored tags for status for quick visual identification
        if obj.status == 'new':
            color = 'primary'
        elif obj.status == 'in_progress':
            color = 'warning'
        elif obj.status == 'resolved':
            color = 'success'
        else:
            color = 'secondary'
        return format_html('<span class="badge badge-{}">{}</span>', color, obj.get_status_display())
    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'created_at')
    list_filter = ('resource_type',)
    search_fields = ('title', 'content', 'source')
    fieldsets = (
        (None, {
            'fields': ('title', 'resource_type', 'content', 'source')
        }),
    )
