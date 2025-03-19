from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_tracking.mixins import LoggingMixin
from accounts import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserAuthView(LoggingMixin, APIView):
    """This class handles User verification during login.
    If the user information like password and ... is valid, it returns JWT access and refresh tokens.
    """
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        ser_data = serializers.AuthSerializer(data=request.data)

        if ser_data.is_valid():
            try:
                # Get the authenticated user
                user = ser_data.validated_data['user']
                user_data = serializers.UserSerializer(instance=user)

                # set_token
                token = RefreshToken.for_user(user)

                return Response({
                    'user_data': user_data.data,
                    'jwt_token': {
                        'access_token': str(token.access_token),
                        'refresh_token': str(token),
                    }
                }, status=status.HTTP_200_OK)

            except Exception as e:
                # TODO: it is better if we set logging for e exception

                return Response(
                    {'message': 'An error occurred while processing your request. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(LoggingMixin, APIView):
    """ Logout apiview
    View for handling user logout by blacklisting a refresh token.
    This view allows authenticated users to log out by invalidating their refresh token.
    The user sends the refresh token in the request body, and the system attempts to blacklist it.
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        ser_data = serializers.LogoutSerializer(data=request.data)

        if ser_data.is_valid():
            try:
                refresh_token = RefreshToken(ser_data.validated_data['refresh_token'])
                refresh_token.blacklist()

                return Response(
                    {"detail": "Successfully logged out."},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Exception as e:
                print(e)
                return Response(
                    {'message': 'An error occurred while processing your request. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    """This class handles User registering.
    """
    def post(self, request):
        serializer = serializers.UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            ser_data = serializers.UserSerializer(instance=user)

            # set_token
            token = RefreshToken.for_user(user)

            return Response({
                'user_data': ser_data.data,
                'jwt_token': {
                    'access_token': str(token.access_token),
                    'refresh_token': str(token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

