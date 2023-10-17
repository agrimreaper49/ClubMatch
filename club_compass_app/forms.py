from django import forms

class ClubForm(forms.Form):
    club_name = forms.CharField(label="Enter your club's name", max_length=50, 
                                    widget = forms.TextInput(attrs={"placeholder": "Enter your club name here",
                                                                    "class": "form-control"}))
    
    description = forms.CharField(label='Enter a little description about your club here', max_length=2000,
                               widget = forms.Textarea(attrs={"class": "form-control",
                                                                "placeholder": "Enter a description about your club"}))


class EventForm(forms.Form):
    event_name = forms.CharField(label="Enter the title of your event", max_length=50,
                                 widget=forms.TextInput(attrs={"placeholder": "Enter your event name here",
                                                              "class": "form-control"}))
    
    description = forms.CharField(label="Enter a description about your event", max_length=2000,
                                    widget=forms.Textarea(attrs={"class": "form-control",
                                                                 "placeholder": "Enter a description about your event"}))
    
    date = forms.DateField(label="Enter the date of your event", 
                           widget=forms.DateInput(attrs={"class": "form-control",
                                                        "placeholder": "Enter the date of your event"}))
    
    start_time = forms.TimeField(label="Enter the start time of your event", 
                                 widget=forms.TimeInput(attrs={"class": "form-control",
                                                            "placeholder": "Enter the start time of your event"}))
    
    end_time = forms.TimeField(label="Enter the end time of your event", 
                               widget=forms.TimeInput(attrs={"class": "form-control",
                                                            "placeholder": "Enter the end time of your event"}))
    
    location = forms.CharField(label="Enter the location of your event", max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "Enter the location of your event"}))
    
    