from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate

from staff.models import User
from course.serializer import *
from course.models import *
from staff.serializer import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator


login_message = {
        'status': 403,
        'message': "You are not logged in",
        'type': 'error'
    }


def is_user_logged(request):
    return False if request.user.is_anonymous else True
 

@api_view(['GET', 'POST'])
def std_register(request):
    if request.method == 'POST':
        first_name = request.data.get('first_name').strip().capitalize()
        last_name = request.data.get('last_name').strip().capitalize()
        email = request.data.get('email').lower()
        pass1 = request.data.get('password')
        pass2 = request.data.get('password_confirm')
        try:
            if User.objects.get(email=email):
                return Response({'status': 400, 'message': 'User Already exists, Kindly Login!', 'type': 'error'})
        except User.DoesNotExist:
            if pass1 == pass2:
                User.objects.create_user(email=email, password=pass1, first_name=first_name,
                                         last_name=last_name)
                return Response({"status": 201, 'message': 'User Successfully Created, Kindly Login Again', 'type': 'success'})
            else:
                return Response({'status': 400, 'message': 'Password Does not match', 'type': 'error'})
    else:
        return Response({'status': 403, 'message': 'POST method is required', 'type': 'error'})


@api_view(['GET', 'POST'])
def login_(request):
    if request.method == 'POST':
        email = request.data.get("email").strip().lower()
        password = request.data.get("password").strip()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': 400, 'message': 'Student Does Not Exist', 'type': 'error'})
        else:
            if user.is_staff:
                return Response({'status': 403, 'message': 'You are a Staff User, user Staff Login!!', 'type': 'warning'})
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'status': 200, 'message': 'Student Logged-In Successfully', 'type': 'success', 'is_staff': user.is_staff})
            else:
                return Response({'status': 400, 'message': 'Wrong Password, Please Enter it again', 'type': 'error'})
    else:
        return Response({'status': 403, 'message': 'POST method is required', 'type': 'error'})    


@api_view(['GET'])
def std_logout(request):
    logout(request)
    return Response({'status': 200, 'message': 'Student Logged-out', 'type': 'success'})


class UserCRUDView(APIView):
    def get(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        user = request.user
        user_data = UserSerializer(user, many=False)
        return Response({'status': 200, 'data': user_data.data})

    def patch(self, request, pk=None, *args, **kwargs):
        if not request.data.get("email"):
            return Response({'status': 400, 'message': 'Email is required', 'type': 'error'})
        # try:
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 200, 'message': 'User Updated Succcessfully', 'data': serializer.data, 
            'type': 'success'})
        return Response({'status': 400, 'Invalid Data': '', 'type': 'error'})

    def delete(self, request, *args, **kwargs):
        if not is_user_logged(request):
            return Response(login_message)
        user = request.user
        user.delete()
        return Response({'status': 204, 'message': 'Profile deleted successfully', 'type': 'success'})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfTokenView(APIView):
    permission_classes = (AllowAny, )
    def get(self, request, format=None):
        return Response({'status': 200, 'message': 'csrf cookie sent'})
