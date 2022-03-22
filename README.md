# ISS Positioning and Signting Data Tracker (ISSPSDT)
The International Space Station Positional and Sighting Data Tracker (ISSPSDT) was motivated by the following scenario:

“We have found an abundance of positional data for the International Space Station (ISS). It is full of interesting information including ISS position and velocity data at given times, as well as when the ISS can be seen over select cities. It is a challenge, however, to sift through the data manually to find what we are looking for.”

In order to sift through this abundance of ISS data we've created the ISSPSDT REST API which permits a serving machine to load in all of this abundant ISS data (either via file or scraped straight from the source) and process it for an external user's usage via a network utilizing HTTPs communications and URL verbiage. This allows an external client or user to request key sections of the ISS data sets via this API from another serving machine (server). Additionally, developing a web API to organize this data allows for the compartmentalization of our software packages and separation of this implementation from any of its clients code – compartmentalization and separation of packages is important for testing, management, organization, and the security of assets. As you will see, this ISSPSDT API allows clients with an internet connection (which permits communication to the serving connection) to receive ISS data for analysis or use in their own applications.

#
# Pulling from Dockerhub
 
Aside from being here on Github, the ISSPSDT pre-built working container is also on Dockerhub and can be pulled with the command below. Note that this repository also provides the tools necessary to build an image of this repository as well.

    docker pull petelealiieej/isspdt

(notice that this image is pulled as isspdt and NOT isspsdt)

#
# Setting Up for Full Functionality 
Because of some of the rubric requirements for this project, the ISS data sets need to be downloaded from this [link](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq) in order to containerize the repository. Although having local data sets is not required for usage of the API, the user can download them with the following command which utilizes wget to download the data set xmls into the correct location of the repository (the repository directory itself):

    [repo_dir]$ make data 

this command downloads two xml data sets from the [link](https://data.nasa.gov/Space-Science/ISS_COORDS_2022-02-13/r6u8-bhhq): 
- Public Distribution File [xml file]
- XMLsightingData_citiesUSA10 [xml file]


#
# Python Dependencies, Functionality and Testing

The app.py file works as the primary (only) body of programming needed for services and use this API. The python script utilizes the flask, requestsF, xmltodict, logging and socket libraries in its development and the external dependencies are downloaded via the following commands 

    []$ pip3 install --user flask
    []$ pip3 install --user requests
    []$ pip3 install --user xmltodict

The app.py python script starts with a few string constants which may be of importance to the user - EPOCH_URL (str), SIGHTING_URL (str), EPOCH_FILE (str), and SIGHTING_FILE (str). These constants are as they are for use in the functions below them and for easy accessibility and change should the source strings/names change.

Next, the flask library is used to create the application variable and configure the application to not sort our json keys when returning - this is done to keep the original organization of the data:

    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False        

Additionally, because many of the services provided by this api can go wrong and because we would like to provide adequate debugging information, the logging format below is used with a configuration level set below DEBUG:

    format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=format_str)

Note that logging is used across all functions to tell (on the servicing side) when request are made, when they are successful, and when they fail for debugging and logging purposes.

We then put some variables in the global scope in order to preserve and save their values during communications with the server

    iss_epoch_data = []
    iss_sighting_data = []
    readonce = False


Next, the HTTP routes are shared with the user with the usage_info() function on the '/' GET route and it simply prints all the routes and what they return to the user. This is implemented so clients can see what they can get from the service and become familiar with the API.

Because data must be read from two sources and saved via POST methods, we include two functions: get_xml_data_url(str) and get_xml_data_file(str) to parse the data using the xmltodict library from an xml file on the internet and in a local file, respectively. These two functions are utilized, respectively, on the '/load_url' and '/load_file' application routes to load the xml data into the application.

The next few functions have different things they return; However, they all work similarly to one another. Understanding this, a general explanation is provided for each general route case.

The '/things' GET routes, whether those "things" be epochs, countries, regions, or cities, returns all of the values for a given key in a set of data. Should there be multiple things-s, such as in a '/things1/<thing1\>/things2>' route, then the service will return all values for the things2 key in data elements from thing1 and its subsequent filtering. This is done in the functions below by sifting through all the elements in the current element data list and appending to a new specialized-specific organized list only containing data elements respective to the route - doing this for each group of things gives a filtered list of the things the user is looking for. Functions that use this method:
- epoch() -> '/epoch'
- countries() -> 'countries'
- country_regions(country) -> '/countries/<country\>/regions'
- country_regions_cities(country,region) -> '/countries/<country\>/regions/<region\>/cities'

The '/things1/<thing1\>' GET routes, filters through data elements like the methods above BUT these routes return (entire) dictionaries which include thing1 rather than just elements at a given key by separating elements which don't have the corresponding thing1 value at the things1 key. Functions that use this method include:
- epoch_state() -> '/epochs/<epoch\>'
- country_sightings(country) -> 'countries/<country\>'
- country_region_info(country,region) -> '/countries/<country\>/regions/<region\>'
- country_regions_cities_info(country,region) -> '/countries/<country\>/regions/<region\>/cities/<city\>'

All of the functions utilized in the app.py file are unit tested via pytest, for correct return values, return types, and exceptions to ensure that the application works and continues working with changes to the implementation. Running the pytest at the repository directory should show 6 completed test as seen below - if not please submit an issue via github:

    [repo_dir]$ pytest

should return:

    ======================================================================================== test session starts =========================================================================================
    platform linux -- Python 3.6.8, pytest-7.0.1, pluggy-1.0.0
    rootdir: /home/<you>/ISSPSDT
    collected 6 items                                                                                                                                                                                    

    test_app.py ......                                                                                                                                                                             [100%]

    ========================================================================================= 6 passed in <some time> ==========================================================================================



#
# Spinning up and down the Service

Next, there are two possibilities: either spin up the service using the repository or containerize a service and run it in the container 

To start service with repository locally, set Flask environmental variables and spin up flask service.

    [repo_dir]$ export FLASK_APP=app.py
    [repo_dir]$ export FLASK_ENV=development
    [repo_dir]$ flask run -p <port_num>

Alternatively, build a container image and start the service in a container rather than the terminal with the following automated Make commands:

    [repo_dir]$ make data
    [repo_dir]$ make build
    [repo_dir]$ make run

For the container method, running the following automated Make command will give information about the running images services keyed to the {name} variable in the Makefile.

    [repo_dir]$ make ps

From the above command you will get a service image number, and with that number you can shutdown the service and remove the service via the following commands

    []$ docker stop <service_image_num>
    []$ docker rm <service_image_num>

To stop the service in the repository utilization method simply kill the service via 

    [service_terminal]$ (ctrl+c)


#
# Interacting with a Server running this API

Interacting with the server is done through various HTTP routes and requests. In order to communicate with the server and through the API the host machine will have to be spun up via the instruction in the previous section

Next, notice that all HTTP routes are given when requesting the following route from the host machine running the API. Note that <host\> is the host address and <port\> is the port the service is using. Additionally note that the automated containerization makes the host local (host==localhost) and services at port 5015.

    curl <host>:<port>/

This command returns the following reference card which describes the routes and what they do when utilizing the API:


    ### ISS Positioning and Sighting Data Tracker (ISSPSDT) ###                                                                                   
                                                                                                                                                  
    Informational and Management Routes:                                                                                                          
    /                                                             (GET) Print Route Information                                          
    /load_url                                                     (POST) Loads/Overwrites Data from URL ISS sources                      
    /load_file                                                    (POST) Loads/Overwrites Data from local ISS data files                 
                                                                                                                                                  
    Epoch, Positioning and Velocity Data Query Routes:                                                                                            
    /epochs                                                       (GET) List all Epochs                                                  
    /epochs/<epoch>                                               (GET) Position and Velocity Data for <epoch>                           
                                                                                                                                                  
    Regional Sightings Data Query Routes:                                                                                                         
    /countries                                                    (GET) List of all countries in data set                                
    /countries/<country>                                          (GET) Sighting Information in Specified <country>                      
    /countries/<country>/regions                                  (GET) List of all regions in <country>                                 
    /countries/<country>/regions/<region>                         (GET) Sighting Information in Specified <country>&<region>             
    /countries/<country>/regions/<region>/cities                  (GET) List of all cities in <country>&<region>                         
    /countries/<country>/regions/<region>/cities/<city>           (GET) Sighting Information in Specified <country>&<region>&<city>   


To access any of the "Epoch, Positioning and Velocity Data Query" or "Regional Sightings Data Query" routes, one must load in the data via either of the '/load_' POST routes depending on preference.

    []$ curl <host>:<port>/load_url -X POST

-or-

    []$ curl <host>:<port>/load_file -X POST

Users will get either of the following messages if loading was completed successfully:

    Data has been scraped from ISS positioning and sighting URL sources below: 
    Positioning: https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml 
    Sighting: https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA10.xml 

-or-

    Data has been scraped from ISS positioning and sighting files below: 
    Positioning: ISS.OEM_J2K_EPH.xml 
    Sighting: XMLsightingData_citiesUSA10.xml 

To access the data from the routes above, the user will follow the following format where <route\> is one of the routes shown above:

    []$ curl <host>:<port>/<route>


An few examples are given below:
#

Request:

    []$ curl <host>:<port>/epochs

Returns:  

    [
        "2022-042T12:00:00.000Z", 
        "2022-042T12:04:00.000Z", 
        "2022-042T12:08:00.000Z", 
        ...
        "2022-057T11:56:56.869Z", 
        "2022-057T12:00:00.000Z"
    ]

#

Request:


    []$ curl <host>:<port>/countries/United_States

Returns:  

    [
    {
        "country": "United_States", 
        "region": "Texas", 
        "city": "Carrizo_Springs", 
        "spacecraft": "ISS", 
        "sighting_date": "Tue Feb 15/06:11 AM", 
        "duration_minutes": "4", 
        "max_elevation": "14", 
        "enters": "10 above SSE", 
        "exits": "10 above E", 
        "utc_offset": "-6.0", 
        "utc_time": "12:11", 
        "utc_date": "Feb 15, 2022"
    }, 
    ...
    {
        "country": "United_States", 
        "region": "Texas", 
        "city": "Orange", 
        "spacecraft": "ISS", 
        "sighting_date": "Sat Feb 19/04:39 AM", 
        "duration_minutes": "1", 
        "max_elevation": "17", 
        "enters": "17 above E", 
        "exits": "10 above ENE", 
        "utc_offset": "-6.0", 
        "utc_time": "10:39", 
        "utc_date": "Feb 19, 2022"
    }, 
    ...
    ]



#

Request: 

    []$ curl <host>:<port>/countries/United_States/regions

Returns: 

    [
    "Texas", 
    "Utah", 
    "Vermont", 
    "Virgin_Islands", 
    "Virginia"
    ]


#

Notice that each route above returns what’s expected and said in the informational provided by the ‘\’ route; However, should a you make a request at an unrecognized URL they will receive an error message like the one below:

Request:

    []$ curl <host>:<port>/epochs/this_doesnt_exist


Returns:

    NO MATCH FOR INPUT EPOCH KEY FOUND IN DATA SET 




