from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import main 
from geometry import Geometry
import os

app = Flask(__name__)

def serialize_feature(f):
    """
    Serialize a feature object to a dictionary, converting the geometry to a dictionary if applicable.
    
    Parameters:
    - f: The feature object to serialize.
    
    Returns:
    - dict: A dictionary representation of the feature.
    """
    feature_dict = vars(f).copy()
    if 'geometry' in feature_dict and isinstance(feature_dict['geometry'], Geometry):
        feature_dict['geometry'] = feature_dict['geometry'].to_dict()
        return feature_dict

@app.route('/fires/location', methods=['GET'])
def get_fires_by_location():
    """
    Endpoint to get fire incidents by location.
    Expects a 'location' query parameter.
    
    Returns:
    - JSON: A list of serialized fire features matching the location.
    """
    location = request.args.get('location', '')

    results = []
    if location:
        results.extend(main.get_features_by_location(location))

    return jsonify([serialize_feature(f) for f in results])


@app.route('/fires/date', methods=['GET'])
def get_fires_between_range():
    """
    Endpoint to get fire incidents between a date range.
    Expects 'start_date' and 'end_date' query parameters in YYYY-MM-DD format.
    
    Returns:
    - JSON: A list of serialized fire features within the date range or an error message.
    """
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    results = []

    # Convert dates
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    if start_dt and end_dt:
        results.extend(main.get_features_between_date_range(start_dt, end_dt))
    else:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    
    return jsonify([serialize_feature(f) for f in results])
        
@app.route('/fires/areas', methods=['GET'])
def get_larger_fire_areas():
    """
    Endpoint to get fire areas larger than a certain threshold.
    
    Returns:
    - JSON: A list of serialized fire features with large areas or a message if none are found.
    """
    results = []
    results.extend(main.get_larger_areas())
    if len(results) == 0:
        return jsonify({"message": "Could not find any areas"})
    else:
        return jsonify([serialize_feature(f) for f in results])

@app.route('/plots/incident_hours', methods=['GET'])
def get_incident_hours_plot():
    """
    Endpoint to get a plot of incident hours.
    Expects optional 'location' and 'timezone' query parameters.
    
    Returns:
    - File: The plot image file if available, or an error message.
    """
    location = request.args.get('location', None)
    timezone = request.args.get('timezone', 'US/Pacific')
    plot_path = main.plot_incident_hours(location, timezone)
    if plot_path:
        return send_from_directory(os.path.dirname(plot_path), os.path.basename(plot_path))
    else:
        return jsonify({"error": "No data to plot."}), 404

@app.route('/plots/affected_areas', methods=['GET'])
def get_affected_areas_plot():
    """
    Endpoint to get a plot of affected areas.
    
    Returns:
    - File: The plot image file if available, or an error message.
    """
    plot_path = main.plot_affected_areas()
    if plot_path:
        #return jsonify({"message" : f"image is saved in {plot_path}"})
         return send_from_directory(os.path.dirname(plot_path), os.path.basename(plot_path))
    else:
        return jsonify({"error": "No data to plot."}), 404

@app.route('/plots/correlation', methods=['GET'])
def get_correlation_plot():
    """
    Endpoint to get a plot of the correlation between fire ignition time and affected area.
    
    Returns:
    - File: The plot image file if available, or an error message.
    """
    plot_path = main.plot_correlation()
    if plot_path:
        return send_from_directory(os.path.dirname(plot_path), os.path.basename(plot_path))
    else:
        print("No data to plot.")
        return jsonify({"error": "No data to plot."}), 404

@app.route('/analysis/ignition_times', methods=['GET'])
def analyze_ignition_times():
    """
    Endpoint to analyze ignition times of fires.
    Expects optional 'location' and 'timezone' query parameters.
    
    Returns:
    - JSON: Analysis results or an error message if no data is available.
    """
    location = request.args.get('location', None)
    timezone = request.args.get('timezone', 'US/Pacific')

    analysis_result = main.analyze_ignition_times(location, timezone)
    if analysis_result:
        return jsonify(analysis_result)
    else:
        return jsonify({"error": "No data to analyze."}), 404
    
@app.route('/analysis/affected_areas', methods=['GET'])
def analyze_affected_areas():
    """
    Endpoint to analyze affected areas of fires.
    
    Returns:
    - JSON: Analysis results or an error message if no data is available.
    """
    analysis_result = main.analyze_affected_areas()
    if analysis_result:
        return jsonify(analysis_result)
    else:
        return jsonify({"error": "No data to analyze."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
