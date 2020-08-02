from django.db import models
from datetime import datetime


class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name

class Sample(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    message = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

class WordManager(models.Manager):
    def createWord(self, word):
        wrd, created = Word.objects.get_or_create(word=word)
        wrd.occurrences +=1
        wrd.save()
        return wrd

class Word(models.Model):
    word = models.CharField(max_length=101)
    occurrences = models.IntegerField(default=0)
    objects = WordManager()
    def __str__(self):
        return self.word
    class Meta:
        ordering = ['-occurrences']

class DateManager(models.Manager):
    def createDateOfPost(self, timestamp):
        date = datetime.fromtimestamp(timestamp / 1e3) 
        date.replace(hour=0, minute=0, second=0, microsecond=0)
        dop, created = DateOfPost.objects.get_or_create(dateOfPost=date)
        dop.occurrences += 1
        dop.save()
        return dop

class DateOfPost(models.Model):
    dateOfPost = models.DateTimeField()
    occurrences = models.IntegerField(default=0)
    objects = DateManager()
    def __str__(self):
        return str(self.dateOfPost)

class WordRelationManager(models.Manager):
    def createWordRelation(self, word1, word2, wordDistance):
        try:
            wrdRel, created = WordRelation.objects.get_or_create(word1 = word1, word2 = word2)
        except WordRelation.MultipleObjectsReturned:
            duplicates = WordRelation.objects.filter(word1 = word1, word2 = word2)
            wrdRel = duplicates[0]
            for dup in duplicates[1:]:
                dup.delete()
        if wordDistance <3:
            wrdRel.closeDistance += 1
        elif wordDistance < 6:
            wrdRel.shortDistance += 1
        elif wordDistance < 9:
            wrdRel.mediumDistance += 1
        elif wordDistance < 15:
            wrdRel.longDistance += 1 

        wrdRel.occurrences += 1
        wrdRel.save()
        #wrdRel.date.add(date)
        return wrdRel

class WordRelation(models.Model):
    word1 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="word1")
    word2 = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="word2")
    occurrences = models.IntegerField(default=0)
    inComment = models.IntegerField(default=0)
    objects = WordRelationManager()
    #date = models.ForeignKey(DateOfPost, on_delete=models.CASCADE)
    closeDistance = models.IntegerField(default=0) #1-2
    shortDistance = models.IntegerField(default=0) #3-5
    mediumDistance = models.IntegerField(default=0) #6-8
    longDistance = models.IntegerField(default=0) #9-14
    def __str__(self):
        return self.word1.word + "-" + self.word2.word
    class Meta:
        ordering = ['-occurrences']
        


class NicknameOfPosterManager(models.Manager):
    def createNickname(self, name, wordPair):
        nn, created = NicknameOfPoster.objects.get_or_create(nickname = name)
        nn.numberOfPosts += 1
        nn.wordRelation.add(wordPair)
        nn.save()
        return nn


class NicknameOfPoster(models.Model):
    nickname = models.CharField(max_length=100)
    numberOfPosts = models.IntegerField(default=0)
    wordRelation = models.ManyToManyField(WordRelation)
    objects = NicknameOfPosterManager()
    def __str__(self):
        return self.nickname

class Keywords(models.Model):
    word = models.CharField(max_length=100)
    occurrences = models.IntegerField(default=0)
    subforum = models.ForeignKey(WordRelation, on_delete=models.CASCADE, blank=True, null=True)

class Stats(models.Model):
    threads = models.IntegerField(default=0)
    totalComments = models.IntegerField(default=0)
    wordPairs = models.IntegerField(default=0)