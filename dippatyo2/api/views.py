from api.models import Sample, WordRelation, Word
from django.shortcuts import get_object_or_404
from api.serializers import SampleSerializer, FileSerializer, word_serializer, wordRelation_serializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import status

from filescanner.views import Filescanner


class SampleListCreate(generics.ListAPIView):
    queryset = Sample.objects.all()
    serializer_class = SampleSerializer


class WordView(generics.ListCreateAPIView):
    queryset = Word.objects.all()
    serializer_class = word_serializer

class SingleWordView(generics.RetrieveAPIView):
    serializer_class = word_serializer
    def get_queryset(self):
        self.lookup_field = 'word'
        self.word = get_object_or_404(Word, word=self.kwargs['word'])
        return Word.objects.filter(word = self.word)

class WordRelationView(generics.ListCreateAPIView):
    queryset = WordRelation.objects.all()
    serializer_class = wordRelation_serializer
"""
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        words = WordRelation.objects.all()
        serializer = wordRelation_serializer
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        wordRelation_serializer = wordSerializer(data=request.data)
        if wordRelation_serializer.is_valid():
            wordRelation_serializer.save()
            return Response(wordRelation_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', wordRelation_serializer.errors)
            return Response(wordRelation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, req, format='json'):
        try:
            fileobj = req.FILES['file']
            destination = open('filescanner/uploadFiles/' + fileobj.name, 'wb+')
            for chunk in fileobj.chunks():
                destination.write(chunk)
            destination.close()

            return Response(fileobj.name, status.HTTP_201_CREATED)
        except:
            return Response("Internal server error, bad file format", status.HTTP_400_BAD_REQUEST)
        #file_serializer = FileSerializer(data=req.data)

        #if file_serializer.is_valid():
        #    file_serializer.save()
        #    return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        #else:
        #    print('error', file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Scan(APIView):

    def get(self, req, *args, **kwargs):
        res = Filescanner.scan()
        print("asd")
        return Response(res, status.HTTP_200_OK)