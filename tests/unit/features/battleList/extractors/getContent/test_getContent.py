import numpy as np
import pathlib
from src.features.battleList.extractors import getContent
from src.utils.image import loadFromRGBToGray


currentPath = pathlib.Path(__file__).parent.resolve()
screenshotImage = loadFromRGBToGray(f'{currentPath}/screenshot.png')


def test_should_return_None_when_container_top_bar_position_is_None(mocker):
    getContainerTopBarPositionSpy = mocker.patch('battleList.extractors.getContainerTopBarPosition', return_value=None)
    getContainerBottomBarPositionSpy = mocker.patch('battleList.extractors.getContainerBottomBarPosition', return_value=None)
    content = getContent(screenshotImage)
    expectedContent = None
    assert content == expectedContent
    getContainerTopBarPositionSpy.assert_called_once_with(screenshotImage)
    getContainerBottomBarPositionSpy.assert_not_called()


def test_should_return_None_when_container_bottom_bar_position_is_None(mocker):
    getContainerTopBarPositionSpy = mocker.patch('battleList.extractors.getContainerTopBarPosition', return_value=(1572, 25, 81, 13))
    getContainerBottomBarPositionSpy = mocker.patch('battleList.extractors.getContainerBottomBarPosition', return_value=None)
    content = getContent(screenshotImage)
    expectedContent = None
    assert content == expectedContent
    getContainerTopBarPositionSpy.assert_called_once_with(screenshotImage)
    # TODO: assert params
    getContainerBottomBarPositionSpy.assert_called_once()


def test_should_get_content():
    emptyContent = loadFromRGBToGray(f'{currentPath}/emptyContent.png')
    content = getContent(screenshotImage)
    assert emptyContent.shape == content.shape
    np.testing.assert_allclose(content, emptyContent, atol=1)
