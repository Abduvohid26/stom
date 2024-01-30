import uuid

from django.contrib.auth import logout
from django.shortcuts import render
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignUpSerializer, UserSerializer, PatientsSerializer, PaymentsSerializer
from rest_framework import generics, permissions, status
from users.models import User, Patients


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

class UserListView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
        )


# class PatientViewDetail(View):
#     lookup_field = 'id'
#     def get(self, request, id):
#         patient = Patients.objects.get(id=str(uuid.UUID(str(id))))
#         patient_serializer = PatientsSerializer(patient)
#         payment_serializer = PaymentsSerializer(patient.payments.all(), many=True)
#         response_data = {
#             'patient': patient_serializer.data,
#             'payments': payment_serializer.data,
#         }
#         return Response(data=response_data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         patient_serializer = PatientsSerializer(Patients, data=request.data)
#         if patient_serializer.is_valid():
#             patient_serializer.save()
#             return Response(data=patient_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def put(self, request, id):
#         patient = get_object_or_404(Patients, id=str(uuid.UUID(str(id))))
#         patient_serializer = PatientsSerializer(instance=patient, data=request.data)
#         if patient_serializer.is_valid():
#             patient_serializer.save()
#             return Response(data=patient_serializer.data, status=status.HTTP_200_OK)
#         return Response(data=patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def patch(self, request, id):
#         patient = get_object_or_404(Patients, id=str(uuid.UUID(str(id))))
#         patient_serializer = PatientsSerializer(instance=patient, data=request.data)
#         if patient_serializer.is_valid():
#             patient_serializer.save()
#             return Response(patient_serializer.data, status=status.HTTP_200_OK)
#         return Response(data=patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, id):
#         patient = get_object_or_404(Patients, id=str(uuid.UUID(str(id))))
#         patient.delete()
#         return Response(data={'message': 'Patient has been deleted!'}, status=status.HTTP_200_OK)
#

# class PatientView(APIView):
#     serializer_class = PatientsSerializer
#     queryset = Patients.objects.all()
#     permission_classes = [permissions.AllowAny]
#     lookup_field = 'id'
class PatientView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        patients = Patients.objects.all()
        serializer = PatientsSerializer(patients, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = PatientsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientsSerializer
    queryset = Patients.objects.all()
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        serializer = serializer_class(*args, **kwargs)
        patient = self.get_object()
        serializer.context['payments'] = patient.payments.all()
        return serializer