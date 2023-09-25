import requests
from datetime import datetime
import smtplib
import time

# email settings
MY_EMAIL = "etb901@gmail.com"
MY_PASSWORD = "frst pdxv ztyw wvuq"
THEIR_EMAIL = "elijah.t.busch@gmail.com"

# my long and lat
MY_LAT = 33.197247  # Your latitude
MY_LONG = -96.639786  # Your longitude


# If the ISS is close to my current position
def proximity_check():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # ISS long and lat
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print(f"iss lat: {iss_latitude}, long: {iss_longitude}")

    # Boundary check of coordinates
    if (iss_longitude - 5 <= MY_LONG <= iss_longitude + 5) and (iss_latitude - 5 <= MY_LAT <= iss_latitude + 5):
        return True
    else:
        return False


# and it is currently dark
def night_check():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    # Sunset sunrise times
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(f"sunrise: {sunrise}, sunset: {sunset}")

    hour_now = datetime.now().hour - 12

    if sunset <= hour_now <= sunrise:
        return True
    else:
        return False


# Then email me to tell me to look up.
def email_notification():
    with smtplib.SMTP("smtp.gmail.com") as gmail_connection:
        gmail_connection.starttls()
        gmail_connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        gmail_connection.sendmail(from_addr=MY_EMAIL, to_addrs=THEIR_EMAIL,
                                  msg="Subject: Look up!\n\nThe International Space Station should be visible, go look!"
                                  )


# # BONUS: run the code every 60 seconds.
# start_time = monotonic()
# while True:
#     iss_is_close = proximity_check(my_long=MY_LONG, my_lat=MY_LAT, iss_long=iss_longitude, iss_lat=iss_latitude)
#     is_night = night_check(time_hour=time_now.hour, time_sunset=sunset, time_sunrise=sunrise)
#
#     if iss_is_close and is_night:
#         email_notification()
#
#     sleep(60.0 - ((monotonic() - start_time) % 60.0))



while True:
    time.sleep(60)
    iss_is_close = proximity_check()
    is_night = night_check()
    if iss_is_close and is_night:
        email_notification()
