from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import generic
from .models import Club, Membership
from .forms import ClubForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User


# Create your views here.

def login(request):
    if request.user.is_authenticated:
        # If the user is authenticated, redirect them to the home page
        return redirect('/home/')
    return render(request, 'club_compass_app/accountTypeSelectionScreen.html')


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
        return self.request.user.is_authenticated and \
            not Club.check_user_owns_club(self.request.user)


class UserClubDetail(UserPassesTestMixin, generic.DetailView):
    login_url = "/"
    model = Club
    template_name = "club_compass_app/user_club_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.object.get_name()
        context["description"] = self.object.get_desc()
        return context

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/")

    def test_func(self):
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
        return self.request.user == self.get_object().owner


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
        return self.request.user.is_authenticated and \
            not Club.check_user_owns_club(self.request.user)


@login_required
def join_club(request, slug):
    club = Club.objects.filter(Q(slug=slug))[0]
    Membership(user=request.user, club=club).save()
    return redirect("/home/")


@login_required
def approve_member(request, slug, user_pk):
    pending_user = User.objects.get(pk=user_pk)
    membership = Membership.objects.get(user=pending_user, club__slug=slug)
    membership.approve()
    membership.save()
    return redirect(f"/clubs/{slug}")


@login_required
def reject_member(request, slug, user_pk):
    pending_user = User.objects.get(pk=user_pk)
    membership = Membership.objects.get(user=pending_user, club__slug=slug)
    membership.reject()
    membership.save()
    return redirect(f"/clubs/{slug}")
