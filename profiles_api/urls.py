from django.urls import path, include
from profiles_api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("hello-viewset", views.HelloViewSet, base_name="hello-viewset")
# We don't need to specify the basename given we have defined a query set
# so Django generate the names for us
router.register("profile", views.UserProfileViewSet)

urlpatterns = [
	path("hello-view/", views.HelloAPIView.as_view()),
	path("login/", views.UserLoginAPIView.as_view()),
	path("", include(router.urls)),
]