import numpy as np
from src.features.battleList.core import getCreatures
from src.features.battleList.typings import Creature


def test_should_return_an_empty_array_when_filled_slots_count_is_zero(mocker):
    getFilledSlotsCountSpy = mocker.patch('battleList.core.getFilledSlotsCount', return_value=0)
    getBeingAttackedCreaturesSpy = mocker.patch('battleList.core.getBeingAttackedCreatures')
    getCreaturesNamesSpy = mocker.patch('battleList.core.getCreaturesNames')
    content = np.array([], dtype=np.uint8)
    creatures = getCreatures(content)
    expectedCreatures = np.array([], dtype=Creature)
    np.testing.assert_array_equal(creatures, expectedCreatures)
    getFilledSlotsCountSpy.assert_called_once_with(content)
    getBeingAttackedCreaturesSpy.assert_not_called()
    getCreaturesNamesSpy.assert_not_called()


def test_should_return_an_array_of_creatures_when_filled_slots_count_is_greater_than_zero(mocker):
    creature = ('Rat', True)
    getFilledSlotsCountSpy = mocker.patch('battleList.core.getFilledSlotsCount', return_value=1)
    getBeingAttackedCreaturesSpy = mocker.patch('battleList.core.getBeingAttackedCreatures', return_value=[True])
    getCreaturesNamesSpy = mocker.patch('battleList.core.getCreaturesNames', return_value=['Rat'])
    content = np.array([], dtype=np.uint8)
    creatures = getCreatures(content)
    expectedCreatures = np.array([creature], dtype=Creature)
    np.testing.assert_array_equal(creatures, expectedCreatures)
    getFilledSlotsCountSpy.assert_called_once_with(content)
    getBeingAttackedCreaturesSpy.assert_called_once_with(content, 1)
    getCreaturesNamesSpy.assert_called_once_with(content, 1)
