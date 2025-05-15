from django.urls import path
from .views import RFIDAccessView, access_form, dashboard, active_workers_api  # Importe a view access_form

urlpatterns = [
    path('api/access/', RFIDAccessView.as_view(), name='rfid-access'),
    path('access-form/', access_form, name='access-form'),  # Rota do template
    path('dashboard/', dashboard, name='dashboard'),
    path('api/active-workers/', active_workers_api, name='active-workers-api'),
]