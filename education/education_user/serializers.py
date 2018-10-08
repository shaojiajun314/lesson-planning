from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
            'nickname',
            'mobile',
            'email')

class UserInfoSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username',
            'nickname',
            'mobile',
            'permissions')

    def get_permissions(self, obj):
        return {'modify_category': obj.has_perm('catalogue.modify_category'),
        'modify_example': obj.has_perm('catalogue.modify_example')}
