# from sorl import thumbnail
from rest_framework import serializers

from education.catalogue.models import (Category, Example, Answer,
    ExampleImage, AnswerImage)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id',
                'path',
                'depth',
                'numchild',
                'name',
                'image',
                'image_name')

class AnswerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerImage
        fields = ('image',
            'image_name')

class ExampleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleImage
        fields = ('image',
            'image_name')

class AnswerSerializer(serializers.ModelSerializer):
    images = AnswerImageSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ('id',
            'answer',
            'images')

class ExampleSerializer(serializers.ModelSerializer):
    images = ExampleImageSerializer (many=True, read_only=True)
    answers = AnswerSerializer (many=True, read_only=True)

    class Meta:
        model = Example
        fields = ('id',
            'content',
            'answers',
            'images')
