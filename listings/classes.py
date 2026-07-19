from asyncio import threads
import statistics
import threading

from pymongo import results

class Property:

    def __init__(
        self,
        title,
        owner,
        phone,
        area,
        city,
        pincode,
        rent,
        amenities,
        property_id=None,
        price_history=None
    ):

        self.id = property_id
        self.property_id = property_id
        self.title = title
        self.owner = owner
        self.phone = phone
        self.area = area
        self.city = city
        self.pincode = pincode
        self.rent = rent
        self.amenities = amenities

        if price_history is None:
            self.price_history = []
        else:
            self.price_history = price_history

    def to_dict(self):

        return {
            "title": self.title,
            "owner": self.owner,
            "phone": self.phone,
            "area": self.area,
            "city": self.city,
            "pincode": self.pincode,
            "rent": self.rent,
            "amenities": self.amenities,
            "price_history": self.price_history
        }
    
class PriceAnalyzer:

    def __init__(self, properties):
        self.properties = properties

    def average_rent_by_area(self):

        area_rents = {}

        for property in self.properties:

            area = property.area
            rent = int(property.rent)

            if area not in area_rents:
                area_rents[area] = []

            area_rents[area].append(rent)

        average_rents = {}

        for area, rents in area_rents.items():
            average_rents[area] = round(statistics.mean(rents), 2)

        return average_rents
    
    def area_wise_price_trend(self):

        trend_report = {}

        for property in self.properties:

            history = property.price_history

            if len(history) < 2:
                trend = "Not enough data"

            else:
                first_rent = history[0]["rent"]
                last_rent = history[-1]["rent"]

                if last_rent > first_rent:
                    trend = "Increasing"

                elif last_rent < first_rent:
                    trend = "Decreasing"

                else:
                    trend = "Stable"

            if property.area not in trend_report:
                trend_report[property.area] = []

            trend_report[property.area].append(trend)

        return trend_report
    
    def calculate_price_trend(self):

        results = {}

        def process_property(property):

            if property.price_history:
                latest_rent = property.price_history[-1]["rent"]
            else:
                latest_rent = property.rent

            results[property.property_id] = latest_rent

        threads = []

        for property in self.properties:

            thread = threading.Thread(
                target=process_property,
                args=(property,)
            )

        threads.append(thread)
        thread.start()

        for thread in threads:
            thread.join()

        return results
    
class Tenant:

    def __init__(
        self,
        preferred_city=None,
        preferred_area=None,
        max_rent=None,
        amenities=None
    ):

        self.preferred_city = preferred_city
        self.preferred_area = preferred_area
        self.max_rent = max_rent

        if amenities is None:
            self.amenities = []
        else:
            self.amenities = amenities