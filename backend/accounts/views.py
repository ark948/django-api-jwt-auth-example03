from rest_framework.generics import GenericAPIView
from accounts.serializers import UserRegisterSerializer
from accounts.utils import send_code_to_user
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    # get data from request, validate it, if valid, create and return user object

    def post(self, request):
        # customizing the POST request of GenericAPIView
        user_data = request.data
        # get user data from request object
        serializer = self.serializer_class(data=user_data)
        # get the serilizer object filled with user data, which is UserRegisterSerializer
        if serializer.is_valid(raise_exception=True):
            # run its validation, if ok, continue
            serializer.save()
            # and save it
            user = serializer.data
            # the returned data will be a newly created user object
            send_code_to_user(user['email'])
            return Response({
                'data': user,
                'message': f'Thank you for signing up. Please check your email.',
            }, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # if validation of serializer with data failed, return 400 error