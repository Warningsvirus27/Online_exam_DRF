from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from rest_framework.generics import ListAPIView
from django.views.decorators.csrf import csrf_exempt
from .serializer import *
from student.views import login_message, is_user_logged


staff_message = {
    'status': 400,
    'message': "Staff User is Needed",
    'type': 'error'
}


class TestView(APIView):
    test_serializer = TestSerializer
    mcq_serializer = MCQSerializer

    def get(self, request, test_id=None, *args, **kwargs):
        if not (is_user_logged(request) and test_id):
            return Response({'status': 400, 'message': 'user not logged in or missing test id', 'type': 'error'})
        if not test_id:
            return Response({'status': 400, 'message': 'Test Id is missing', 'type':'error'})
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid test id', 'type': 'error'})
        else:
            test_data = TestView.test_serializer(test)
            test_mcqs = MCQ.objects.filter(test_id=test.id)
            mcq_data = TestView.mcq_serializer(test_mcqs, many=True)
            return Response({'status': 200, 'test': test_data.data, 'mcqs': mcq_data.data})
        
    def post(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response(staff_message)
        test_name = request.data.get('test_name')
        duration = request.data.get('duration')
        mark_per_question = request.data.get('mark_per_question')
        description = request.data.get('description')
        course_id = request.data.get('course_id')
        print(course_id)
        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid Course Id', 'type': 'error'})
        else:
            test = Test.objects.create(test_name=test_name, duration=duration, mark_per_question=mark_per_question,
            description=description, course_id=course)
            return Response({'status': 201, 'message': 'Test created successfully', 'type': 'success'})

    def patch(self, request, test_id, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response(staff_message)
        if not test_id:
            return Response({'status': 400, 'message': 'Test Id is required', 'type': 'error'})
        try:
            test = Test.objects.get(id=test_id)
        except Courses.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid test id', 'type': 'error'})
        else:
            serializer = TestView.test_serializer(test, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 201, 'message': 'Test Updated Successfully', 'data': serializer.data, 
                'type': 'success'})
            return Response({'status': 400, 'message': 'Invalid data', 'type': 'error'})
        
    def delete(self, request, test_id=None, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response(staff_message)
        if not test_id:
            return Response({'status': 400, 'message': 'Test id required', 'type': 'error'})
        try:
            test = Test.objects.get(id=test_id)
        except Courses.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid test id', 'type': 'error'})
        else:
            test.delete()
            return Response({'status': 204, 'message': 'Successfully deleted test', 'type': 'success'})


class MCQView(APIView):
    serializer_class = MCQSerializer

    # def get(self, request, mcq_id, *args, **kwargs):
    #     try:
    #         mcq = MCQ.objects.get(id=mcq_id)
    #     except MCQ.DoesNotExist:
    #         return Response({'status': 400, 'message': 'invalid MCQ Id', 'type': 'error'})
    #     else:
    #         mcq_data = MCQView.serializer_class(mcq, many=False)
    #         return Response({'status': 200, 'data': mcq_data.data})

    def post(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response(staff_message)
        question = request.data.get('question')
        option1 = request.data.get('opt1')
        option2 = request.data.get('opt2')
        option3 = request.data.get('opt3')
        option4 = request.data.get('opt4')
        correct_option = request.data.get('correct_opt')
        test_id = request.data.get("test_id")
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid Test Id', 'type': 'error'})
        else:
            mcq = MCQ.objects.create(question=question, opt1=option1, opt2=option2, opt3=option3, opt4=option4, 
            correct_opt=correct_option, test_id=test)
            return Response({'status': 201, 'message': 'MCQ created successfully', 'type': 'success'})

    def put(self, request, mcq_id, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response(staff_message)
        if not mcq_id:
            return Response({'status': 400, 'message': 'MCQ Id is required', 'type': 'error'})
        try:
            mcq = MCQ.objects.get(id=mcq_id)
        except MCQ.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid MCQ Id', 'type': 'error'})
        else:
            serializer = MCQView.serializer_class(mcq, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({'status': 400, 'message': 'Invalid data', 'type': 'error'})
        
    def delete(self, request, mcq_id, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response(staff_message)
        if not mcq_id:
            return Response({'status': 400, 'message': 'MCQ id required', 'type': 'error'})
        try:
            mcq = MCQ.objects.get(id=mcq_id)
        except MCQ.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid Test Id', 'type': 'error'})
        else:
            mcq.delete()
            return Response({'status': 204, 'message': 'Successfully deleted MCQ', 'type': 'success'})


class CourseGeneric(APIView):
    def get(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        user = request.user
        courses = Courses.objects.exclude(subscription=user)
        courses = CourseSerializer(courses, many=True)
        return Response({'status':200, 'data': courses.data, 'type': 'success'})


class TestGeneric(APIView):
    def get(self, request, course_id=None, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not course_id:
            return Response({'status': 400, 'message': 'Course Id is needed', 'type': 'error'})
        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return Response({'status': 400, 'messag': 'invalid course id', 'type': 'error'})
        else:
            tests = Test.objects.filter(course_id=course)
            tests_data = TestSerializer(tests, many=True)
            return Response({'status': 200, 'data': tests_data.data, 'type': 'success'})


class MCQGeneric(APIView):
    def get(self, request, test_id, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not test_id:
            return Response({'status': 400, 'message': 'Course Id is needed', 'type': 'error'})
        mcq = MCQ.objects.filter(test_id=test_id)
        return Response({'status': 200, 'data': MCQSerializer(mcq, many=True).data, 'type': 'success'})

class TestHistoryGeneric(APIView):
    def get(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        test_history_list = TestHistory.objects.filter(user=request.user)
        
        ret_list = []
        for index, obj in enumerate(test_history_list):
            test = Test.objects.get(id=obj.test_id.id)
            test_history = TestHistorySerializer(obj).data
            test_data = TestSerializer(test).data
            result = test_data.update(test_history)
            ret_list.append(test_data)
        return Response({'status': 200, 'data': ret_list, 'type': 'successs'})


class SubscribedView(APIView):
    def get(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        courses = Courses.objects.filter(subscription=request.user.email)
        subscriptions_data = CourseSerializer(courses, many=True)
        return Response({'status': 200, 'data': subscriptions_data.data, 'type': 'success'})

    def post(self, request, email, *args, **kwargs):
        if not (email and request.data.get("course_id")):
            return Response({'status': 400, 'message': 'Email or Coures_Id is missing', 'type': 'error'})
        try:
            course = Courses.objects.get(id=request.data.get('course_id'))
        except Courses.DoesNotExist:
            return Response({'status': 400, 'message': 'invalid course id', 'type': 'error'})
        else:
            try:
                Subscribed.objects.get(user=request.user, course_id=course)
                return Response({'status': 400, 'message': 'Course Already subscribed!!', 'type': 'warning'})
            except Subscribed.DoesNotExist:
                Subscribed.objects.create(course_id=course, user=request.user)
                return Response({'status': 201, 'message': "course, subscribed successfully", 'type': 'success'})

    def delete(self, request, email, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not (email or course_id):
            return Response({'status': 400, 'message': 'Email or Course_id is missing', 'type': 'error'})
        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return Response({'status': 400, 'message': 'invalid course id', 'type': 'error'})
        else:
            try:
                print(course, request.user.email)
                subscribed_course = Subscribed.objects.get(course_id=course, user=request.user.email)
                subscribed_course.delete()
                return Response({'status': 204, 'message': "subscription deleted successfully", 'type': 'success'})
            except Subscribed.DoesNotExist:
                return Response({'status': 400, 'messag': 'No Subscription exist', 'type': 'error'})


@api_view(['GET'])
def user_data(request):
    if not is_user_logged(request):
        return Response(login_message)
    number_of_course = Subscribed.objects.filter(user=request.user.email).count()
    number_of_test = TestHistory.objects.filter(user=request.user.email).count()
    return Response({'status': 200, 'data': {'course': number_of_course, 'test': number_of_test}, 'type': 'success'})


@api_view(['POST'])
def evaluate(request, test_id=None):
    if not (test_id and request.data.get('answers')):
        return Response({'status': 400, 'message': 'Test_Id or Answer list is missing', 'type': 'error'})
    if not is_user_logged(request):
        return Response(login_message)
    try:
        test = Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return Response({'status': 400, 'message': 'invalid test id', 'type': 'error'})
    else:
        score = 0
        try:
            for mcq_id, option in request.data.get('answers').items():
                mcq = MCQ.objects.get(id=mcq_id)
                correct_opt = mcq.correct_opt
                mapper = {
                    1: mcq.opt1,
                    2: mcq.opt2,
                    3: mcq.opt3,
                    4: mcq.opt4,
                }
                print(correct_opt, mapper[correct_opt])
                if mapper[correct_opt] == option:
                    score += test.mark_per_question
            TestHistory.objects.create(test_id=test, user=request.user, marks_scored=score)
            return Response({'status': 200, 'data': score})
        except MCQ.DoesNotExist:
            return Response({'status': 400, 'message': 'wrong data', 'type': 'error'})
    
