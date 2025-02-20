import numpy as np
import pyautogui
from ...typings import Context
# from src.features.gameWindow.core import getSlotFromCoordinate
from src.features.gameWindow.slot import rightClickSlot
from src.features.gameWindow.typings import Creature
from .baseTask import BaseTask


# TODO: check if something was looted or exactly count was looted
class LootCorpseTask(BaseTask):
    def __init__(self, creature: Creature):
        super().__init__()
        self.delayBeforeStart = 0.25
        self.delayAfterComplete = 0.25
        self.name = 'lootCorpse'
        self.value = creature

    # TODO: add unit tests
    def do(self, context: Context) -> Context:
        # slot = getSlotFromCoordinate(
        #     context['radar']['coordinate'], self.value['coordinate'])
        # pyautogui.keyDown('shift')
        # rightClickSlot(slot, context['gameWindow']['coordinate'])
        pyautogui.keyDown('shift')
        rightClickSlot([6, 4], context['gameWindow']['coordinate'])
        rightClickSlot([7, 4], context['gameWindow']['coordinate'])
        rightClickSlot([8, 4], context['gameWindow']['coordinate'])
        rightClickSlot([6, 5], context['gameWindow']['coordinate'])
        rightClickSlot([7, 5], context['gameWindow']['coordinate'])
        rightClickSlot([8, 5], context['gameWindow']['coordinate'])
        rightClickSlot([6, 6], context['gameWindow']['coordinate'])
        rightClickSlot([7, 6], context['gameWindow']['coordinate'])
        rightClickSlot([8, 6], context['gameWindow']['coordinate'])
        pyautogui.keyUp('shift')
        return context

    # TODO: add unit tests
    def onDidComplete(self, context: Context) -> Context:
        creatureToLoot = context['corpsesToLoot'][0]
        indexesToDelete = []
        for index, corpseToLoot in enumerate(context['corpsesToLoot']):
            coordinateDidMatch = creatureToLoot['coordinate'][0] == corpseToLoot['coordinate'][0] and creatureToLoot['coordinate'][1] == corpseToLoot['coordinate'][1] and creatureToLoot['coordinate'][2] == corpseToLoot['coordinate'][2]
            if coordinateDidMatch:
                indexesToDelete.append(index)
        context['corpsesToLoot'] = np.delete(context['corpsesToLoot'], indexesToDelete)
        return context
