from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

from accounts.models import User
from django.core.mail import send_mail
from django.db.models.aggregates import Count
import datetime

@staff_member_required
def user_dashboard(request):
    return render(request, 'user_analytics.html', context={})


@staff_member_required
def user_dashboard_api(request):
    user_data = User.objects.extra({'created': "date(created)"}).values(
        'created').annotate(date_added_count=Count('id'))

       # Create an empty list to contain the days the ads has been running
    days = []
    data_set = []

        # Loop through the Views list
    for item in user_data:
            # Append each view item to the data set list
        data_set.append(item['date_added_count'])

            # Append each days the ads has being running
        days.append(datetime.datetime.strptime(
                item['created'], '%Y-%m-%d').strftime('%a'))
    return JsonResponse({"data_set": data_set, "days": days})


@staff_member_required
def list_all_users(request):
    users = User.objects.all()
    return render(request, "index.html", context={"users": users})


@staff_member_required
def send_user_email(request):
    user_id = request.POST.get('user_id')
    message = request.POST.get('valName')
    user_obj = User.objects.get(id=user_id)
    send_mail("Action mail from admin", message,
              "admin@silentcode.co", [user_obj.email])
    return JsonResponse({"detail": f"Email successfully sent to {user_obj.email}"})


@staff_member_required
def change_user_status(request, slug):
    user_obj = User.objects.get(id=slug)
    user_obj.status = "active" if user_obj.status == "inactive" else "inactive"
    user_obj.save()
    print(user_obj.status)
    return JsonResponse({"detail": "User status has been changed"})
