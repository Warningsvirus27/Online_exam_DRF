from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .models import *

from .serializer import *
from course.models import *
from course.serializer import TestSerializer, CourseSerializer
from student.views import login_message, is_user_logged


@api_view(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        first_name = request.data.get('first_name').strip().capitalize()
        last_name = request.data.get('last_name').strip().capitalize()
        email = request.data.get('email').lower()
        pass1 = request.data.get('password')
        pass2 = request.data.get('password_confirm')
        try:
            if User.objects.get(email=email):
                return Response({'status': 400, 'message': 'User Already Exists, Kindly Login', 'type': 'error'})
        except User.DoesNotExist:
            if pass1 == pass2:
                User.objects.create_staff_user(email=email, password=pass1, first_name=first_name,
                                         last_name=last_name)
                return Response({"status": 201, 'message': 'User created successfully', 'type': 'success'})
            else:
                return Response({'status': 400, 'message': 'Password Does Not Match', 'type': 'error'})
    else:
        return Response({'status': 403, 'message': 'POST method is required', 'type': 'error'})


@api_view(['GET', 'POST'])
def staff_login(request):
    if request.method == 'POST':
        email = request.data.get("email").strip().lower()
        password = request.data.get("password").strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': 400, 'message': 'Staff Does Not Exist', 'type': 'error'})
        else:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return Response({'status': 200, 'message': 'Staff Logged-In Successfully', 'type': 'success'})
                else:
                    return Response({'status': 403, 'message': 'You are not Staff User', 'type': 'error'})
            else:
                return Response({'status': 400, 'message': 'Wrong Password, Please Enter it again', 'type': 'error'})
    else:
        return Response({'status': 403, 'message': 'POST method is required', 'type': 'error'})    


class DisableStudentView(APIView):
    def get(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response({'status': 403, 'message': 'Staff Login is required', 'type': 'error'})
        student = User.objects.filter(is_staff=False, is_superuser=False, is_active=False)
        student_count = student.count()
        student_data = UserSerializer(student, many=True)
        return Response({'status': 200, 'data': student_data.data, 'count': student_count})

    def post(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        user = request.data.get('email')
        try:
            student_model = User.objects.get(email=user)
            if student_model.is_active:
                student_model.is_active = False
            else:
                student_model.is_active = True
            student_model.save()
        except User.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid Email', 'type': 'error'})
        else:
            return Response({'status': 200, 'message': 'User Altered', 'type': 'success'})


class CourseView(APIView):
    serializer_class = CourseSerializer

    def get(self, request, course_id=None, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response({'status': 403, 'message': 'You are not a staff User', 'type': 'error'})
        if course_id:
            try:
                course = Courses.objects.get(id=course_id)
            except Courses.DoesNotExist:
                return Response({'status': 400, 'message': 'invalid course id', 'type': 'error'})
            course_data = CourseView.serializer_class(course)
            return Response({'status': 200, 'data': course_data.data, 'type': 'success'})
        else:
            course = Courses.objects.filter(staff_id=request.user)
            course_data = CourseSerializer(course, many=True)
            return Response({'status': 200, 'data': course_data.data, 'type': 'success'})

    def post(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not request.user.is_staff:
            return Response({'status': 403, 'message': 'You are not a Staff User', 'type': 'error'})
        email = request.user
        course_name = request.data.get('name')
        description = request.data.get('description')
        course = Courses.objects.create(name=course_name, description=description, staff_id=email)
        return Response({'status': 201, 'data': CourseSerializer(course).data, 'message': 'Course created successfully', 
        'type': 'success'})

    def patch(self, request, course_id, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not course_id:
            return Response({'status': 400, 'message': 'Course Id is required', 'type': 'error'})
        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid Course Id', 'type': 'error'})
        else:
            serializer = CourseView.serializer_class(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 200, 'data': serializer.data, 'message': 'Course Updated Successully', 'type': 'success'})
            return Response({'status': 400, 'message': 'Invalid data', 'type': 'error'})

    def delete(self, request, course_id, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        if not course_id:
            return Response({'status': 400, 'message': 'Course Id is required', 'type': 'error'})
        try:
            course = Courses.objects.get(id=course_id)
            print(course)
        except Courses.DoesNotExist:
            return Response({'status': 400, 'message': 'Invalid Course Id', 'type': 'error'})
        else:
            course.delete()
            return Response({'status': 204, 'message': 'Course deleted successfully', 'type': 'success'})


@api_view(['GET'])
def subscription_number(request):
    if not is_user_logged(request):
        return Response(login_message)
    if not request.user.is_staff:
        return Response({'status': 403, 'message': 'You are not a staff User', 'type': 'error'})
    course_id = list(Courses.objects.filter(staff_id=request.user).values_list('id', flat=True))
    suscription_count = 0
    for course in course_id:
        suscription_count += Subscribed.objects.filter(course_id=course).count()
    return Response({'status': 200, 'data': suscription_count, 'type': ' success'})


@api_view(['GET'])
def search(request):
    print(request.data)
    users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)
    users_data = UserSerializer(users, many=True)
    return Response({'status': 200, 'data': users_data.data})
