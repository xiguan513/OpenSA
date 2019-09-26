from django.db import models
from asset import models as assetModels

# Create your models here.


class TemplatePod(models.Model):
    name = models.CharField(verbose_name='模板名称',max_length=50)
    namespace = models.ForeignKey(assetModels.Work_Env,on_delete=models.CASCADE,verbose_name='命名空间')
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
    rlimitsCpu = models.CharField(verbose_name='需求CPU',max_length=10)
    initialDelaySeconds = models.CharField(verbose_name='初始化时间',max_length=10)
    periodSeconds = models.CharField(verbose_name='重试',max_length=10)
    timeoutSeconds = models.CharField(verbose_name='超时',max_length=10)

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
    server_name = models.ForeignKey(GitInfo,on_delete=models.CASCADE,verbose_name="服务名称")
    image_name = models.CharField(verbose_name="镜像名字",max_length=100,null=True,blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    pro_env = models.CharField(verbose_name="运行环境",max_length=10,default="default")
    image_env = models.CharField(verbose_name='项目环境', max_length=10)

    class Meta:
        db_table = 'updateinfo'
        verbose_name = '服务更新记录'
        verbose_name_plural = verbose_name
        ordering = ['create_time']

    def __str__(self):
        return self.image_name










