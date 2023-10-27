from typing import Any
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import generic
from .models import Club, Membership, Message, Event
from .forms import ClubForm, MessageForm, EventForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.conf import settings

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        # If the user is authenticated, redirect them to the home page
        return redirect('/home/')
    return render(request, 'club_compass_app/accountTypeSelectionScreen.html')


class AddEvent(UserPassesTestMixin, generic.FormView):
    template_name = "club_compass_app/add_event.html"
    context = {'key': settings.GOOGLE_MAPS_API_KEY}
    form_class = EventForm
    success_url = "/"
    
    def get_context_data(self, location_query = None, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['key'] = settings.GOOGLE_MAPS_API_KEY
        context['location_query'] = location_query if location_query is not None else "UVA" # Default value to set location over UVA
        return context
    
    def query_location(self, location_query):
        print("running")
        location_query = location_query.replace(" ", "+")
        self.get_context_data(location_query)
    
    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        print("event request")
        if self.request.user.is_authenticated \
                and Club.check_user_owns_club(self.request.user):
            
            event_name = form.cleaned_data['event_name']
            club = Club.get_club_by_owner(self.request.user)
            description_ = form.cleaned_data['description']
            date = form.cleaned_data['date']
            
            start_hour = form.cleaned_data['start_hour']
            start_minute = form.cleaned_data['start_minute']
            start_day_night = form.cleaned_data['start_day_night']
            start_time = self.get_24_hour_time(start_hour, start_minute, start_day_night)
            
            end_hour = form.cleaned_data['end_hour']
            end_minute = form.cleaned_data['end_minute']
            end_day_night = form.cleaned_data['end_day_night']
            end_time = self.get_24_hour_time(end_hour, end_minute, end_day_night)
            
            location = form.cleaned_data['location']
            print(f"send {event_name} to {club.get_name()}")
            club = Club.get_club_by_owner(self.request.user)
            event = Event(name=event_name, description=description_, club=club, start_time = start_time, 
              end_time=end_time, date=date, location=location)
            print(event.start_time)
            print(event.end_time)
            event.save()
            return super().form_valid(form)
        else:
            return redirect("/")
            
    def get_24_hour_time(self, hour, minute, am_pm):
        hour = int(hour)
        if am_pm == "AM" and hour == 12:
            hour -= 12
        elif am_pm == "PM" and hour != 12:
            hour += 12
        return f"{hour:02d}:{minute}:00"

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/")

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if Membership.is_user_account(self.request.user):
            return False

        if not Club.check_user_owns_club(self.request.user):
            return False

        return True

class SendMessage(UserPassesTestMixin, generic.FormView):
    template_name = "club_compass_app/send_message.html"
    form_class = MessageForm
    success_url = "/"

    def form_valid(self, form):
        print("message request")
        if self.request.user.is_authenticated \
                and Club.check_user_owns_club(self.request.user):
            message_text = form.cleaned_data['message_text']
            club = Club.get_club_by_owner(self.request.user)
            print(f"send {message_text} to {club.get_name()}")
            message = Message(text=message_text, club=club)
            message.save()
            club.messages.add(message)
            # print(club.messages.all())
            # club_name = form.cleaned_data['club_name']
            # description = form.cleaned_data['description']
            # owner = self.request.user
            # public = form.cleaned_data['public']
            # club = Club(name=club_name, description=description, owner=owner, public=public)
            # club.save()
            return super().form_valid(form)
        else:
            return redirect("/")

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/")

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False

        if Membership.is_user_account(self.request.user):
            return False

        if not Club.check_user_owns_club(self.request.user):
            return False

        return True


class Login(UserPassesTestMixin, generic.FormView):
    template_name = "club_compass_app/create_club.html"
    form_class = ClubForm
    success_url = "/home/"

    def form_valid(self, form):
        if self.request.user.is_authenticated \
                and Club.check_user_owns_club(self.request.user) == 0:

            club_name = form.cleaned_data['club_name']
            description = form.cleaned_data['description']
            owner = self.request.user
            public = form.cleaned_data['public']
            club = Club(name=club_name, description=description, owner=owner, public=public)
            club.save()
            # TODO add tags
            return super().form_valid(form)
        else:
            return redirect("/")

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/")

    def test_func(self):
        if not self.request.user.is_authenticated:
            return True
        else:
            return not Club.check_user_owns_club(self.request.user) \
                and not Membership.is_user_account(self.request.user)


def logout_view(request):
    # Calls a built in method to log the user out and returns to the home screen
    if request.method == "POST":
        logout(request)
        return redirect("/")


class Home(UserPassesTestMixin, generic.ListView):
    template_name = 'club_compass_app/home.html'
    context_object_name = 'clubs'

    def get_queryset(self):
        return Club.objects.filter(membership__user=self.request.user, membership__role='member')

    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.request.user.is_authenticated:
            return redirect(f"/clubs/{Club.get_club_by_owner(self.request.user).slug}")
        else:
            return redirect("/")

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        if Club.check_user_owns_club(self.request.user):
            return False
        
        return True


class UserClubDetail(UserPassesTestMixin, generic.DetailView):
    login_url = "/"
    model = Club
    template_name = "club_compass_app/user_club_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.object.get_name()
        context["description"] = self.object.get_desc()
        context["messages"] = self.object.get_messages()
        context['events'] = self.object.get_upcoming_events()
        context['key'] = settings.GOOGLE_MAPS_API_KEY
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/")

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        return self.request.user in self.get_object().get_members()


class ClubDetail(UserPassesTestMixin, generic.DetailView):
    login_url = "/"
    model = Club
    template_name = 'club_compass_app/club_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberships'] = self.object.get_members()
        context['pending_members'] = self.object.get_pending_members()
        context['rejected_members'] = self.object.get_rejected_members()
        context['club'] = self.get_object()
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/clubs/")

    # Checks if the user owns the club
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        if not self.get_object().check_user_owns_club(self.request.user):
            return False

        return True

class Discover(UserPassesTestMixin, generic.ListView):
    template_name = 'club_compass_app/discover.html'
    context_object_name = 'clubs'

    def get_queryset(self):  # shows the user clubs that they are not a member of
        return Club.get_public_clubs().filter(~Q(membership__user=self.request.user))

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # If they are logged in and they own a club, redirect them to their club
            return redirect(f"/clubs/{Club.get_club_by_owner(self.request.user).slug}")
        else:
            return redirect("/")  # If there not logged in redirect to the login page

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        
        if Club.check_user_owns_club(self.request.user):
            return False
        
        return True


@login_required
def join_club(request, slug):
    if not request.user.is_authenticated:
        return redirect("/")
    
    club = Club.objects.get(slug=slug)
    if club is None:
        return redirect("/")
    
    if club.public is False:
        return redirect("/")

    if Membership.objects.filter(user=request.user, club=club).exists():
        return redirect("/")
    
    Membership(user=request.user, club=club).save()
    return redirect("/home/")


@login_required
def approve_member(request, slug, user_pk):
    if request.user.is_authenticated \
            and Club.objects.get(slug=slug).check_user_owns_club(request.user):
        pending_user = User.objects.get(pk=user_pk)
        membership = Membership.objects.get(user=pending_user, club__slug=slug)
        membership.approve()
        membership.save()
        return redirect(f"/clubs/{slug}")
    
    else:
        return redirect("/")


@login_required
def reject_member(request, slug, user_pk):
    if request.user.is_authenticated \
            and Club.check_user_owns_club(request.user):
        pending_user = User.objects.get(pk=user_pk)
        membership = Membership.objects.get(user=pending_user, club__slug=slug)
        membership.reject()
        membership.save()
        return redirect(f"/clubs/{slug}")
    
    return redirect("/")



