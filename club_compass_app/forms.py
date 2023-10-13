from django import forms

class ClubForm(forms.Form):
    club_name = forms.CharField(label="Enter your club's name", max_length=50, 
                                    widget = forms.TextInput(attrs={"placeholder": "Enter your club name here",
                                                                    "class": "form-control"}))
    
    description = forms.CharField(label='Enter a little description about your club here', max_length=2000,
                               widget = forms.Textarea(attrs={"class": "form-control",
                                                                "placeholder": "Enter a description about your club"}))
    
    def submit_question(self):
        pass