from datetime import datetime
from bson import ObjectId
from django.shortcuts import render,redirect
from django.contrib import messages

from .validators import (
    validate_phone,
    validate_pincode,
    validate_rent
)

from .db import properties_collection
from .classes import Property,PriceAnalyzer

from .serializers import PropertySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

        existing_property = properties_collection.find_one(
        {
            "_id": ObjectId(property_id)
        }
        )

        price_history = existing_property.get("price_history", [])

        new_rent = int(rent)
        old_rent = existing_property["rent"]

        if new_rent != old_rent:
            price_history.append(
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "rent": new_rent
                }
            )

        property = Property(
            title=title,
            owner=owner,
            phone=phone,
            area=area,
            city=city,
            pincode=pincode,
            rent=int(rent),
            amenities=amenities,
            price_history=price_history
        )

        properties_collection.update_one(
            {"_id": ObjectId(property_id)},
            {
                "$set": property.to_dict()
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

    query = {}

    area = request.GET.get("area")
    city = request.GET.get("city")
    rent = request.GET.get("rent")

    if area:
        query["area"] = area

    if city:
        query["city"] = city

    if rent:
        query["rent"] = {"$lte": int(rent)}

    documents = list(properties_collection.find(query))

    properties = []

    for document in documents:

        property = Property(
            title=document["title"],
            owner=document["owner"],
            phone=document["phone"],
            area=document["area"],
            city=document["city"],
            pincode=document["pincode"],
            rent=document["rent"],
            amenities=document["amenities"],
            property_id=str(document["_id"]),
            price_history=document.get("price_history", [])
        )

        properties.append(property)

    analyzer = PriceAnalyzer(properties)

    average_rents = analyzer.average_rent_by_area()

    context = {
        "properties": properties,
        "average_rents": average_rents
    }

    return render(request, "home.html", context)

def owner_dashboard(request):
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
        
        property = Property(
            title=title,
            owner=owner,
            phone=phone,
            area=area,
            city=city,
            pincode=pincode,
            rent=int(rent),
            amenities=amenities,
            price_history=[
                {
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "rent": int(rent)
                }
            ]
        )

        properties_collection.insert_one(property.to_dict())

        print("Property Title :", title)
        print("Owner :", owner)
        print("Phone :", phone)
        print("Area :", area)
        print("City :", city)
        print("Pincode :", pincode)
        print("Rent :", rent)
        print("Amenities :", amenities)

        messages.success(request, "Property details received successfully!")

    documents = list(properties_collection.find())

    properties = []

    for document in documents:

        property = Property(
            title=document["title"],
            owner=document["owner"],
            phone=document["phone"],
            area=document["area"],
            city=document["city"],
            pincode=document["pincode"],
            rent=document["rent"],
            amenities=document["amenities"],
            property_id=str(document["_id"]),
            price_history=document.get("price_history", [])
        )

        properties.append(property) 

    return render(request, 'owner_dashboard.html',
    {
        "properties": properties
    })

def average_rent_report(request):

    pipeline = [
        {
            "$group": {
                "_id": "$area",
                "average_rent": {
                    "$avg": "$rent"
                }
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]

    report = list(properties_collection.aggregate(pipeline))

    for item in report:
        item["area"] = item.pop("_id")

    chart_labels = []
    chart_values = []

    for item in report:

        chart_labels.append(item["area"])
        chart_values.append(item["average_rent"])

    return render(
    request,
    "reports.html",
    {
        "report": report,
        "chart_labels": chart_labels,
        "chart_values": chart_values
    }
)

@api_view(["GET"])
def property_api(request):

    documents = list(properties_collection.find())

    properties = []

    for document in documents:

        property = Property(
            title=document["title"],
            owner=document["owner"],
            phone=document["phone"],
            area=document["area"],
            city=document["city"],
            pincode=document["pincode"],
            rent=document["rent"],
            amenities=document["amenities"],
            property_id=str(document["_id"]),
            price_history=document.get("price_history", [])
        )

        properties.append(property)

    serializer = PropertySerializer(properties, many=True)

    return Response(serializer.data)