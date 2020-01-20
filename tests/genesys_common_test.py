import os
import pytest
import genesys_common

def test_humanize():
    assert genesys_common.humanize("lower_case") == "Lower Case"

def test_resource_path():
    assert os.path.isfile(genesys_common.resource_path("genesys.ttf")) == True
    assert os.path.isfile(genesys_common.resource_path("badfont.ttf")) == False

def test_load_data():
    test_file = genesys_common.resource_path('test_data.yaml')
    data = genesys_common.load_data(test_file)

def test_data_filename_with_default():
    expected = os.path.join("GenesysTools","data","test_item.yaml")
    assert genesys_common.data_filename([''], default_filename = "test_item").endswith(expected)

def test_data_filename_with_missing():
    with pytest.raises(FileNotFoundError):
        genesys_common.data_filename([''], default_filename="test_item2")

def test_data_filename_with_absolute_path():
    filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources/test_data'))
    expected = os.path.join("GenesysTools","resources","test_data.yaml")
    assert genesys_common.data_filename([''], default_filename = filename).endswith(expected)

def test_data_filename_with_supplied_filename():
    expected = os.path.join("GenesysTools","data","test_item.yaml")
    assert genesys_common.data_filename(['', 'test_item']).endswith(expected)
