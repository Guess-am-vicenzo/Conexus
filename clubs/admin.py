from django.contrib import admin
from.models import Club, Member

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'club')  # Use actual fields
    search_fields = ('first_name', 'last_name', 'email', 'club__name')
    
admin.site.register(Club, ClubAdmin)
admin.site.register(Member, MemberAdmin)