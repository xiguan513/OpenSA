from django.db import models
from asset import models as assetModels

# Create your models here.

class TemplateStorage(models.Model):
    stroname = models.CharField(verbose_name='存储名称',max_length=100)
    claimname = models.CharField(verbose_name='pvc名称',max_length=100)
    mountpath = models.CharField(verbose_name='挂载路径',max_length=100)

    class Meta:
        db_table = 'storage'
        verbose_name = '存储模板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stroname


class TemplatePod(models.Model):
    name = models.CharField(verbose_name='模板名称',max_length=50)
    configmap = models.CharField(verbose_name='环境变量', max_length=20)
    harbor = models.CharField(verbose_name='镜像仓库', max_length=20)
    common = models.CharField(verbose_name='运行命令', max_length=200)
    args = models.CharField(verbose_name='命令参数', max_length=20)
    path = models.CharField(verbose_name='验证地址', max_length=100, default="/")
    port = models.BigIntegerField(verbose_name='容器端口')
    replicas = models.SmallIntegerField(verbose_name='副本数')
    requestsMem = models.CharField(verbose_name='需求内存',max_length=10)
    requestsCpu = models.CharField(verbose_name='需求CPU',max_length=10)
    limitsMem = models.CharField(verbose_name='限制内存',max_length=10)
    rlimitsCpu = models.CharField(verbose_name='限制CPU',max_length=10)
    initialDelaySeconds = models.CharField(verbose_name='初始化时间',max_length=10)
    periodSeconds = models.CharField(verbose_name='测试间隔',max_length=10)
    timeoutSeconds = models.CharField(verbose_name='超时时间',max_length=10)
    storage = models.ForeignKey(TemplateStorage,on_delete=models.CASCADE,null=True,default=None,verbose_name='存储',blank=True)

    class Meta:
        db_table = 'template'
        verbose_name = '基础模板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class GitInfo(models.Model):
    git_name = models.CharField(verbose_name='服务名称',max_length=50)
    git_http = models.CharField(verbose_name='Http地址',max_length=100)
    git_ssh = models.CharField(verbose_name='ssh地址',max_length=100)
    git_env = models.ForeignKey(assetModels.ServerUse,on_delete=models.CASCADE,verbose_name='项目环境')
    git_sort = models.SmallIntegerField(verbose_name="排序",blank=True,null=True)
    git_tag = models.ForeignKey(TemplatePod, verbose_name='模板名称', on_delete=models.CASCADE)

    class Meta:
        db_table = 'gitinfo'
        verbose_name = 'Git信息'
        verbose_name_plural = verbose_name
        ordering = ['git_sort']
        unique_together = (('git_name', 'git_ssh', 'git_http'),)
    def __str__(self):
        return self.git_name


class UpdateInfo(models.Model):
    server_name = models.CharField(verbose_name="服务名称",max_length=100)
    image_name = models.CharField(verbose_name="镜像名字",max_length=100,null=True,blank=True)
    pro_env = models.CharField(verbose_name="运行环境",max_length=10,null=True)
    image_env = models.CharField(verbose_name='项目环境', max_length=10,null=True)
    branch_env = models.CharField(verbose_name="分支信息", max_length=50, default='master')
    build_uuid = models.UUIDField(verbose_name="uuid",null=True)
    create_time = models.DateTimeField(verbose_name="打包时间", auto_now_add=True)
    class Meta:
        db_table = 'updateinfo'
        verbose_name = '服务更新记录'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.image_name


class DeployStatus(models.Model):
    env_name = models.CharField(verbose_name='环境名称',max_length=50,null=True)
    renew_status = models.CharField(verbose_name='更新状态',max_length=50,null=True)
    server_name = models.CharField(verbose_name='服务名称',max_length=250,null=True)
    branch_env = models.CharField(verbose_name="上线分支", max_length=50,default='master')
    build_uuid = models.UUIDField(verbose_name='uuid',null=True)
    create_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True, null=True)


    class Meta:
        db_table = 'deploystatus'
        verbose_name = '部署状态记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.renew_status


class Release(models.Model):
    server_name = models.CharField(verbose_name='服务名称',max_length=100)
    image_name = models.CharField(verbose_name="镜像名字",max_length=100,null=True,blank=True)
    branch_env = models.CharField(verbose_name="上线分支",max_length=50)
    status = models.CharField(verbose_name="latest", max_length=50, default="latest")
    create_time = models.DateTimeField(verbose_name="镜像创建时间", auto_now=True)



    class Meta:
        db_table = 'release'
        verbose_name = '阿里云上线记录'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
        unique_together = (('server_name','status','branch_env'))

    def __str__(self):
        return self.image_name



class Codefreeze(models.Model):
    project_name = models.CharField(verbose_name="项目名",max_length=100)
    checkout_branch = models.CharField(max_length=100,null=True)
    code_freeze = models.CharField(max_length=100,blank=True, null=True)
    git_tag = models.CharField(max_length=100,null=True)
    status = models.CharField(max_length=10,blank=True,null=True,default=0)

    def __str__(self):
        return self.code_freeze

    class Meta:
        db_table = 'codefreeze'
        verbose_name = "封板"
        verbose_name_plural = verbose_name


