from django.contrib import admin
from .models import *
# Register your models here.

class FileUploadInline(admin.TabularInline):
    model           = FileUpload
    extra           = 0
    fields          = ('filename', 'status', 'upload_time', 'word_count')
    readonly_fields = ('upload_time', 'word_count')
    can_delete      = False
    show_change_link = True

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display    = ('id', 'filename', 'user_profile', 'status', 'word_count', 'upload_time')
    list_filter     = ('status', 'upload_time')
    search_fields   = ('filename', 'user_profile__user__username', 'user_profile__user__email')
    readonly_fields = ('upload_time',)
    ordering        = ('-upload_time',)

    fieldsets       = (
        (None, {
            'fields': ('user_profile', 'file', 'filename', 'status', 'word_count')
        }),
        ('Timestamps', {
            'fields': ('upload_time',),
            'classes': ('collapse',),
        }),
    )

    # set filename from uploaded file
    def save_model(self, request, obj, form, change):
        if not obj.filename:
            obj.filename = obj.file.name
        super().save_model(request, obj, form, change)

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display    = ('id', 'user_profile', 'action', 'timestamp')
    list_filter     = ('timestamp', 'action')
    search_fields   = ('user_profile__user__username', 'action')
    readonly_fields = ('timestamp',)
    ordering        = ('-timestamp',)

    fieldsets       = (
        (None, {
            'fields': ('user_profile', 'action', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('timestamp',),
            'classes': ('collapse',),
        }),
    )

    # print metadata JSON
    def formatted_metadata(self, obj):
        import json
        return json.dumps(obj.metadata, indent=2)

    formatted_metadata.short_description = 'Metadata (formatted)'