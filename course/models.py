from django.db import models
from staff.models import User


class Courses(models.Model):
    subscription = models.ManyToManyField(User, through='Subscribed')
    id = models.AutoField(unique=True, null=False, primary_key=True)
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")

    def __str__(self):
        return self.name


class Test(models.Model):
    history = models.ManyToManyField(User, through='TestHistory')
    id = models.AutoField(unique=True, null=False, primary_key=True)
    test_name = models.CharField(max_length=255)
    duration = models.IntegerField(null=False)
    mark_per_question = models.IntegerField(null=False)
    description = models.TextField(null=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):
        return self.test_name


class MCQ(models.Model):
    id = models.AutoField(unique=True, null=False, primary_key=True)
    question = models.CharField(max_length=255, null=False)
    opt1 = models.CharField(max_length=255, null=False)
    opt2 = models.CharField(max_length=255, null=False)
    opt3 = models.CharField(max_length=255, null=False)
    opt4 = models.CharField(max_length=255, null=False)
    correct_opt = models.IntegerField(null=False)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


class Subscribed(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return f'{self.course_id.name}-{self.user.first_name} {self.user.last_name}'


class TestHistory(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    test_id = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marks_scored = models.IntegerField(default=0)
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.test_id.test_name}-{self.user.first_name} {self.user.last_name}'

