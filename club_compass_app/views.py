from typing import Any
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import generic
from .models import Club, Membership
from .forms import ClubForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin

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
        if self.request.user.is_authenticated and len(Club.objects.filter(Q(owner=self.request.user))) == 0:
            # Checks to see if the user already made a club or not
            club_name = form.cleaned_data['club_name']
            description = form.cleaned_data['description']
            owner = self.request.user
            club = Club(name=club_name, description=description, owner=owner)
            club.save()
            return super().form_valid(form)
        else:
            return redirect("/")
        
    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/")    
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return True
        else:
            return len(Club.objects.filter(owner=self.request.user)) == 0 \
            and len(Membership.objects.filter(user=self.request.user)) == 0
        

def logout_view(request):
    # Calls a built in method to log the user out and returns to the home screen
    if request.method == "POST":
        logout(request)
        return redirect("/")
    

class Home(UserPassesTestMixin, generic.ListView):
    template_name = 'club_compass_app/home.html'
    context_object_name = 'clubs'
    
    def get_queryset(self):
        return Club.objects.filter(membership__user=self.request.user)
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.request.user.is_authenticated:
            return redirect(f"/clubs/{Club.objects.filter(Q(owner=self.request.user))[0].slug}")
        else:
            return redirect("/")
    
    def test_func(self):
        return self.request.user.is_authenticated and \
            len(Club.objects.filter(Q(owner=self.request.user))) == 0
    

class ClubDetail(UserPassesTestMixin, generic.DetailView):
    login_url = "/"
    model = Club
    template_name = 'club_compass_app/club_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberships'] = Membership.objects.filter(club=self.object).filter(~Q(role='pending'))
        context['pending_members'] = Membership.objects.filter(club=self.object).filter(role='pending')
        return context
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect("/clubs/")
    
    def test_func(self) -> bool | None:
        return self.request.user == self.get_object().owner
    
class Discover(UserPassesTestMixin, generic.ListView):
    template_name = 'club_compass_app/discover.html'
    context_object_name = 'clubs'
    
    def get_queryset(self) -> QuerySet[Any]:
        return Club.objects.filter(~Q(membership__user=self.request.user))
    
    def handle_no_permission(self) -> HttpResponseRedirect:
        if self.request.user.is_authenticated:
            return redirect(f"/clubs/{Club.objects.filter(Q(owner=self.request.user))[0].slug}")
        else:
            return redirect("/")
    
    def test_func(self):
        return self.request.user.is_authenticated and \
            len(Club.objects.filter(Q(owner=self.request.user))) == 0
    
@login_required
def join_club(request, slug):
    club = Club.objects.filter(Q(slug=slug))[0]
    Membership(user=request.user, club=club).save()
    return redirect("/home/")

@login_required
def approve_member(request, slug, pk):
    membership = Membership.objects.get(pk=pk)
    membership.approve()
    membership.save()
    return redirect(f"/clubs/{slug}")

