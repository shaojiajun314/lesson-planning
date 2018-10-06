from rest_framework import serializers

from education.analytics.models import ExampleRecord

class ExampleRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleRecord
        fields = ('num_assemble',)
