from rest_framework.serializers import ModelSerializer
from .models import *


class TestSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Courses
        fields = ['id', 'name', 'description']


class MCQSerializer(ModelSerializer):
    class Meta:
        model = MCQ
        fields = ['id', 'question', 'opt1', 'opt2', 'opt3', 'opt4', 'correct_opt']


class SubscribedSerializer(ModelSerializer):
    class Meta:
        model = Subscribed
        fields = "__all__"


class TestHistorySerializer(ModelSerializer):
    class Meta:
        model = TestHistory
        fields = "__all__"