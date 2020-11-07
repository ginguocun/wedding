from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.admin import UserAdmin
from django.db.models import AutoField, CharField, TextField, BooleanField, DateTimeField, DateField, EmailField, \
    SmallIntegerField, PositiveSmallIntegerField, URLField, ForeignKey, Q
from django.utils.translation import gettext_lazy as _

from main.models import *


@admin.register(WxUser)
class WxUserAdmin(UserAdmin):
    readonly_fields = (
        'last_login', 'date_joined', 'nick_name', 'city', 'province', 'country', 'avatar_url',
    )
    list_display = [
        'pk', 'username', 'full_name', 'nick_name', 'mobile',
        'is_staff', 'is_superuser', 'date_joined', 'last_login']
    list_display_links = ['pk', 'username', 'full_name', 'nick_name']
    search_fields = [
        'username', 'openid', 'email', 'mobile', 'full_name', 'first_name', 'last_name', 'nick_name']
    list_filter = ('is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (_('基础信息'), {'fields': ('username', 'password', 'openid')}),
        (_('个人信息'), {'fields': (
            'nick_name', 'first_name', 'last_name', 'full_name', 'avatar_url', 'gender', 'date_of_birth', 'desc'
        )}),
        (_('联络信息'), {'fields': ('mobile', 'email',)}),
        (_('地址信息'), {'fields': ('city', 'province', 'country')}),
        (_('权限管理'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (_('登录信息'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    readonly_fields = ['main_account']
    list_display = ['pk', 'name', 'total_invited_people']

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(
            Q(main_account_id=request.user.id) | Q(familymember__member_id=request.user.id))
        return qs

    def save_model(self, request, instance, form, change):
        # 自动保存创建人员
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.main_account:
            instance.main_account = user
        instance.save()
        form.save_m2m()
        return instance


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['pk', 'family', 'member']
    list_display_links = ['pk', 'family']
    list_filter = ['member']

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(
            Q(family__main_account_id=request.user.id) | Q(member_id=request.user.id)
        )
        return qs


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'desc', 'max_persons', 'related_family', 'related_session']
    list_display_links = ['pk', 'name']
    list_filter = ['related_family', 'related_session']

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(
            Q(
                related_family__main_account_id=request.user.id
            ) | Q(
                related_family__familymember__member_id=request.user.id
            )
        )
        return qs


@admin.register(InvitedPeople)
class InvitedPeopleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'mobile', 'related_family', 'table', 'category', 'persons', 'has_gift', 'percentage']
    list_display_links = ['pk', 'name']
    list_filter = ['category', 'related_family', 'has_gift']
    filter_horizontal = ['session']

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(related_family__main_account_id=request.user.id)
        return qs


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'related_family']
    list_display_links = ['pk', 'name']
    list_filter = ['related_family']

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(related_family__main_account_id=request.user.id)
        return qs


app_models = apps.get_app_config('main').get_models()

# 需要显示的字段类型
list_display_types = [
    AutoField, CharField, TextField, BooleanField, DateTimeField, DateField,
    EmailField, SmallIntegerField, PositiveSmallIntegerField, URLField, ForeignKey]

# 可以用于筛选的字段类型
list_filter_types = [ForeignKey, ]

# 不显示的字段
exclude_field_names = ['id', 'password']

for model in app_models:  # 遍历所有的 models
    try:
        list_display = ['pk', '__str__']
        list_filter = []
        for f in getattr(model, '_meta').fields:  # 遍历所有的字段
            if type(f) in list_display_types:  # 如果字段在需要显示的字段类型列表内
                if f.name not in exclude_field_names:  # 排除不需要显示的字段
                    list_display.append(f.name)
            if type(f) in list_filter_types:
                if f.name in list_display:
                    list_filter.append(f.name)
        admin.site.register(
            model,
            list_display=list_display,  # 列表页面显示的字段
            list_display_links=['pk', '__str__'],  # 列表页面可跳转至详情页面的字段
            list_filter=list_filter
        )
    except AlreadyRegistered:  # 避免重复注册报错
        pass
