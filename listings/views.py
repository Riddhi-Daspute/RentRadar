from bson import ObjectId
from django.shortcuts import render,redirect
from django.contrib import messages

from .validators import (
    validate_phone,
    validate_pincode,
    validate_rent
)

from .db import properties_collection

def edit_property(request, property_id):

    if request.method == "POST":

        title = request.POST.get("title")
        owner = request.POST.get("owner")
        phone = request.POST.get("phone")
        area = request.POST.get("area")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        rent = request.POST.get("rent")
        amenities = request.POST.get("amenities")

        properties_collection.update_one(
            {"_id": ObjectId(property_id)},
            {
                "$set": {
                    "title": title,
                    "owner": owner,
                    "phone": phone,
                    "area": area,
                    "city": city,
                    "pincode": pincode,
                    "rent": int(rent),
                    "amenities": amenities
                }
            }
            )

        return redirect("home")

    property = properties_collection.find_one(
        {
            "_id": ObjectId(property_id)
        }
    )

    return render(
    request, "edit_property.html",
    {
        "property": property
    }
    )

def delete_property(request, property_id):

    properties_collection.delete_one(
        {
            "_id": ObjectId(property_id)
        }
    )

    messages.success(request, "Property deleted successfully!")

    return redirect("home")


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

        # Phone Validation
        if not validate_phone(phone):
            messages.error(request, "Invalid phone number! Phone number must contain exactly 10 digits.")
            return render(request, "home.html")

        # Pincode Validation
        if not validate_pincode(pincode):
            messages.error(request, "Invalid pincode! Pincode must contain exactly 6 digits.")
            return render(request, "home.html")

        # Rent Validation
        if not validate_rent(rent):
            messages.error(request, "Invalid rent! Rent must be a positive number.")
            return render(request, "home.html")
        
        property_data = {
            "title": title,
            "owner": owner,
            "phone": phone,
            "area": area,
            "city": city,
            "pincode": pincode,
            "rent": int(rent),
            "amenities": amenities
        }

        properties_collection.insert_one(property_data)

        print("Property Title :", title)
        print("Owner :", owner)
        print("Phone :", phone)
        print("Area :", area)
        print("City :", city)
        print("Pincode :", pincode)
        print("Rent :", rent)
        print("Amenities :", amenities)

        messages.success(request, "Property details received successfully!")

    properties = list(properties_collection.find())

    for property in properties:
        property["id"] = str(property["_id"])  

    return render(request, 'home.html',
    {
        "properties": properties
    })