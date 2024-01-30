from django.urls import path
from .views import SignUpView, UserListView, UserDetailView, LogoutView, PatientView, PatientDetailView
urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user', UserListView.as_view()),
    path('user/<uuid:id>/', UserDetailView.as_view()),
    path('patient', PatientView.as_view()),
    path('patient/<uuid:id>/', PatientDetailView.as_view()),
]