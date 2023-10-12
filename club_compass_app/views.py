from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import generic
from .models import Club, Membership

# Create your views here.

def index(request):
    # https://stackoverflow.com/questions/11916297/django-detect-admin-login-in-view-or-template 
    is_superuser = request.user.is_superuser  # Check if the user is a superuser
    
    # https://stackoverflow.com/questions/4789021/in-django-how-do-i-check-if-a-user-is-in-a-certain-group#:~:text=You%20can%20access%20the%20groups%20simply%20through%20the%20groups%20attribute%20on%20User%20.&text=then%20user.,%5D%20.
    # user_roles = [group.name for group in request.user.groups.all()]  # Get all the roles/groups the user is in
    if request.user.groups.filter(name='admin').exists():
        role = 'admin'
    else:
        role = 'user'
        
    if request.user.is_authenticated:
        # If the user is authenticated, redirect them to the home page
        return redirect('/home/')
        
    return render(request, 'club_compass_app/accountTypeSelectionScreen.html', {'is_superuser': is_superuser, 'role': role})


def logout_view(request):
    # Calls a built in method to log the user out and returns to the home screen
    if request.method == "POST":
        logout(request)
        return redirect("/")
    

class Home(generic.ListView):
    template_name = 'club_compass_app/home.html'
    context_object_name = 'clubs'
    
    def get_queryset(self):
        return Club.objects.filter(membership__user=self.request.user)
    

class ClubDetail(generic.DetailView):
    model = Club
    template_name = 'club_compass_app/club_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memberships'] = Membership.objects.filter(club=self.object)
        return context


