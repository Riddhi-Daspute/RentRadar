import re

def validate_phone(phone):
    pattern = r"^\d{10}$"
    if re.match(pattern, phone):
        return True
    
    return False

def validate_pincode(pincode):

    pattern = r"^\d{6}$"

    if re.match(pattern, pincode):
        return True

    return False

def validate_rent(rent):

    pattern = r"^\d+$"

    if re.match(pattern, rent):

        if int(rent) > 0:
            return True

    return False