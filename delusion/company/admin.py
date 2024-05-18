from django.contrib import admin
from delusion.company.models import (
    Company,
    Message,
    MessageFile,
    Ticket,
    TicketFile,
    Worker,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )
    list_display = (
        'id',
        'name',
        'description',
        'parent_company',
        'mesh_id'
    )


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = (
        'id',
        'company',
        'user',
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'priority', 'status',  'created_at')
    list_filter = ('priority', 'sender', 'status',  'created_at')
    search_fields = ('title', 'sender', 'priority', 'status',  'created_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'sender', 'created_at')
    list_filter = ('ticket', 'sender', 'created_at')
    search_fields = ('ticket', 'sender', 'created_at')



admin.site.register(MessageFile)
admin.site.register(TicketFile)