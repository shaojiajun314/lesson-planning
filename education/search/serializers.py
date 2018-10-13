from sorl import thumbnail
from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer
from education.catalogue.serializers import CategorySerializer, AnswerSerializer
from education.search.search_indexes import ExampleIndex

class ExampleIndexSerializer(HaystackSerializer):

    # answers = AnswerSerializer(many=True, read_only=True)
    # categories = CategorySerializer(many=True, read_only=True)
    id = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_id(self, obj):
        id_ = obj.object.id
        return id_

    def get_categories(self, obj):
        categories = obj.object.categories.all()
        return CategorySerializer(categories, many=True).data

    def get_answers(self, obj):
        answers = obj.object.answers.all()
        return AnswerSerializer(answers, many=True).data

    def get_content(self, obj):
        return obj.object.content

    class Meta:
        index_classes = [ExampleIndex]
        fields = ('id',
            'answers'
            'content',
            'categories',
            'difficulty',)
