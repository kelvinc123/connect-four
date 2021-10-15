'''
Name : Kelvin Christian
Github : student-KelvinChristian
'''

from chip import Chip


def test_chip_color():

    chip_1 = Chip("RED", 100)
    assert chip_1.color == "RED"
    assert chip_1.rgb == (1, 0, 0)

    chip_2 = Chip("YELLOW", 100)
    assert chip_2.color == "YELLOW"
    assert chip_2.rgb == (1, 1, 0)
