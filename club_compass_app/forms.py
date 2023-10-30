from django import forms


class When2MeetForm(forms.Form):
    event_name = forms.CharField(label="Enter the title of your event", max_length=50,
                                 widget=forms.TextInput(attrs={"placeholder": "Enter your event name here",
                                                               "class": "form-control"}))

    # dates = forms.DateField(label="Meeting Date(s)", widget=forms.DateInput())

    dates = forms.DateField(label="Enter the date of your event",
                           widget=forms.DateInput(attrs={"class": "form-control",
                                                         "placeholder": "Enter the date of your event"}))


class MessageForm(forms.Form):
    message_text = forms.CharField(label="Enter Message", max_length=1000,
                                   widget=forms.Textarea(attrs={"class": "form-control",
                                                                "placeholder": "Enter message to send to all club "
                                                                               "members"}))


class ClubForm(forms.Form):
    club_name = forms.CharField(label="Enter your club's name", max_length=50,
                                widget=forms.TextInput(attrs={"placeholder": "Enter your club name here",
                                                              "class": "form-control"}))

    description = forms.CharField(label='Enter a little description about your club here', max_length=2000,
                                  widget=forms.Textarea(attrs={"class": "form-control",
                                                               "placeholder": "Enter a description about your club"}))

    public = forms.BooleanField(label="Make your club public?",
                                widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), required=False)


class EventForm(forms.Form):
    HOURS = [(f'{i:02d}', f'{i:02d}') for i in range(1, 13)]
    MINUTES = [(f'{i:02d}', f'{i:02d}') for i in range(0, 60)]
    DAY_NIGHT = [("AM", "AM"), ("PM", "PM")]

    event_name = forms.CharField(label="Enter the title of your event", max_length=50,
                                 widget=forms.TextInput(attrs={"placeholder": "Enter your event name here",
                                                               "class": "form-control"}))

    description = forms.CharField(label="Enter a description about your event", max_length=2000,
                                  widget=forms.Textarea(attrs={"class": "form-control",
                                                               "placeholder": "Enter a description about your event"}))

    date = forms.DateField(label="Enter the date of your event", 
                           widget=forms.DateInput(attrs={"class": "form-control",
                                                         "placeholder": "YYYY-MM-DD"}))
    
    location = forms.CharField(label="Enter the location of your event", max_length=100,
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Enter the location of your event"}))
    
    ## TIMES ##

    ## START TIME ##
    start_hour = forms.ChoiceField(label="Enter the start time of your event", choices=HOURS,
                                   widget=forms.Select(attrs={"class": "form-control"}, choices=HOURS))
    
    start_minute = forms.ChoiceField(label="Enter the start time of your event", choices=MINUTES,
                                   widget=forms.Select(attrs={"class": "form-control"}, choices=MINUTES))
    
    start_day_night = forms.ChoiceField(label="AM or PM?", choices=DAY_NIGHT,
                                    widget=forms.Select(attrs={"class": "form-control"}, choices=DAY_NIGHT))
    
    ## END TIME ##
    end_hour = forms.ChoiceField(label="Enter the end time of your event", choices=HOURS,
                                   widget=forms.Select(attrs={"class": "form-control"}, choices=HOURS))
    
    end_minute = forms.ChoiceField(label="Enter the start hour of your event", choices=MINUTES,
                                   widget=forms.Select(attrs={"class": "form-control"}, choices=MINUTES))
    
    end_day_night = forms.ChoiceField(label="AM or PM?", choices=DAY_NIGHT,
                                    widget=forms.Select(attrs={"class": "form-control"}, choices=DAY_NIGHT))
