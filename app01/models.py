from django.db import models
from rbac.models import UserInfo as RbacUserInfo


# Create your models here.


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(RbacUserInfo):
    """
    用户表
    """
    # name = models.CharField(verbose_name='用户名', max_length=32)
    # password = models.CharField(verbose_name='密码', max_length=64)
    # email = models.CharField(verbose_name='邮箱', max_length=32)
    # roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

    # user = models.OneToOneField(verbose_name="用户", to=RbacUserInfo, on_delete=models.CASCADE)
    phone = models.CharField(verbose_name="联系方式", max_length=32)
    level_choices = (
        (1, 'T1'),
        (2, 'T2'),
        (3, 'T3'),
    )
    level = models.IntegerField(verbose_name="级别", choices=level_choices)

    depart = models.ForeignKey(verbose_name='部门', to='Department', on_delete=models.CASCADE)



class Host(models.Model):
    """
    主机表
    """
    hostname = models.CharField(verbose_name='主机名', max_length=32)
    ip = models.GenericIPAddressField(verbose_name='IP', protocol='both')
    depart = models.ForeignKey(verbose_name="归属部门", to='Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname
