from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, ContentItem, Category
from .Serializers import UserSerializer, ContentItemSerializer, CategorySerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView


class UserRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            return Response({'message': 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ContentContentItemViewSet(viewsets.ModelViewSet):
    serializer_class = ContentItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ContentItem.objects.all()
        return ContentItem.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContentSearchAPIView(APIView):
    queryset = ContentItem.objects.all()
    serializer_class = ContentItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body', 'summary', 'categories']

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import status


class GetOrCreateTokenView(APIView):
    """
    View to get or create a token for the user.
    """

    def post(self, request):
        """
        Get or create a token for the user.
        """
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try to authenticate the user
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Create token if user exists and password matches
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        """
        Get the current user's token if authenticated.
        """
        if request.user.is_authenticated:
            token, created = Token.objects.get_or_create(user=request.user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAdminUser]
#
#     def create(self, request, *args, **kwargs):
#         print('okkk')
#         # Custom user creation logic (for registering authors)
#         pass
#
#
# class ContentItemViewSet(viewsets.ModelViewSet):
#     queryset = ContentItem.objects.all()
#     serializer_class = ContentItemSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#     def get_queryset(self):
#         if self.request.user.is_staff:
#             return ContentItem.objects.all()
#         return ContentItem.objects.filter(author=self.request.user)
#
#     @action(detail=True, methods=['get'])
#     def search_content(self, request, pk=None):
#         term = request.query_params.get('term', '')
#         queryset = ContentItem.objects.filter(
#             title__icontains=term
#         ) | ContentItem.objects.filter(
#             body__icontains=term
#         ) | ContentItem.objects.filter(
#             summary__icontains=term
#         )
#         serializer = ContentItemSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#     def list(self, request, *args, **kwargs):
#         # Custom user creation logic (for registering authors)
#         return super().list(request, *args, **kwargs)
#
#
# from django_seed import Seed
# from .models import ContentItem
#
# def seed_content():
#     seeder = Seed.seeder()
#     seeder.add_entity(ContentItem, 10)  # Create 10 ContentItem instances
#     seeder.execute()