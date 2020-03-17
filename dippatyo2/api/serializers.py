from rest_framework import serializers
from api.models import Sample, File, WordRelation, Word

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = ('__all__')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('__all__')

class word_serializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('__all__')

class wordRelation_serializer(serializers.ModelSerializer):
    word1 = serializers.StringRelatedField()
    word2 = serializers.StringRelatedField()
    date = serializers.StringRelatedField()
    class Meta:
        model = WordRelation
        fields = ('word1', 'word2', 'occurrences', 'date')
