from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class WxUser(AbstractUser):
    # 微信同步的用户信息
    openid = models.CharField(_('微信小程序OpenID'), max_length=100, unique=True, null=True, blank=True)
    openid_gzh = models.CharField(_('微信公众号OpenID'), max_length=100, unique=True, null=True, blank=True)
    avatar_url = models.URLField(_('头像'), null=True, blank=True)
    nick_name = models.CharField(_('昵称'), max_length=100, null=True, blank=True, unique=True)
    gender = models.SmallIntegerField(
        verbose_name=_('性别'), help_text=_('0-->未知, 1-->男, 2-->女'),
        choices=((1, '男'), (2, '女'), (0, '未知')), default=0)
    language = models.CharField(_('语言'), max_length=100, null=True, blank=True)
    city = models.CharField(_('城市'), max_length=200, null=True, blank=True)
    province = models.CharField(_('省份'), max_length=200, null=True, blank=True)
    country = models.CharField(_('国家'), max_length=200, null=True, blank=True)
    # 附加信息
    full_name = models.CharField(_('真实姓名'), max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(_('出生日期'), null=True, blank=True)
    desc = models.TextField(_('描述'), max_length=2000, null=True, blank=True)
    mobile = models.CharField(_('手机号'), max_length=100, null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        ordering = ['-id']

    def __str__(self):
        if self.full_name:
            res = self.full_name
        else:
            res = self.username
        return "[{0}] {1}".format(
            self.pk,
            res,
        )


class Family(models.Model):
    name = models.CharField(_('名称'), max_length=255, null=True)
    main_account = models.ForeignKey(
        WxUser,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_('主账号')
    )

    objects = models.Manager()

    class Meta:
        ordering = ['pk']
        verbose_name = _('家庭')
        verbose_name_plural = _('家庭')

    def total_invited_people_property(self):
        if self.pk:
            total_persons = InvitedPeople.objects.filter(
                related_family_id=self.pk
            ).aggregate(total_persons=Sum('persons'))
            return total_persons['total_persons']

    total_invited_people_property.short_description = "受邀人数"

    total_invited_people = property(total_invited_people_property)

    def __str__(self):
        return "{0} {1}".format(
            self.name, self.main_account
        )


class FamilyMember(models.Model):
    family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        verbose_name=_('家庭')
    )
    member = models.ForeignKey(
        WxUser,
        on_delete=models.CASCADE,
        verbose_name=_('成员')
    )
    can_edit = models.BooleanField(_('可编辑'), default=False)

    objects = models.Manager()

    class Meta:
        ordering = ['pk']
        verbose_name = _('家庭成员')
        verbose_name_plural = _('家庭成员')

    def __str__(self):
        return "{0} {1}".format(
            self.family, self.member
        )


class Table(models.Model):
    name = models.CharField(_('名称'), max_length=255, null=True)
    desc = models.TextField(_('描述'), max_length=1000, null=True, blank=True)
    max_persons = models.PositiveSmallIntegerField(_('最多人数'), default=10)
    related_family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        verbose_name=_('关联家庭')
    )

    objects = models.Manager()

    class Meta:
        ordering = ['name']
        verbose_name = _('桌子')
        verbose_name_plural = _('桌子')

    def __str__(self):
        return "{0}".format(
            self.name,
        )


class Category(models.Model):
    name = models.CharField(_('名称'), max_length=255, null=True)
    related_family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        verbose_name=_('关联家庭')
    )

    objects = models.Manager()

    class Meta:
        ordering = ['name']
        verbose_name = _('受邀人归类')
        verbose_name_plural = _('受邀人归类')

    def __str__(self):
        return "{0}".format(
            self.name,
        )


class InvitedPeople(models.Model):
    name = models.CharField(_('名称'), max_length=255, null=True)
    mobile = models.CharField(_('手机号'), max_length=100, null=True, blank=True)
    related_family = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        verbose_name=_('关联家庭')
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('桌子')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('归类')
    )
    persons = models.SmallIntegerField(_('人数'),  default=1)
    has_gift = models.BooleanField(_('收礼金'), null=True)
    gift_amount_pred = models.IntegerField(_('礼金金额预计'), null=True, blank=True)
    gift_amount_real = models.IntegerField(_('礼金金额实际'), null=True, blank=True)
    percentage = models.SmallIntegerField(
        _('参加概率'),  default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])

    objects = models.Manager()

    class Meta:
        ordering = ['name']
        verbose_name = _('受邀人员')
        verbose_name_plural = _('受邀人员')

    def __str__(self):
        return "{0}".format(
            self.name,
        )
