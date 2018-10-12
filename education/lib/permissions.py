#!coding:utf-8
from rest_framework.permissions import BasePermission

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff and request.user.is_active

class UpdateCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('catalogue.modify_category')

class UpdateExamplePermission(BasePermission):
    def has_permission(self, request, view):
        # 允许创建　验证修改权限
        if not view.kwargs.get('pk'):
            return True
        return request.user.has_perm('catalogue.modify_example')

class UpdateEDUFile(BasePermission):
    def has_permission(self, request, view):
        # 允许创建　验证修改权限
        if not view.kwargs.get('pk'):
            return True
        return request.user.has_perm('catalogue.modify_edufile')

# class UpdateCourseWare(BasePermission):
#     def has_permission(self, request, view):
#         # 允许创建　验证修改权限
#         if not view.kwargs.get('pk'):
#             return True
#         return request.user.has_perm('catalogue.modify_courseware')
