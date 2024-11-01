import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

#class Question(models.Model):
#    question_text = models.CharField(max_length=200)
#    pub_date = models.DateTimeField("date published")


#class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text

class Persona(models.Model):
    persona_nom = models.CharField(max_length=200)
    persona_cognom1 = models.CharField(max_length=100)
    persona_data_naixement = models.DateTimeField('Data de naixement')
    
    def __str__(self):
        return self.persona_nom+" "+self.persona_cognom1


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # ...
    def __str__(self):
        return self.choice_text
