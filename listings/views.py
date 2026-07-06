from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def home(request):

    if request.method == "POST":
        title = request.POST.get("title")
        owner = request.POST.get("owner")
        phone = request.POST.get("phone")
        area = request.POST.get("area")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        rent = request.POST.get("rent")
        amenities = request.POST.get("amenities")

        print("Property Title :", title)
        print("Owner :", owner)
        print("Phone :", phone)
        print("Area :", area)
        print("City :", city)
        print("Pincode :", pincode)
        print("Rent :", rent)
        print("Amenities :", amenities)

        messages.success(request, "Property details received successfully!")
        
    return render(request, 'home.html')