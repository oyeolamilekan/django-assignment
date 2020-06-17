from django.urls import path
from .views import list_all_users, send_user_email, change_user_status, user_dashboard, user_dashboard_api

urlpatterns = [
    path("user_dashboard/", user_dashboard, name="user_dashboard"),
    path("user_dashboard_api/", user_dashboard_api, name="user_dashboard_api"),
    path("user_inline/", list_all_users, name="list_all_users"),
    path("send_user_email/", send_user_email, name="send_user_email"),
    path("user_status/<slug>/", change_user_status, name="change_user_status"),
]