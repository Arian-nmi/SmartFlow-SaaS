from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Service, Appointment
from .serializers import ServiceSerializer, AppointmentSerializer


class ServiceListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['price', 'duration']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'duration']

    def get_queryset(self):
        return Service.objects.filter(business__owner=self.request.user)


class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(business__owner=self.request.user)


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['date', 'status']
    search_fields = ['service__name']
    ordering_fields = ['date']

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)


class AppointmentStatusUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Appointment.objects.all()


class AppointmentCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk, user=request.user)
        except Appointment.DoesNotExist:
            return Response({"detail": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        if appointment.status == "cancelled":
            return Response({"detail": "This appointment is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        if appointment.date < timezone.now().date():
            return Response({"detail": "You cannot cancel a past appointment."}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = "cancelled"
        appointment.save()

        return Response({"detail": "Appointment cancelled successfully."}, status=status.HTTP_200_OK)
