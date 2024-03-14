from django.contrib import admin

from .models import CustomUser, Level
from .models import Faculty, Department,Amount, Gender, Hostel, Room, Block, Bunk, BedSpace,Complaint, Exeat, Upload, Payment

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'matric_number',
                    'faculty', 'department', 'level', 'gender',
                    'hostel', 'block', 'room', 'bunk', 'space', 'phone_number','has_paid_hostel_fee')
    search_fields =  ('matric_number', 'first_name', 'last_name')
    list_per_page = 100
admin.site.register(CustomUser, UserAdmin)

class PassAdmin(admin.ModelAdmin):
    list_display = ('user', 'faculty', 'department', 
                    'student_number', 'parent_number', 'departure_date',
                    'return_date', 'reason', 'status')
    search_fields =  ('parent_number', 'student_number')
    list_per_page = 100
admin.site.register(Exeat, PassAdmin)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'block_number', 'room_number',
                    'title', 'message', 'hostel_name')
    search_fields =  ( 'block_number', 'room_number', 'hostel')
    list_per_page = 100
admin.site.register(Complaint, ReportAdmin)


admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Gender)
admin.site.register(Room)
admin.site.register(Hostel)
admin.site.register(Block)
admin.site.register(Bunk)
admin.site.register(BedSpace)
admin.site.register(Upload)
admin.site.register(Amount)
admin.site.register(Level)
admin.site.register(Payment)