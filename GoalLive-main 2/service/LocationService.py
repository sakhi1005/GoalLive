import geocoder

def get_user_location():
    try:
        # Get user's current location based on IP
        g = geocoder.ip('me')

        # Check if geocoding was successful
        if g.latlng:
            latitude, longitude = g.latlng
            return latitude, longitude
        else:
            raise ValueError("Could not retrieve location data.")
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# Step 3: Use the function
latitude, longitude = get_user_location()
if latitude and longitude:
    print(f"User's Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Could not retrieve user's location.")