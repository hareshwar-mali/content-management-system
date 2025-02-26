from os.path import basename
from tkinter.font import names

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ContentContentItemViewSet, UserRegistrationAPIView, LoginAPIView, \
    ContentSearchAPIView
from .views import GetOrCreateTokenView

# from .views import UserViewSet, ContentItemViewSet, CategoryViewSet
#
# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'content', ContentItemViewSet)
# router.register(r'categories', CategoryViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
router = DefaultRouter()
router.register(r'contents', ContentContentItemViewSet, basename='contents')

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('search/', ContentSearchAPIView.as_view(), name='content_search'),
    path('get-or-create-token/', GetOrCreateTokenView.as_view(), name='get_or_create_token'),
    path('', include(router.urls)),
]
