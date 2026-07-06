from django.shortcuts import render

# Create your views here.
def home(request):

    if request.method == "POST":
        print("Form Submitted!")
        
    return render(request, 'home.html')