import numpy as np
import pyautogui
from src.features.radar.typings import Coordinate
from ...typings import Context
from ..factories.makeSetNextWaypoint import makeSetNextWaypointTask
from ..factories.makeWalk import makeWalkTask
from ..typings import Task
from ..waypoint import generateFloorWalkpoints
from .groupTask import GroupTask


class GroupOfWalkTasks(GroupTask):
    def __init__(self, context: Context, coordinate: Coordinate):
        super().__init__()
        self.delayAfterComplete = 1
        self.name = 'groupOfWalk'
        self.value = coordinate
        self.tasks = self.generateTasks(context, self.value)

    # TODO: add unit tests
    def generateTasks(self, context: Context, waypointCoordinate: Coordinate):
        nonWalkableCoordinates = context['cavebot']['holesOrStairs'].copy()
        for monster in context['gameWindow']['monsters']:
            monsterCoordinateTuple = (monster['coordinate'][0], monster['coordinate'][1], monster['coordinate'][2])
            coordinatesToAppend = np.array([monsterCoordinateTuple], dtype=Coordinate)
            nonWalkableCoordinates = np.append(nonWalkableCoordinates, coordinatesToAppend)
        walkpoints = generateFloorWalkpoints(
            context['radar']['coordinate'], waypointCoordinate, nonWalkableCoordinates=nonWalkableCoordinates)
        tasks = np.array([], dtype=Task)
        for walkpoint in walkpoints:
            walkpointTask = makeWalkTask(context, walkpoint)
            taskToAppend = np.array([walkpointTask], dtype=Task)
            tasks = np.append(tasks, [taskToAppend])
        tasksToAppend = np.array([
            makeSetNextWaypointTask(),
        ], dtype=Task)
        tasks = np.append(tasks, [tasksToAppend])
        return tasks

    # TODO: add unit tests
    def _ping(self, context: Context) -> Context:
        nonWalkableCoordinates = context['cavebot']['holesOrStairs'].copy()
        for monster in context['gameWindow']['monsters']:
            monsterCoordinateTuple = (monster['coordinate'][0], monster['coordinate'][1], monster['coordinate'][2])
            coordinatesToAppend = np.array([monsterCoordinateTuple], dtype=Coordinate)
            nonWalkableCoordinates = np.append(nonWalkableCoordinates, coordinatesToAppend)
        walkpoints = generateFloorWalkpoints(
            context['radar']['coordinate'], self.value, nonWalkableCoordinates=nonWalkableCoordinates)
        if len(walkpoints) == 0 and context['targeting']['hasIgnorableCreatures'] == False:
            context['targeting']['canIgnoreCreatures'] = False
            hasKeyPressed = context['lastPressedKey'] is not None
            if hasKeyPressed:
                pyautogui.keyUp(context['lastPressedKey'])
                context['lastPressedKey'] = None
                context['currentTask'] = None
        return context

    # TODO: add unit tests
    def did(self, _: Context) -> bool:
        for taskWithName in self.tasks:
            _, task = taskWithName
            if task.status != 'completed':
                return False
        return True
