from django.db import models

# Create your models here.


class TemplatePod(models.Model):
    name = models.CharField(verbose_name='模板名称',max_length=50)
    namespace = models.CharField(verbose_name='命名空间', max_length=50)
    configmap = models.CharField(verbose_name='环境变量', max_length=20)
    harbor = models.CharField(verbose_name='镜像仓库', max_length=20)
    image_com = models.CharField(verbose_name='运行命令', max_length=200)
    image_arg = models.CharField(verbose_name='命令参数', max_length=20)
    image_path = models.CharField(verbose_name='验证地址', max_length=100, default="/")
    immage_port = models.BigIntegerField(verbose_name='容器端口')

    class Meta:
        db_table = 'template'
        verbose_name = 'Pod基础模板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class GitInfo(models.Model):
    git_name = models.CharField(verbose_name='服务名称',max_length=50)
    git_http = models.CharField(verbose_name='Http地址',max_length=100)
    git_ssh = models.CharField(verbose_name='ssh地址',max_length=100)
    git_env = models.CharField(verbose_name='环境',max_length=10)
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










