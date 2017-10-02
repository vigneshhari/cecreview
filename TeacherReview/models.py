from __future__ import unicode_literals

from django.db import models

class Teacher(models.Model):
    teacher_class_id = models.IntegerField()
    name = models.CharField(max_length = 500)
    semester = models.CharField(max_length = 100)
    div = models.CharField(max_length = 100)

    def __str__(self):
        return "S" + self.semester + " " + self.div + " Taught by " + self.name + " alias T" + str(self.teacher_class_id)

class Review(models.Model):
    teacher = models.ForeignKey("Teacher")
    question = models.ForeignKey("Questions")
    ans = models.CharField(max_length = 1000)

class Questions(models.Model):
    question_no = models.IntegerField()
    question = models.CharField(max_length=500)

    def __str__(self):
        return str(self.question_no) + ". " + self.question


