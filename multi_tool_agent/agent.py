from google.adk.agents import Agent
import requests
import json


def get_satellite_coordinates(sat: str) -> dict:
    """Retrieves the current coordinates of the satellite.

    Returns:
        dict: A dictionary containing the current position information with a 'status' key ('success' or 'error') and a 'position' key with the coordinates details if successful, or an 'error_message' if an error occurred.
    """
    response = requests.get("http://api.open-notify.org/iss-now.json")

    obj = response.json()

    if sat.lower() == "iss":
        return {"status": "success",
                "position": f"[{obj['iss_position']['latitude']}, {obj['iss_position']['longitude']}]"}
    else:
        return {"status": "error",
                "error_message": f"The position of '{sat}' is not available."}

def get_location(lat:str, long:str) -> dict:
    """Returns the country where this coordinates belong to is.

    Returns:
        dict: A dictionary containing the country_code if the place for the specified latitude and longitude with 'status' key ('success' or 'error') and a 'country_code' key with the country code of the place if successful, or an 'error_message' if an error occurred.
    """
    import datetime
    from zoneinfo import ZoneInfo

    if lat == None or long == None :
        return {"status": "error",
                "error_message": f"Sorry, I don't have country code information for {lat} and {long}."}

    # tz = ZoneInfo(tz_identifier)
    # now = datetime.datetime.now(tz)

    response = requests.get(f"https://api.wheretheiss.at/v1/coordinates/{lat},{long}")
    obj = response.json()

    print(obj)

    return {"status": "success",
            "country_code": f"{obj['country_code']}"}

root_agent = Agent(
    name="satellite_location_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions about current coordinate of the satellite",
    instruction="I can answer your questions about the satellite position and country.",
    tools=[get_satellite_coordinates, get_location]
)