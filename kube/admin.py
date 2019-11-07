from django.contrib import admin
from .models import GitInfo,UpdateInfo,TemplatePod,TemplateStorage,DeployStatus,Release,Codefreeze
from asset.models import Work_Env

# Register your models here.

@admin.register(Work_Env)
class WorkEnvAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(GitInfo)
class GitInfoAdmin(admin.ModelAdmin):
    list_display = ['id','git_name','git_http','git_ssh','git_env','git_sort','git_tag']
    list_per_page = 50
    list_display_links = ('id',)
    list_filter = ('git_http','git_ssh','git_name','git_env','git_sort')
    search_fields = ('git_name','git_env__name')
    ordering = ['git_sort']


@admin.register(TemplatePod)
class TemplatePodAdmin(admin.ModelAdmin):
    list_display = ['id','name','configmap','harbor','common','args','path','port','replicas',
                    'requestsMem','requestsCpu','limitsMem','rlimitsCpu','initialDelaySeconds',
                    'periodSeconds','timeoutSeconds','storage']

@admin.register(TemplateStorage)
class TemplateStorageAdmin(admin.ModelAdmin):
    list_display = ['id','stroname','claimname','mountpath']


@admin.register(UpdateInfo)
class UpdateInfoAdmin(admin.ModelAdmin):
    list_display = ['id','server_name','image_name','pro_env','image_env','branch_env','create_time']
    ordering = ['-create_time']
    search_fields = ('pro_env','server_name__git_name')



@admin.register(DeployStatus)
class DeployStatusAdmin(admin.ModelAdmin):
    list_display = ['id','env_name','renew_status','server_name','create_time','branch_env','build_uuid']
    search_fields = ('renew_status', 'env_name','server_name')
    ordering = ['-create_time']


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ['id','server_name','image_name','create_time','branch_env']
    search_fields = ('server_name', 'branch_env')
    ordering = ['-create_time']


@admin.register(Codefreeze)
class CodefreezeAdmin(admin.ModelAdmin):
    list_display = ['id','project_name','checkout_branch','code_freeze','git_tag','status']

admin.site.site_header = '自动化运维'
admin.site.site_title = '自动化运维'