from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import(
    User,
    Job,
    Application,
    SavedJob,
    Userprofile
)

# Register your models here.
class UserAdmin(UserAdmin):
    model= User
    list_display= ['id','email', 'first_name','last_name', 'role', 'is_staff']
    list_filter= ['role', 'is_active']
    search_fields= ['email', 'first_name', 'last_name']
    ordering= ['email']

    fieldsets= (
        (None, {'fields':('email', 'password')}),
        ('personal Info', {'fields':('first_name', 'last_name', 'role')}),
        ('permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('email', 'first_name', 'last_name', 'password', 'confirm_password', 'is_staff', 'is_superuser')
        }),
    )
    admin.site.register(User,UserAdmin)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display=['id','title','description', 'company_name','salary','requirements', 'recruiter', 'category', 'job_type', 'created_at', 'deadline']
    search_fields= ['title', 'company_name']
    list_filter= ['category', 'job_type', 'created_at']
    auto_complete= ['recruiter']

#inline Applications
class ApplicationInline(admin.TabularInline):
    model=Application
    extra=0
    readonly_fields= ['candidate', 'cover_letter','cv', 'status', 'applied_at']
    can_delete= False
    
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display= ['id' , 'job', 'candidate', 'applied_at' ]
    search_fields= ['candidate_email', 'job_title']
    list_filter=['applied_at']

#updating JobAdmin to include inline: 
JobAdmin.inlines= [ApplicationInline]


class UserProfileInline(admin.TabularInline):
    model=Userprofile
    can_delete=False
    verbose_name_plural= 'Profile'


class UserProfileAdmin(admin.ModelAdmin):
    list_display= ['email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter=['role', 'is_staff']
    search_fields= ['emails', 'first_name', 'last_name']
    ordering= ['email']
    inlines= [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Userprofile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'resume', 'bio')
    search_fields = ('user__email', 'bio')
    list_filter = ('user',)


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__email', 'job__title')
    list_filter = ('saved_at',)







