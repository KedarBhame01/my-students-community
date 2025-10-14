from django.shortcuts import render
from django.db.models import Q
from .serializers import Admins_serializer, Admins_login_serializer 
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status,filters
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Admins
# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
# JWT authentication class
#for jwt json web token
import jwt
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from utils.base_viewsets import BaseCRUDViewSet
from utils.base_viewsets import success_response, error_response
import logging

logger = logging.getLogger(__name__)
# Create your views here.

    
class AdminsLoginAPI(ModelViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_login_serializer
    
    @swagger_auto_schema(request_body=Admins_login_serializer)
    def login(self, request, *args, **kwargs):
        """Login API with comprehensive error handling"""
        try:
            # 🔹 Check if request data exists
            if not request.data:
                return error_response(
                    'No data provided. Please send email, password', 
                    code=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = self.serializer_class(data=request.data)

            if not serializer.is_valid():
                # 🔹 Better error messages for validation
                error_messages = []
                for field, errors in serializer.errors.items():
                    error_messages.append(f"{field}: {', '.join(errors)}")
                return error_response(
                    f"Validation failed: {'; '.join(error_messages)}", 
                    code=status.HTTP_400_BAD_REQUEST
                )

            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            # 🔹 Validate required fields
            if not email:
                return error_response('email is required', code=status.HTTP_400_BAD_REQUEST)
            if not password:
                return error_response('Password is required', code=status.HTTP_400_BAD_REQUEST)
            
            
            
            try:
                    Admins = Admins.objects.get(email=email)
                    data ={
                        "id": Admins.id,
                        'email': Admins.email,
                    }
                    # 🔹 Add password check with better error handling
                    try:
                        if check_password(password, Admins.password):
                            logger.info(f"Admins login successful for: {email}")
                            return success_response(
                                "Admins login successful",
                                data,
                                code=status.HTTP_200_OK
                            )
                        else:
                            logger.warning(f"Invalid password attempt for Admins: {email}")
                            return error_response(
                                'Invalid password. Please check your password and try again.', 
                                code=status.HTTP_401_UNAUTHORIZED
                            )
                    except Exception as pwd_error:
                        logger.error(f"Password check error for Admins {email}: {pwd_error}")
                        return error_response(
                            'Authentication failed. Please try again.', 
                            code=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                
            except Admins.DoesNotExist:
                    logger.warning(f"Login attempt with non-existent Admins email: {email}")
                    return error_response(
                        'No Admins account found with this email. Please contact system Adminsistrator.', 
                        code=status.HTTP_404_NOT_FOUND
                    )
            except Exception as e:
                    logger.error(f"Unexpected error during Admins login: {e}")
                    return error_response(
                        'Login failed due to server error. Please try again later.', 
                        code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            

        except Exception as e:
            logger.error(f"Unexpected error in login API: {e}")
            return error_response(
                'An unexpected error occurred. Please try again later.', 
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class Admins_API(BaseCRUDViewSet):
    queryset = Admins.objects.all()
    serializer_class = Admins_serializer 
    
    # @swagger_auto_schema(
    #     methods=['post'],
    #     request_body=Admins_search_serializer,
    #     responses={200: Admins_login_serializer(many=True)}
    # )
    # @action(detail=False, methods=['post'], url_path='search')
    # def search(self, request, *args, **kwargs):
    #         try:
    #             search_term = request.data.get('search_term')
    #             if not search_term:
    #                     return Response({"message": "Please provide a search term"},
    #                                     status=status.HTTP_400_BAD_REQUEST)
    #             search_in = request.data.get('search_in').lower()
                
               
    #             search_results = Admins.objects.none()
    #             if search_in == 'email':
    #                     search_results = Admins.objects.filter(email=search_term)
                
    #             if not search_results.exists():
    #                 return error_response(
    #                 f"No Admins found matching '{search_term}' in {search_in}"
    #                 )
    #             serializer = Admins_serializer(search_results, many=True)

    #             return success_response("Search results", serializer.data)
    #         except Exception as e:
    #             return error_response(f"Error searching Admins: {e}")   
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if not data:
                return error_response('No data provided.', code=status.HTTP_400_BAD_REQUEST)

            # Check required fields
            for field in ['email', 'password']:
                if not data.get(field):
                    return error_response(f'Missing field: {field}', code=status.HTTP_400_BAD_REQUEST)

            # Check if Adminsname exists
            if Admins.objects.filter(email=data['email']).exists():
                return error_response('Admins already exists.', code=status.HTTP_409_CONFLICT)

            # Hash password
            data = data.copy()
            data['password'] = make_password(data['password'])

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return success_response(
                "Admins registered successfully",
                                    serializer.data,
                                    code=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating Admins: {e}")
            return error_response('Registration failed. Please try again later.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            