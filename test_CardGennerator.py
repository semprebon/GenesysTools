import pytest

class TestCardGenerator:
    def test_format_modifier(self):
        from card_generator import format_modifier
        assert format_modifier(-10) == "-10"
        assert format_modifier(0) == "+0"
        assert format_modifier(+3) == "+3"

    def test_attribute_modifier(self):
        from card_generator import attribute_modifier
        assert attribute_modifier(1) == -5
        assert attribute_modifier(8) == -1
        assert attribute_modifier(9) == -1
        assert attribute_modifier(10) == 0
        assert attribute_modifier(13) == +1

    def test_batch_list(self):
        from card_generator import batch_list
        assert batch_list([0,1,2,3,4], 2) == [[0,1],[2,3],[4]]
        assert batch_list([0,1,2,3,4], 1) == [[0],[1],[2],[3],[4]]
        assert batch_list([0,1,2], 5) == [[0,1,2]]