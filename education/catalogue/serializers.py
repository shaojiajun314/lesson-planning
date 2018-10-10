from sorl import thumbnail
from rest_framework import serializers

from education.catalogue.models import (Category, Example, Answer,
    ExampleImage, AnswerImage, CourseWare, ExaminationOutline)
from education.analytics.serializers import ExampleRecordSerializer as ExampleAnalyticsRecordSerializer

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        im = thumbnail.get_thumbnail(obj.image,
            '256x256', crop='bottom', upscale=False)
        try:
            return im.url
        except:
            return ''

    class Meta:
        model = Category
        fields = ('id',
                'path',
                'depth',
                'numchild',
                'name',
                'image',
                'image_name')

# class CategoryDetailSerializer(serializers.ModelSerializer):
#     # ancestors = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Category
#         fields = ('id',
#                 'path',
#                 'depth',
#                 'numchild',
#                 'name',
#                 'image',
#                 'image_name')
#
#     # def get_ancestors(self, obj):
#     #     qs = obj.get_ancestors()
#     #     return CategorySerializer(qs, many=True).data

class AnswerImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        im = thumbnail.get_thumbnail(obj.image,
            '375x375', crop='bottom', upscale=False)
        try:
            return im.url
        except:
            return ''

    class Meta:
        model = AnswerImage
        fields = ('image',
            'image_name',
            'id')

class ExampleImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        im = thumbnail.get_thumbnail(obj.image,
            '375x375', crop='bottom', upscale=False)
        try:
            return im.url
        except:
            return ''

    class Meta:
        model = ExampleImage
        fields = ('image',
            'image_name',
            'id',)

class AnswerSerializer(serializers.ModelSerializer):
    images = AnswerImageSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ('id',
            'answer',
            'images')

class ExampleSerializer(serializers.ModelSerializer):
    images = ExampleImageSerializer(many=True, read_only=True)
    analytics = ExampleAnalyticsRecordSerializer(many=False, read_only=True)

    # answers = AnswerSerializer (many=True, read_only=True)

    class Meta:
        model = Example
        fields = ('id',
            'content',
            # 'answers',
            'images',
            'difficulty',
            'analytics',)

class ExampleDetailSerializer(serializers.ModelSerializer):
    images = ExampleImageSerializer(many=True, read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Example
        fields = ('id',
            'content',
            'answers',
            'images',
            'categories',
            'difficulty')

class CourseWareSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseWare
        fields = '__all__'

class CourseWareDeailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = CourseWare
        fields = ('categories',
            'date_created',
            'title',
            'description',
            'file',)

class ExaminationOutlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExaminationOutline
        fields = '__all__'

class ExaminationOutlineDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ExaminationOutline
        fields = ('categories',
            'date_created',
            'title',
            'description',
            'file',)
