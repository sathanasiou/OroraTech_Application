import requests
from datetime import datetime
from geometry import *
from arcGISResponse import *
import os

BASE_URL = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/arcgis/rest/services/WFIGS_Incident_Locations/FeatureServer/0/query?where=1%3D1&outFields=ContainmentDateTime,ControlDateTime,IncidentSize,DiscoveryAcres,FinalAcres,FireCause,FireCauseSpecific,FireDiscoveryDateTime,FireOutDateTime,FireStrategyPointZonePercent,IncidentName,IncidentShortDescription,IncidentTypeKind,IsFireCauseInvestigated,IsFireCodeRequested,CreatedOnDateTime_dt,ModifiedOnDateTime_dt,SourceGlobalID,IncidentComplexityLevel,POOCity,POOCounty,SourceOID,FireStrategyMonitorPercent,InitialLatitude,InitialLongitude&geometry=&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=&f=json"

large_acre_threshold = 1000

response = None
arcgis_response = None

def get_all():
    global response
    global arcgis_response

    # only fetching the data if we haven't previously done so
    if response == None:
        response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        if arcgis_response == None:
            data = response.json()
            arcgis_response = ArcGISResponse(**data)
    else:
        print("-- BAD REQUEST --")
        return
    
def get_larger_areas():
    """
    Retrieves incidents with an area larger than the specified threshold.
    
    Returns:
    - List of large incidents sorted by size.
    """
    if arcgis_response is None:
        get_all()

    if not hasattr(arcgis_response, 'features') or arcgis_response.features is None:
        raise ValueError("The arcgis_response object is invalid or does not contain 'features'.")

    # filtering
    large_incidents = [
        f for f in arcgis_response.features 
        if hasattr(f, 'IncidentSize') and f.IncidentSize is not None 
        and f.IncidentSize > large_acre_threshold
    ]

    # sorting by IncidentSize
    large_incidents.sort(key=lambda x: x.IncidentSize)

    return large_incidents

def analyze_affected_areas():
    """
    Analyzes the affected areas of fire incidents.
    
    Returns:
    - Dictionary with total fires and count of large fires.
    """
    if arcgis_response is None:
        get_all()

    areas = arcgis_response.get_affected_areas()

    if not areas:
        return None

    # Count fires larger than 1000 acres
    large_fires = [area for area in areas if area > large_acre_threshold]

    return {
        "total_fires": len(areas),
        f"fires_larger_than_{large_acre_threshold}_acres": len(large_fires)
    }

def get_features_by_location(location: str):
    """
    Retrieves fire incidents by location.
    
    Parameters:
    - location (str): The location to filter incidents by.
    
    Returns:
    - List of features that match the specified location.
    """
    if arcgis_response is None:
        get_all()

    if not location:
        print("You need to specify the location")
        return []

    location = location.lower().strip()

    features_returned = [
        f for f in arcgis_response.features 
        if (f.IncidentShortDescription and location in f.IncidentShortDescription.lower()) or
           (f.POOCity and location in f.POOCity.lower()) or
           (f.POOCounty and location in f.POOCounty.lower())
    ]

    return features_returned

def get_features_between_date_range(startDate: datetime, endDate: datetime):
    """
    Retrieves fire incidents within a specified date range.
    
    Parameters:
    - startDate (datetime): The start date of the range.
    - endDate (datetime): The end date of the range.
    
    Returns:
    - List of features within the date range.
    """
    if arcgis_response is None:
        get_all()

    start_timestamp = int(startDate.timestamp() * 1000)
    end_timestamp = int(endDate.timestamp() * 1000)
    
    filtered_features = [
        f for f in arcgis_response.features
        if f.FireDiscoveryDateTime is not None
        and start_timestamp <= f.FireDiscoveryDateTime <= end_timestamp
    ]

    return filtered_features

def analyze_ignition_times(location: str = None, timezone: str = 'US/Pacific'):
    """
    Analyzes the distribution of fire ignition times.
    
    Parameters:
    - location (str, optional): The location to filter incidents by.
    - timezone (str, optional): The timezone for time conversion.
    
    Returns:
    - Dictionary with the hour of most fires, count of most fires, and distribution.
    """
    if arcgis_response is None:
        get_all()

    hour_count = arcgis_response.get_incident_hours(location, timezone)
    if not hour_count:
        return None

    max_hour = max(hour_count, key=hour_count.get)
    max_count = hour_count[max_hour]

    return {
        "most_fires_hour": max_hour,
        "most_fires_count": max_count,
        "hour_distribution": hour_count
    }

# Ensure the "plots" directory exists
if not os.path.exists("plots"):
    os.makedirs("plots")

def plot_incident_hours(location: str = None, timezone: str = 'US/Pacific'):
    """
    Plots the distribution of incident hours and saves the plot.
    
    Parameters:
    - location (str, optional): The location to filter incidents by.
    - timezone (str, optional): The timezone for time conversion.
    
    Returns:
    - str: The path to the saved plot image.
    """
    if arcgis_response is None:
        get_all()

    save_path = os.path.abspath(f"plots/incident_hours_{location if location else 'all'}.png")
    return arcgis_response.plot_incident_hours(location, timezone, save_path)

def plot_affected_areas():
    """
    Plots the distribution of affected areas and saves the plot.
    
    Returns:
    - str: The path to the saved plot image.
    """
    if arcgis_response is None:
        get_all()

    save_path = os.path.abspath("plots/affected_areas.png")
    return arcgis_response.plot_affected_areas(save_path)

def plot_correlation():
    """
    Plots the correlation between ignition time and affected area and saves the plot.
    
    Returns:
    - str: The path to the saved plot image.
    """
    if arcgis_response is None:
        get_all()

    save_path = os.path.abspath("plots/correlation.png")
    return arcgis_response.plot_correlation(save_path)
