from flask import Flask, request, jsonify
import requests 
import xmltodict
import logging 

############################################################################################################################
### CONSTANTS
EPOCH_URL = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml'  
SIGHTING_URL = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA10.xml' 
#SIGHTING_URL = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesINT01.xml'

############################################################################################################################
### FLASK
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

############################################################################################################################
### VARIABLES DECLARED FOR GLOBAL SCOPE
iss_epoch_data = []
iss_sighting_data = []
readonce = False

############################################################################################################################
### MISCELLANEOUS FUNCTIONS
def get_xml_data(url_str:str)->dict:
    """                                                                                                                                                                                              
    Uses input url string to web accessible xml contnet and outputs dictionary filed from parsed xml data                       
    args:
        url_str (str): String of url to xml of ISS positioning data                                                                                                                                  
    returns:                                                                                                                                                                                         
        data_dict (dict): Dictionary containing ISS positioning data                                                                                                                            
    """
    data_resp = requests.get(url=url_str)
    data_dict = xmltodict.parse(data_resp.content)
    logging.info("DATA PARSED SUCCESSFULLY FROM URL")
    return data_dict


############################################################################################################################
### USAGE INFOFORMATION FUNCTION
@app.route('/', methods=['GET'])
def usage_info():
    """                                                                                                                                                                                              
    Called to print usage information for API
        (none)                                                                                                                                  
    returns:                                                                                                                                                                                         
        (str) Formatted Usage Information for users                                                                                                                            
    """
    usage_tab = [
        ['### ISS Positioning and Sighting Data Tracker (ISSPSDT) ###', ''],
        ['',''],
        ['Informational and Management Routes:', ''],
        ['/', '(GET) Print Route Information'],
        ['/load', '(POST) Loads/Overwrites Data from URL ISS sources'  ]
    ]

    pos_tab = [
        ['Epoch, Positioning and Velocity Data Query Routes:', ''],
        ['/epochs', '(GET) List all Epochs'],
        ['/epochs/<epoch>', '(GET) Position and Velocity Data for <epoch>'],
    ]
    
    sight_tab = [
        ['Regional Sightings Data Query Routes:',''],
        ['/countries','(GET) List of all countries in data set'],
        ['/countries/<country>','(GET) Sighting Information in Specified <country>'],
        ['/countries/<country>/regions','(GET) List of all regions in <country>'],
        ['/countries/<country>/regions/<region>','(GET) Sighting Information in Specified <country>&<region>'],
        ['/countries/<country>/regions/<region>/cities','(GET) List of all cities in <country>&<region>'],
        ['/countries/<country>/regions/<region>/cities/<city>','(GET) Sighting Information in Specified <country>&<region>&<city>'],

    ]

    spacer_tab = [
        ['',''],
    ]

    full_tab = usage_tab + spacer_tab + pos_tab + spacer_tab + sight_tab + spacer_tab
    usage_str = '\n'
    for x in full_tab:
        usage_str += ( "    {: <70} {: <70} ".format(*x) + '\n' )
    logging.info("RETURNING USAGE INFORMATION CARD TO USER")
    return usage_str


@app.route('/load', methods=['POST'])
def read_data_from_url():
    """                                                                                                                                                                                              
    Called to update the global positioning and sighting data sets used for services                    
    args:
        (none)                                                                                                                               
    returns:                                                                                                                                                                                         
       (str): Comfirmation of completed parse                                                                                                                           
    """
    global iss_epoch_data
    global iss_sighting_data
    global readonce
    iss_epoch_data = get_xml_data(EPOCH_URL)['ndm']['oem']['body']['segment']['data']['stateVector']
    iss_sighting_data = get_xml_data(SIGHTING_URL)['visible_passes']['visible_pass']
    if not readonce:
        logging.info("DATA LOADED ONCE BY USER")
        readonce = True
    return f'Data has been scraped from ISS positioning and sighting URL sources below: \n \
            Positioning: {EPOCH_URL} \n Sighting: {SIGHTING_URL} \n'
    


############################################################################################################################
### ISS POSITIONING DATA FUNCTIONS 
@app.route('/epochs', methods=['GET'])
def epochs():
    """                                                                                                                                                                                              
    Called to return all epochs in the ISS positioning data set 
    args:                                                                                                                                                                                            
        (none)                                                                                                                                 
    returns:                                                                                                                                                                                       
        (jsonify-ed list): Jsonified List containing all Epochs in Position Data Set                                                                                                                    
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    epoch_vec = []
    for x in iss_epoch_data:
        epoch_vec.append(x['EPOCH'])
    logging.info("SENDING EPOCHS LIST TO USER")
    return jsonify(epoch_vec)


@app.route('/epochs/<epoch>',methods=['GET'])
def epoch_state(epoch):
    """                                                                                                                                                                                              
    Called to return positioning information about specific epoch in the ISS positioning data set                                                                                                                                       
    args:                                                                                                                                                                                            
        epoch (str): String of Epoch obtained from route 
    returns:                                                                                                                                                                                                 
        (jsonify-ed dict): Jsonified Dictionary of Positioning Information at input epoch                                                                                                                    
        (str): Error string stating that specified epoch was not found 
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    for x in iss_epoch_data:
        if epoch == x['EPOCH']:
            logging.info("EPOCH KEY FOUND - SENDING RESPECTIVE DICTIONARY TO USER")
            return jsonify(x)
    logging.error("NO MATCH FOR USER INPUT EPOCH")
    return 'NO MATCH FOR INPUT EPOCH KEY FOUND IN DATA SET \n'



############################################################################################################################
### SIGHTING DATA FUNCTIONS 

@app.route('/countries', methods=['GET'])
def countries():
    """                                                                                                                                                                                              
    Called to return all countries in the ISS sightings data set                                                                                                                                    
    args:                                                                                                                                                                                            
        (none)                                                                                                                                                                                       
    returns:                                                                                                                                                                                         
        (jsonify-ed list): Jsonified List containing all countries in sightings Data Set                                                                                       
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    countries_vec = []
    for x in iss_sighting_data:
        if not (x['country'] in countries_vec):
            countries_vec.append(x['country'])
    logging.info("SENDING COUNTRIES LIST TO USER")
    return jsonify(countries_vec)


@app.route('/countries/<country>',methods=['GET'])
def country_sightings(country):
    """                                                                                                                                                                                              
    Called to return information about sightings in specified country in the ISS sighting data set                                                                                    
                                                                                                                                                                                                     
    args:                                                                                                                                                                                            
        country (str): String of country obtained from route                                                                                                                                             
    returns:                                                                                                                                                                                      
        (jsonify-ed dict): Jsonified Dictionary of sighting information at input country                                                                                                          
        (str): Error string stating that specified country was not found                                                                                                                               
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    country_info_vec = []
    for x in iss_sighting_data:
        if country == x['country']:
            country_info_vec.append(x)
    if len(country_info_vec)>0:
        logging.info("SENDING COUNTRY SIGHTING INFORMATION TO USER")
        return jsonify(country_info_vec)
    else:
        logging.error("NO MATCH FOR USER INPUT COUNTRY")
        return 'NO MATCH FOR INPUT COUNTRY KEY FOUND IN DATA SET \n'

@app.route('/countries/<country>/regions',methods=['GET'])
def country_regions(country):
    """                                                                                                                                                                                              
    Called to return sighting regions in specified country in the ISS sighting data set                                                                                                    
    args:                                                                                                                                                                                            
        country (str): String of country obtained from route                                                                                                                                         
    returns:                                                                                                                                                                                                 
        (jsonify-ed list): Jsonified list of sighting regions in input country                                                                                                                     
        (str): Error string stating that specified country was not found                                                                                                                                 
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    country_info_vec = []
    for x in iss_sighting_data:
        if country == x['country']:
            country_info_vec.append(x)
    if len(country_info_vec)>0:
        regions_list = []
        for y in country_info_vec:
            if not (y['region'] in regions_list):
                regions_list.append(y['region'])
        logging.info("SENDING REGIONS (IN COUNTRY) LIST TO USER")
        return jsonify(regions_list)
    else:
        logging.error("NO MATCH FOR USER INPUT COUNTRY")
        return 'NO MATCH FOR INPUT COUNTRY KEY FOUND IN DATA SET \n'


@app.route('/countries/<country>/regions/<region>',methods=['GET'])
def country_region_info(country,region):
    """                                                                                                                                                                                              
    Called to return sighting info in specified country and region in the ISS sighting data set                                                                                                              
    args:                                                                                                                                                                                            
        country (str): String of country obtained from route
        region (str): String of region obtained from route
    returns:                                                                                                                                                                                         
        (jsonify-ed dict): Jsonified dictionary of sighting information for specified country-region                                                                                                                      
        (str): Error string stating that specified country or region was not found                                                                                                                           
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    country_info_vec = []
    for x in iss_sighting_data:
        if country == x['country']:
            country_info_vec.append(x)
    if len(country_info_vec)>0:
        region_info_vec = []
        for y in country_info_vec:
            if y['region'] == region:
                region_info_vec.append(y)
        if len(region_info_vec)>0:
            logging.info("SENDING COUNTRY-REGION SIGHTING INFORMATION TO USER")
            return jsonify(region_info_vec)
        else:
            logging.error("NO MATCH FOR USER INPUT REGION")
            return 'NO MATCH FOR INPUT REGION KEY FOUND IN COUNTRY DATA SET \n'
        
    else:
        logging.error("NO MATCH FOR USER INPUT COUNTRY")
        return 'NO MATCH FOR INPUT COUNTRY KEY FOUND IN DATA SET \n'


@app.route('/countries/<country>/regions/<region>/cities',methods=['GET'])
def country_region_cities(country,region):
    """                                                                                                                                                                                              
    Called to return the cities in the specified country and region in the ISS sighting data set                                                                                                     
    args:
        country (str): String of country obtained from route                                                                                                                                                 
        region (str): String of region obtained from route                                                                                                                                               
    returns:                                                                                                                                                                                         
        (jsonify-ed list): Jsonified list of cities in specified country-region                                                                                                                              
        (str): Error string stating that specified country or region was not found                                                                                                                              
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    country_info_vec = []
    for x in iss_sighting_data:
        if country == x['country']:
            country_info_vec.append(x)
    if len(country_info_vec)>0:
        region_info_vec = []
        for y in country_info_vec:
            if y['region'] == region:
                region_info_vec.append(y)
        if len(region_info_vec)>0:
            cities_list = []
            for z in region_info_vec:
                if not (z['city'] in cities_list):
                    cities_list.append(z['city'])
            logging.info("SENDING CITIES (IN COUNTRY-REGION) LIST TO USER")
            return jsonify(cities_list)
        else:
            logging.error("NO MATCH FOR USER INPUT REGION")
            return 'NO MATCH FOR INPUT REGION KEY FOUND IN COUNTRY DATA SET \n'
    else:
        logging.error("NO MATCH FOR USER INPUT COUNTRY")
        return 'NO MATCH FOR INPUT COUNTRY KEY FOUND IN DATA SET \n'


@app.route('/countries/<country>/regions/<region>/cities/<city>',methods=['GET'])
def country_region_city_info(country,region,city):
    """ 
    Called to return the sighting data in the specified country-region-city in the ISS sighting data set                                                                                                                                                          
    args:                                                                                                                                                                                                                                                            
        country (str): String of country obtained from route                                                                                                                                                 
        region (str): String of region obtained from route 
        city (str): String of city obtained from route                                                                                                                                              
    returns:                                                                                                  
        (jsonify-ed dict): Jsonified dictionary of sightings in specified country-region-city                                                                                                                              
        (str): Error string stating that specified country, region, or city was not found                                                                                                                                                                                                                                    
    """
    if not readonce:
        logging.warning("USER HAS NOT LOADED DATA SET BUT ATTEMPTING TO USE SERVICES")
        return 'Use /load route to load data before proceeding \n'
    country_info_vec = []
    for x in iss_sighting_data:
        if country == x['country']:
            country_info_vec.append(x)
    if len(country_info_vec)>0:
        region_info_vec = []
        for y in country_info_vec:
            if y['region'] == region:
                region_info_vec.append(y)
        if len(region_info_vec)>0:
            cities_info_vec = []
            for z in region_info_vec:
                if z['city'] == city:
                    cities_info_vec.append(z)
            if len(cities_info_vec)>0:
                logging.info("SENDING COUNTRY-REGION-CITY SIGHTING INFORMATION TO USER")
                return jsonify(cities_info_vec)
            else:
                logging.error("NO MATCH FOR USER INPUT CITY")
                return 'NO MATCH FOR INPUT CITY KEY FOUND IN COUNTRY-REGION DATA SET \n'
        else:
            logging.error("NO MATCH FOR USER INPUT REGION")
            return 'NO MATCH FOR INPUT REGION KEY FOUND IN COUNTRY DATA SET \n'
    else:
        logging.error("NO MATCH FOR USER INPUT COUNTRY")
        return 'NO MATCH FOR INPUT COUNTRY KEY FOUND IN DATA SET \n'

############################################################################################################################
### MAIN 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

############################################################################################################################
