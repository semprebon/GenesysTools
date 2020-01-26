import os
from os import path

import pytest
import genesys_common
from genesys_common import resource_path

# humanize
def test_humanize():
    assert genesys_common.humanize("lower_case") == "Lower Case"

# resource_path

def test_resource_path_for_package_resource():
    assert path.isfile(resource_path("genesys.ttf")) == True

def test_resource_path_for_local_resource():
    assert os.path.isfile(resource_path("test_item.yaml", __file__)) == True

def test_resource_path_with_bad_resource():
    with pytest.raises(FileNotFoundError):
        os.path.isfile(resource_path("badfont.ttf"))

def test_resource_path_with_implied_ext():
    assert path.isfile(resource_path("BadaarSetting", ext="yaml", directory="data")) == True

def test_resource_path_for_full_pathname():
    assert resource_path(__file__) == __file__

# batch_list

def test_batch_list():
    from genesys_common import batch_list
    assert batch_list([0, 1, 2, 3, 4], 2) == [[0, 1], [2, 3], [4]]
    assert batch_list([0, 1, 2, 3, 4], 1) == [[0], [1], [2], [3], [4]]
    assert batch_list([0, 1, 2], 5) == [[0, 1, 2]]

# load_data

def test_load_data_for_single_item_file():
    data = genesys_common.load_data('test_item.yaml', root=__file__, directory="resources")
    assert len(data) == 1
    assert data[0]["name"] == "Rock"

def test_load_data_for_multiple_items():
    data = genesys_common.load_data(['test_items', 'test_minion.yaml'], root=__file__, directory="resources")
    assert len(data) == 3
    assert data[0]["name"] == "Rock"
    assert data[1]["name"] == "Stick"
    assert data[2]["name"] == "Undead Skeleton"

def test_format_modifier():
    assert genesys_common.format_modifier(-10) == "-10"
    assert genesys_common.format_modifier(0) == "+0"
    assert genesys_common.format_modifier(+3) == "+3"

