from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
from feature import *
from field import *
from spatialReference import *
import pytz
import numpy
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' for non-GUI usage
import matplotlib.pyplot as plt

class ArcGISResponse:
    def __init__(self, objectIdFieldName, uniqueIdField, globalIdFieldName, geometryType, spatialReference, fields, exceededTransferLimit, features):
        self.objectIdFieldName = objectIdFieldName
        self.uniqueIdField = uniqueIdField
        self.globalIdFieldName = globalIdFieldName
        self.geometryType = geometryType
        self.spatialReference = SpatialReference(**spatialReference)
        self.fields = [Field(**field) for field in fields]
        self.exceededTransferLimit = exceededTransferLimit
        self.features = [Feature(**feature['attributes'], geometry=feature['geometry']) for feature in features]

    def get_incident_hours(self, location: str = None, timezone: str = 'US/Pacific') -> dict:
        """
        Extracts the hour of the day from FireDiscoveryDateTime for incidents.
        Converts UTC timestamps to the specified local time zone.
        If a location is provided, filters incidents by location.

         Parameters:
        - location (str, optional): Filters incidents by a specified location. Defaults to None.
        - timezone (str, optional): Specifies the time zone for converting timestamps. Defaults to 'US/Pacific'.
        
        Returns:
        Returns a dictionary with hours (0-23) as keys and incident counts as values.
        """
        hour_count = defaultdict(int)  # Initialize a dictionary to count incidents by hour

        collection = []

        # Filter features by location if provided
        if location is not None:
            temp_collection = [
                f for f in self.features
                if (f.IncidentShortDescription is not None and location in f.IncidentShortDescription) or
                    (f.POOCity is not None and location in f.POOCity)
            ]
            if len(temp_collection) == 0:
                print("Could not find specified location")
                return {}
            else:
                collection = temp_collection
        else:
            collection = self.features

        # Define the time zone
        tz = pytz.timezone(timezone)

        # Extract the hour of the day from FireDiscoveryDateTime and convert to local time
        for feature in collection:
            if feature.FireDiscoveryDateTime is not None and isinstance(feature.FireDiscoveryDateTime, (int, float)):
                timestamp_seconds = feature.FireDiscoveryDateTime / 1000
                # Get UTC time
                utc_time = datetime.utcfromtimestamp(timestamp_seconds)  
                # Convert to local time
                local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(tz)  
                # Extract the hour (0-23)
                hour = local_time.hour
                # Increment the count for this hour
                hour_count[hour] += 1  

        return hour_count
    
    # You can either specify the location (str) and the timeZone (str) ['US/Pacific', 'US/Eastern', 'US/Central', 'US/Mountain']
    # or leave the field empty, which by default the location = None and the timeZone = 'US/Pacific'
    # Example: arcgis_response.plot_incident_hours("Ventura", 'US/Pacific')
    # arcgis_response.plot_incident_hours()
    def plot_incident_hours(self, location: str = None, timezone: str = 'US/Pacific', save_path: str = None):
        """
        Plots the frequency of incidents by hour of the day and saves the plot as an image if a path is provided.
        
        Parameters:
        - location (str, optional): Filters incidents by a specified location. Defaults to None.
        - timezone (str, optional): Specifies the time zone for converting timestamps. Defaults to 'US/Pacific'.
        - save_path (str, optional): Path to save the plot image. If not provided, the plot will not be saved.
        
        Returns:
        - str or None: The path to the saved plot image if save_path is provided; otherwise, None.
        """
        hour_count = self.get_incident_hours(location, timezone)

        if not hour_count:
            print("No data to plot.")
            return None

        # Prepare data for plotting
        hours = sorted(hour_count.keys())
        counts = [hour_count[hour] for hour in hours]

        # Plot the data
        plt.figure()
        plt.bar(hours, counts, color='skyblue')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Incidents')
        plt.title(f'Incident Frequency by Hour of the Day ({location if location else "All Locations"})')
        plt.xticks(range(24))  # Ensure all hours (0-23) are shown on the x-axis
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the plot as an image
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            return None

    def get_affected_areas(self):
        """
        Retrieves a list of the sizes of incidents (e.g., affected areas in acres).
        
        Returns:
        - list: A list of incident sizes.
        """
        areas = [f.IncidentSize for f in self.features if hasattr(f, 'IncidentSize') and f.IncidentSize is not None]
        return areas

    def plot_affected_areas(self, save_path: str = None):
        """
        Plots the distribution of fire-affected areas and saves the plot as an image if a path is provided.
        
        Parameters:
        - save_path (str, optional): Path to save the plot image. If not provided, the plot will not be saved.
        
        Returns:
        - str or None: The path to the saved plot image if save_path is provided; otherwise, None.
        """
        areas = self.get_affected_areas()
        if not areas:
            print("No data to plot.")
            return None

        # Plot the data
        plt.figure()
        plt.hist(areas, bins=50, color='orange')
        plt.xlabel('Affected Area (acres)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Fire Affected Areas')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save the plot as an image
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            return None


    # Correlation between the time the fire was discovered and the size of the fire
    # opos eixame pei Sofaki
    def analyze_correlation(self):
        """
        Analyzes the correlation between the time a fire was discovered and the size of the fire.
        
        Returns:
        - float or None: The correlation coefficient between discovery times and incident sizes, or None if insufficient data.
        """
        data = []
        for f in self.features:
            if hasattr(f, 'FireDiscoveryDateTime') and f.FireDiscoveryDateTime is not None and hasattr(f, 'IncidentSize') and f.IncidentSize is not None:
                data.append((f.FireDiscoveryDateTime, f.IncidentSize))

        if not data:
            return None

        ignition_times = [d[0] for d in data]
        areas = [d[1] for d in data]
        
        # Calculate correlation
        correlation_matrix = numpy.corrcoef(ignition_times, areas) if len(data) > 1 else None
        correlation = correlation_matrix[0, 1]  # Extract the correlation coefficient
        return correlation

    def plot_correlation(self, save_path: str = None):
        """
        Plots the correlation between ignition time and final area and saves the plot as an image.

         Parameters:
        - save_path (str, optional): Path to save the plot image. If not provided, the plot will not be saved.
        
        Returns:
        - str or None: The path to the saved plot image if save_path is provided; otherwise, None.
        """
        data = []
        for f in self.features:
            if hasattr(f, 'FireDiscoveryDateTime') and f.FireDiscoveryDateTime is not None and hasattr(f, 'IncidentSize') and f.IncidentSize is not None:
                data.append((f.FireDiscoveryDateTime, f.IncidentSize))

        if not data:
            print("No data to plot.")
            return None

        ignition_times = [d[0] for d in data]
        areas = [d[1] for d in data]

        # Plot the data
        plt.figure()
        plt.scatter(ignition_times, areas, alpha=0.5)
        plt.xlabel('Ignition Time (Timestamp)')
        plt.ylabel('Affected Area (acres)')
        plt.title('Correlation Between Ignition Time and Final Area')
        plt.grid(linestyle='--', alpha=0.7)

        # Save the plot as an image
        if save_path:
            print(f"Saving plot to: {save_path}")
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            return None
