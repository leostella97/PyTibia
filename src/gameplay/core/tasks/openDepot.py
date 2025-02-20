import pyautogui
from src.features.inventory.core import images
from src.utils.core import locate
from ...typings import Context
from .baseTask import BaseTask


class OpenDepotTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.delayBeforeStart = 1
        self.delayAfterComplete = 1
        self.name = 'openDepot'

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        depotPosition = locate(context['screenshot'], images['slots']['depot'])
        pyautogui.rightClick(depotPosition[0] + 5, depotPosition[1] + 5)
        return context

    # TODO: add unit tests
    # TODO: check if depot is opened
    def did(self, context: Context) -> bool:
        return True
