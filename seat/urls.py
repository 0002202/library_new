from django.urls import path
from seat.views import seat_info, seat_lock, seat_status_update, seat_cancel, seat_save
from user.views import leave
urlpatterns = [
    path('info/', seat_info),
    path('lock/', seat_lock),
    path('status_update/', seat_status_update),
    path('seat_cancel/', seat_cancel),
    path('seat_save/', seat_save),
    path('leave/', leave),
]