from typing import Type
from app import get_xml_data_url 
from app import get_xml_data_file
from app import usage_info
from app import read_data_from_url
from app import read_data_from_file 
from app import epochs 
from app import *
# TESTING OF ROUTE FUNCTIONS WAS NOT PRIORITIZED AS INSTRUCTED 
# VIA SLACK, BUT EPOCHS() ROUTE WAS TESTED BELOW BEFORE BEING 
# INFORMED
import pytest

TEST_EPOCH_URL = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml'
TEST_SIGHTING_URL = 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA10.xml' 
TEST_EPOCH_FILE = 'ISS.OEM_J2K_EPH.xml'
TEST_SIGHTING_FILE = 'XMLsightingData_citiesUSA10.xml'

############################################################################################################################

def test_get_xml_data_url():
    assert get_xml_data_url(TEST_EPOCH_URL)['ndm']['oem']['body']['segment']['data']['stateVector'][0]['EPOCH'] \
        == '2022-042T12:00:00.000Z' 
    assert get_xml_data_url(TEST_SIGHTING_URL)['visible_passes']['visible_pass'][0]['region'] \
        == 'Texas'
    assert isinstance(get_xml_data_url(TEST_EPOCH_URL)['ndm']['oem']['body']['segment']['data']['stateVector'][0]['EPOCH'], str) == True
    assert isinstance(get_xml_data_url(TEST_SIGHTING_URL)['visible_passes']['visible_pass'][0]['region'], str) == True
    assert isinstance(get_xml_data_url(TEST_EPOCH_URL), dict) == True
    assert isinstance(get_xml_data_url(TEST_SIGHTING_URL), dict) == True
    return

def test_get_xml_data_url():
    with pytest.raises(TypeError):
        get_xml_data_url(404)
    return 

############################################################################################################################

def test_get_xml_data_file():
    assert get_xml_data_file(TEST_EPOCH_FILE)['ndm']['oem']['body']['segment']['data']['stateVector'][0]['EPOCH'] \
        == '2022-042T12:00:00.000Z' 
    assert get_xml_data_file(TEST_SIGHTING_FILE)['visible_passes']['visible_pass'][0]['region'] \
        == 'Texas'
    assert isinstance(get_xml_data_file(TEST_EPOCH_FILE)['ndm']['oem']['body']['segment']['data']['stateVector'][0]['EPOCH'], str) == True
    assert isinstance(get_xml_data_file(TEST_SIGHTING_FILE)['visible_passes']['visible_pass'][0]['region'], str) == True
    assert isinstance(get_xml_data_file(TEST_EPOCH_FILE), dict) == True
    assert isinstance(get_xml_data_file(TEST_SIGHTING_FILE), dict) == True
    return

def test_get_xml_data_file():
    with pytest.raises(TypeError):
        get_xml_data_file(404)
    return 

############################################################################################################################

def test_usage_info():
    assert isinstance( usage_info(), str) == True

# IT IS A DISPLAY FUNCTION NO EXCEPTIONS ARE FORSEEABLE

############################################################################################################################

def test_read_data_from_url():
    assert isinstance( read_data_from_url(), str ) == True

# ANY ERROR IN THIS FUNCTION WOULD OCCUR AT THE GET DATA FUNCTION WHICH HAS BEEN ADEQUATELY
# TESTED ABOVE, THIS FUNCTION IS ONLY USED TO UPDATE GLOBAL VARIABLES IN THE APP WHICH MAKES
# THOSE CHANGING VARIABLES INACCESSIBLE EXTERNALLY 

############################################################################################################################

def test_read_data_from_file():
    assert isinstance( read_data_from_file(), str ) == True

# ANY ERROR IN THIS FUNCTION WOULD OCCUR AT THE GET DATA FUNCTION WHICH HAS BEEN ADEQUATELY
# TESTED ABOVE, THIS FUNCTION IS ONLY USED TO UPDATE GLOBAL VARIABLES IN THE APP WHICH MAKES
# THOSE CHANGING VARIABLES INACCESSIBLE EXTERNALLY 

############################################################################################################################

# STARTED APPLICATION TESTING BUT NOT REQUIRED FOR ASSIGNMENT BUT I'LL SHOW THAT I CAN 
# DO IT - INSTRUCTOR INSISTED NOT TO SPEND MUCH TIME ON THE TESTING PORTION. ADDITIONALLY,
# THIS TEST WOULD ESSENTIAL BE REPEATED IN SOME FASHION FOR OTHER ROUTE FUNCTIONS SO ITS
# PSUEDO-ENCOMPASING

def test_epochs():
    test_epoch_list = []
    # CONVERT JSONIFIED LIST BACK TO LIST FROM FLASK APP FOR TESTING
    with app.app_context(): 
        # READ DATA IN APP CONTEXT (READ VIA APPLICATION)
        read_data_from_file()
        # CALL EPOCHS() FUNCTION AND DECODE RESPONSE INTO STRING
        epoch_str = epochs().get_data().decode() 
        # DELIMIT RESPONSE STRING INTO LIST
        test_epoch_list = epoch_str.replace('"','').strip('][\n').split(',')
    # THEN TEST LIST 
    assert len(test_epoch_list)>0
    assert test_epoch_list[0] == '2022-042T12:00:00.000Z'
    # I TRANSFORMED TO LIST SO CHECKING THAT ITS A LIST IS UNINFORMATIVE
    # -> NO ISINSTANCE() ASSERTION


# FURTHER ROUTE FUNCTIONS NOT TESTED DUE TO TIME CONSTRAINTS AND INSTRUCTION




