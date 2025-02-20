## Application Description
The following refers to a Flask Client Application. Bellow you can find a short description. Examples of How to use and run can be found in the section: "How to use".

The application can take as input the area of interest and provide the most common day time of Fire Incidents. If no location provided it will return the a table that demonstates time over the sum of fires for this time. That input is provided in the URL of the client created.

Moreover, you can explore the distribution of the fire, being able to find the fires that are larger than 1000 acres. Input to be added in the URL.

Later on, you can provide a date range in the format of YY-MM-DD in order to get the number of incidents on that frame. Input to be added in the URL. 

Finally, there is a graphical representation of Final Acres Area of fire and time that the incident happened. This can support for easier interprentation of data.

If you wish to know more regarding the flow of the application, please take a look in the UML Diagram provided.


## System Requirements
Python version : 13.3 

Libraries used:
requests 
matplotlib
datetime
json
flask
os
pandas

All the requirements can be found in requests.txt file. 
Since the application will be running through docker container, there is no need to install anything locally. 

If you wish to run it locally use, instructions can be found in the section: "How to use".


## How to use
In order to the application the following steps are required: 

#### Run Application using Docker Compose
Before you run locally, clone this repository: 
```
git clone https://github.com/sathanasiou/OroraTech_Application.git
cd OroraTech_Application
```
1. Make sure a docker client is installed, try: 
```
python --version
```
If there is no output, please install python. 
Corresponding documentation can be found here: 
* Python installation : https://www.python.org/downloads/

2. Create a virtual environment

```
python -m venv venv
```
Source it, using the following based on your OS. 
For macOS or Linux: 
```
sourse venv/bin/activate
```
For Windows: 
```
venv\Script\activate
```

3. Install the required Libraries: 
```
pip install -r requirements.txt
```
4. Run the application: 
```
python flask.py
```
5. Test the application: 

The application will lounch in the following page: 


Supported URIs: 
```
GET /fires/location?location=<location_name> -- ok 
GET /fires/date?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD -- ok 
GET /fires/areas -- ok 
GET /plots/incident_hours?location=<location_name>&timezone=<timezone> --ok 
GET /plots/affected_areas -- ok 
GET /plots/correlation -- ok
GET /analysis/ignition_times?location=<location_name>&timezone=<timezone>
GET /analysis/affected_areas -- ok 
```

There is also a Postman collection added to the repository for easy testing of the API.

## Constrains - Observations

* Sometimes location is not part of the POOCity or the POOCountry so there is the need to search also in other fields, such us IncidentName. 
* In the requirements it was mentioned to search for Colorado through while studying the API I could not find entries for Colorado.
* The API Documentation is not refering to the measurement unit and to parameters (input) limitations, making it harder to understand what the inputs you are providing are representing. For example in the Field FinalAcres, there is no description so that you can relate the values to acre, meters or other. In the current application we are assuming that the value is using acres.
* The management of different time zones in order to be able to correctly interpret the results.
* Scalability issues, if data grow larger, the application currently is not ready to support that. 

