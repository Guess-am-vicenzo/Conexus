from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Club, Member,Announcement
from .forms import ClubForm, MemberForm
from django.contrib.auth.models import User
from .forms import SimpleUserEditForm
from .forms import AnnouncementForm
from .forms import UserForm



def index(request):
    return render(request, 'index.html')


def club_list(request):
    clubs = Club.objects.filter(is_approved=True)
    return render(request, 'club_list.html', {'clubs': clubs})


def club_detail(request, pk):
    club = get_object_or_404(Club, pk=pk, is_approved=True)
    announcements = club.announcements.all()  # Fetch all announcements for this club
    query = request.GET.get('q', '').strip()

    members = club.member_set.all()

    if query:
        terms = query.split()
        search_q = Q()
        for term in terms:
            search_q |= Q(first_name__icontains=term) | Q(last_name__icontains=term)
        members = members.filter(search_q)

    context = {
        'club': club,
        'members': members,
        'query': query,
        'announcements': announcements,
    }
    return render(request, 'club_detail.html', context)

def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'member_detail.html', {'member': member})



def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            # Save the club with a waiting approval status
            form.save()

            # Add a success message
            messages.success(request, "Club created! Waiting for admin approval.")

            # Redirect to club list (or any other page you prefer)
            return redirect('club_list')  
    else:
        form = ClubForm()  # Create an empty form for the GET request

    return render(request, 'create_club.html', {'form': form})


def create_member(request, pk):
    club = get_object_or_404(Club, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            if Member.objects.filter(email=email, club=club).exists():
                messages.error(request, "This email is already registered for this club.")
                return render(request, 'create_member.html', {'form': form, 'club': club})

            member = form.save(commit=False)
            member.club = club
            member.save()
            messages.success(request, "Member successfully created!")
            return redirect('club_detail', pk=club.pk)
    else:
        form = MemberForm()

    return render(request, 'create_member.html', {'form': form, 'club': club})

def signup(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            # Create the User object first (User is linked to Member)
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # You can use email or any field you prefer
             
            )
            
            # Create Member instance and associate with the user
            member = form.save(commit=False)
            member.user = user
            member.save()  # Save the Member instance

            # Log the user in after registration
            login(request, user)
            messages.success(request, "Successfully signed up and logged in!")
            return redirect('club_list')  # Redirect after successful signup

        else:
            messages.error(request, "Signup failed. Please fix the errors below.")
    else:
        form = MemberForm()

    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('club_list')
        else:
            messages.error(request, "Something happened!.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')


def details(request, id):
    mymember = get_object_or_404(Member, id=id)
    return render(request, 'details.html', {'mymember': mymember})


@login_required
def create_announcement(request, pk):
    club = get_object_or_404(Club, pk=pk)

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.club = club
            announcement.save()
            # Redirect to the club detail page after saving the announcement
            return redirect('club_detail', pk=club.pk)
    else:
        form = AnnouncementForm()

    return render(request, 'create_announcement.html', {'form': form, 'club': club})
#
@login_required
def admin_dashboard(request):
    # Check if the user is an admin
    if not request.user.is_superuser:
        # If not an admin, redirect to homepage or some other page
        return redirect('/')  # or redirect('another_page')
    
    # Assuming we need some data for the dashboard, you can pass it like this
    total_users = User.objects.count()
    total_clubs = Club.objects.count()  # replace with your actual model
    total_announcements = Announcement.objects.count()  # replace with your actual model

    new_user_name = ""  # You can query this dynamically based on the latest user
    new_club_name = ""  # Same here, query the latest created club
    new_announcement_title = ""  # and announcements

    context = {
        'total_users': total_users,
        'total_clubs': total_clubs,
        'total_announcements': total_announcements,
        'new_user_name': new_user_name,
        'new_club_name': new_club_name,
        'new_announcement_title': new_announcement_title,
    }

    return render(request, 'admin_dashboard.html', context)

def user_management(request):
    users = User.objects.all()  # Get all users from the database
    return render(request, 'user_management.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = SimpleUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')  # Redirect to the user management page
    else:
        form = SimpleUserEditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_management')




# Create User view
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = UserForm()

    return render(request, 'create_user.html', {'form': form, 'page_title': 'Create User', 'button_text': 'Create'})

def club_management(request):
    # Fetch the necessary data (clubs, categories, etc.)
    clubs = Club.objects.all()  # If you have a Club model
    return render(request, 'club_management.html', {'clubs': clubs})

def announcement_management(request):
    announcements = Announcement.objects.all()  # Fetch all announcements
    return render(request, 'announcement_management.html', {'announcements': announcements})

@login_required
def edit_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)

    if request.method == 'POST':
        if 'save' in request.POST:
            form = AnnouncementForm(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                messages.success(request, "Announcement updated successfully!")
                return redirect('club_detail', pk=announcement.club.pk)
        elif 'delete' in request.POST:
            club_pk = announcement.club.pk  # Save it before deletion
            announcement.delete()
            messages.success(request, "Announcement deleted successfully!")
            return redirect('club_detail', pk=club_pk)
    else:
        form = AnnouncementForm(instance=announcement)

    return render(request, 'edit_announcement.html', {'form': form, 'announcement': announcement})