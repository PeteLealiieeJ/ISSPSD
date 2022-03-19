from flask import Flask, request, jsonify
import requests 
import xmltodict


# CONSTANTS
epoch_url_str = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml'  
sghtng_url_str = '' 
app = Flask(__name__)

"""
index == i (int)
data['ndm']['oem']['body']['segment']['data']['stateVector'][ i ]['X_DOT']['#text']
"""


# FUNCTIONS
def get_xml_data(url_str:str)->dict:
    """                                                                                                                                                                                              
    Uses input url string and outputs dictionary of parsed xml data
                               
    args:
        url_str (str): String of url to xml of ISS positioning data                                                                                                                                  
    returns:                                                                                                                                                                                         
        data_dict (dict): Dictionary containing ISS positioning data                                                                                                                            
    """
    data_resp = requests.get(url=url_str)
    data_dict = xmltodict.parse(data_resp.content)
    return data_dict


@app.route('/epochs', methods=['GET'])
def epochs():
    """                                                                                                                                                                                              
    Called to return all epochs in the ISS positioning data set 

    args:                                                                                                                                                                                            
        (none)                                                                                                                                 
    returns:                                                                                                                                                                                         
        (jsonify-ed list): Jsonified List containing all Epochs in Posiition Data Set                                                                                                                    """

    data = get_xml_data(epoch_url_str)['ndm']['oem']['body']['segment']['data']['stateVector']
    epoch_vec = []
    for x in data:
        epoch_vec.append(x['EPOCH'])
    return jsonify(epoch_vec)


@app.route('/epochs/<epoch>',methods=['GET'])
def epoch_state(epoch):
    """                                                                                                                                                                                              
    Called to return information about specfic epoch in the ISS positioning data set                                                                                                                                       
    args:                                                                                                                                                                                            
        epoch (str): String of Epoch obtained from route 
    returns:                                                                                                                                                                                                 (jsonify-ed list): Jsonified Dictionary of Positioning Information at input epoch                                                                                                                    (str): Error string stating that specified epoch was not found 
    """

    data = get_xml_data(epoch_url_str)['ndm']['oem']['body']['segment']['data']['stateVector']
    for x in data:
        if epoch == x['EPOCH']:
            return jsonify(x)
    return 'NO MATCH FOR INPUT EPOCH KEY FOUND IN DATA SET'


# MAIN 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
