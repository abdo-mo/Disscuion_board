from django.contrib import admin
from .models import Board, Topic
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

admin.site.site_header = "DISCCUSION BOARD ADMIN PANEL"
admin.site.site_title = "Boards admin panel"


class InlineTopic(admin.StackedInline):
    model = Topic
    extra = 1

class BoardAdmin(admin.ModelAdmin):
    inlines = [InlineTopic]

class TopicAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    fields = ('subject', 'board', 'created_by', 'views')
    list_display = ('subject', 'board', 'created_by', 'combineSubjectBoard')
    list_display_links = ('board', 'created_by')
    list_editable = ('subject',)
    list_filter = ('board', 'created_by')
    search_fields = ('board__name', 'created_by__username')

    def combineSubjectBoard(self, obj):
        return "{} - {}".format(obj.subject, obj.board)


# Register your models here.
admin.site.register(Board, BoardAdmin)
admin.site.register(Topic, TopicAdmin)


