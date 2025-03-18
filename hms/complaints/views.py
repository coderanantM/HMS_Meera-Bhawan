from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import pytz
from .models import Complaint
import json

def complaint_form_student(request):
    if request.method == 'POST':
        # Process form data
        bhavan = request.POST.get('bhavan')
        room = request.POST.get('room')
        contact_no = request.POST.get('contactNo')
        complaint_group = request.POST.get('complaintGroup')
        area = request.POST.get('area', '')
        requirement = request.POST.get('requirement')
        category = request.POST.get('category', '')
        preferred_time = request.POST.get('preferredTime', '')
        comments = request.POST.get('comments', '')

        # Get current time in UTC and convert to IST
        utc_now = timezone.now()
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

        # Save the complaint to the database
        Complaint.objects.create(
            bhavan=bhavan,
            room=room,
            contact_no=contact_no,
            complaint_group=complaint_group,
            area=area,
            requirement=requirement,
            category=category,
            preferred_time=preferred_time,
            comments=comments,
            user=request.user,  # Store the logged-in user who submitted the complaint
            ist=ist_now  # Set the IST field
        )

        # Use messages framework to display a success message
        messages.success(request, 'Your complaint has been submitted successfully!')

        # Redirect to the student dashboard
        return redirect('student_dashboard')  # This should be a URL name for the student dashboard

    # If the request is GET, render the form
    context = {
        'requirement_options': ["electrical", "Mason", "Carpentry", "Painter", "Sweeper", "Worker"],
        'time_options': [
            {"value": "2-3", "label": "2-3 pm"},
            {"value": "3-4", "label": "3-4 pm"},
            {"value": "4-5", "label": "4-5 pm"}
        ],
        'category_options': []  # Dynamically set based on the requirement
    }

    return render(request, 'complaints/Page8.html', context)

def complaint_form_warden(request):
    if request.method == 'POST':
        # Process form data
        bhavan = request.POST.get('bhavan')
        room = request.POST.get('room')
        contact_no = request.POST.get('contactNo')
        complaint_group = request.POST.get('complaintGroup')
        area = request.POST.get('area', '')
        requirement = request.POST.get('requirement')
        category = request.POST.get('category', '')
        preferred_time = request.POST.get('preferredTime', '')
        comments = request.POST.get('comments', '')

        # Get current time in UTC and convert to IST
        utc_now = timezone.now()
        ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

        # Save the complaint to the database
        Complaint.objects.create(
            bhavan=bhavan,
            room=room,
            contact_no=contact_no,
            complaint_group=complaint_group,
            area=area,
            requirement=requirement,
            category=category,
            preferred_time=preferred_time,
            comments=comments,
            user=request.user,  # Store the logged-in user who submitted the complaint
            ist=ist_now  # Set the IST field
        )

        # Use messages framework to display a success message
        messages.success(request, 'Your complaint has been submitted successfully!')

        # Redirect to the warden dashboard
        return redirect('warden_dashboard')  # This should be a URL name for the warden dashboard

    # If the request is GET, render the form
    context = {
        'requirement_options': ["electrical", "Mason", "Carpentry", "Painter", "Sweeper", "Worker"],
        'time_options': [
            {"value": "2-3", "label": "2-3 pm"},
            {"value": "3-4", "label": "3-4 pm"},
            {"value": "4-5", "label": "4-5 pm"}
        ],
        'category_options': []  # Dynamically set based on the requirement
    }

    return render(request, 'complaints/Page2.html', context)

def complaint_success(request):
    return render(request, 'complaints/complaint_success.html')

def team_info_warden(request):
    incharge = {
        'name': 'XYZ',
        'designation': 'Hostel Incharge',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    technical_manager = {
        'name': 'XYZ',
        'designation': 'Technical Manager',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    context = {
        'incharge': incharge,
        'technical_manager': technical_manager,
    }

    return render(request, 'complaints/Page5.html', context)

def team_info_student(request):
    incharge = {
        'name': 'XYZ',
        'designation': 'Hostel Incharge',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    technical_manager = {
        'name': 'XYZ',
        'designation': 'Technical Manager',
        'email': 'xyz@gmail.com',
        'phone': '7023714156',
    }

    context = {
        'incharge': incharge,
        'technical_manager': technical_manager,
    }

    return render(request, 'complaints/Page10.html', context)

@login_required
def complaints_view(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    context = {'complaints': complaints}
    return render(request, 'complaints/Page9.html', context)

@login_required
def fetch_student_complaints(request):
    complaints = Complaint.objects.filter(user__user_type='STUDENT').order_by('-created_at')
    complaints_data = [
        {
            'id': complaint.id,
            'IST': complaint.ist.strftime('%d %b %Y %H:%M:%S'),
            'name': complaint.user.get_full_name(),
            'bitsId': complaint.user.username,
            'contact_no': complaint.contact_no,
            'room': complaint.room,
            'area': complaint.area,
            'requirement': complaint.requirement,
            'category': complaint.category,
            'preferred_time': complaint.preferred_time,
            'description': complaint.comments,
            'status': complaint.status,
        }
        for complaint in complaints
    ]
    return JsonResponse(complaints_data, safe=False)

@login_required
def fetch_warden_complaints(request):
    complaints = Complaint.objects.filter(user__user_type__in=['WARDEN', 'SUPERINTENDENT']).order_by('-created_at')
    complaints_data = [
        {
            'id': complaint.id,
            'IST': complaint.ist.strftime('%d %b %Y %H:%M:%S'),
            'name': complaint.user.get_full_name(),
            'bitsId': complaint.user.username,
            'contact_no': complaint.contact_no,
            'room': complaint.room,
            'area': complaint.area,
            'requirement': complaint.requirement,
            'category': complaint.category,
            'preferred_time': complaint.preferred_time,
            'description': complaint.comments,
            'status': complaint.status,
        }
        for complaint in complaints
    ]
    return JsonResponse(complaints_data, safe=False)

@login_required
def update_complaint_status(request, id):
    if request.method == 'PUT':
        try:
            complaint = Complaint.objects.get(id=id)
            data = json.loads(request.body)
            status = data.get('status')
            complaint.status = status
            complaint.save()
            return JsonResponse({'success': True})
        except Complaint.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Complaint not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def previous_student_complaints(request):
    complaints = Complaint.objects.filter(user__user_type='STUDENT').order_by('-created_at')
    context = {'complaints': complaints}
    return render(request, 'complaints/Page6.html', context)

@login_required
def previous_warden_complaints(request):
    complaints = Complaint.objects.filter(user__user_type__in=['WARDEN', 'SUPERINTENDENT']).order_by('-created_at')
    context = {'complaints': complaints}
    return render(request, 'complaints/Page4.html', context)

def page3(request):
    return render(request, 'complaints/Page3.html')

def page2(request):
    return render(request, 'complaints/Page2.html')

def page6(request):
    return render(request, 'complaints/Page6.html')