from typing import Union
from src.shared.typings import GrayImage
from .locators import getLeftArrowsPosition, getRightArrowsPosition


# PERF: [0.1267358999999999, 3.899999999390502e-06]
def getCooldownsImage(screenshot: GrayImage) -> Union[GrayImage, None]:
    leftArrowsPos = getLeftArrowsPosition(screenshot)
    if leftArrowsPos is None:
        return None
    rightArrowsPos = getRightArrowsPosition(screenshot)
    if rightArrowsPos is None:
        return None
    return screenshot[leftArrowsPos[1] + 37: leftArrowsPos[1] + 37 + 22, leftArrowsPos[0]:rightArrowsPos[0]]
