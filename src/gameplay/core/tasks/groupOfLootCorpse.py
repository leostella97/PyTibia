import numpy as np
from scipy.spatial import distance
from src.features.gameWindow.typings import Creature
from src.features.radar.typings import Coordinate
from ...typings import Context
from ..factories.makeLootCorpse import makeLootCorpseTask
from ..factories.makeWalk import makeWalkTask
from ..typings import Task
from ..waypoint import generateFloorWalkpoints
from .groupTask import GroupTask


class GroupOfLootCorpseTasks(GroupTask):
    def __init__(self, context: Context, corpse: Creature):
        super().__init__()
        self.name = 'groupOfLootCorpse'
        self.tasks = self.generateTasks(context, corpse)
        self.value = corpse

    # TODO: add unit tests
    # TODO: add typings
    def generateTasks(self, context: Context, corpse: Creature):
        tasks = np.array([], dtype=Task)
        tasksToAppend = np.array([], dtype=Task)
        tasks = np.append(tasks, [tasksToAppend])
        nonWalkableCoordinates = context['cavebot']['holesOrStairs'].copy()
        for monster in context['gameWindow']['monsters']:
            monsterCoordinateTuple = (monster['coordinate'][0], monster['coordinate'][1], monster['coordinate'][2])
            coordinatesToAppend = np.array([monsterCoordinateTuple], dtype=Coordinate)
            nonWalkableCoordinates = np.append(nonWalkableCoordinates, coordinatesToAppend)
        gameWindowHeight, gameWindowWidth  = context['gameWindow']['img'].shape
        gameWindowCenter = (gameWindowWidth // 2, gameWindowHeight // 2)
        monsterGameWindowCoordinate = context['cavebot']['closestCreature']['gameWindowCoordinate']
        moduleX = abs(gameWindowCenter[0] - monsterGameWindowCoordinate[0])
        moduleY = abs(gameWindowCenter[1] - monsterGameWindowCoordinate[1])
        dist = distance.cdist([context['radar']['coordinate']], [context['cavebot']['closestCreature']['coordinate']]).flatten()[0]
        walkpoints = []
        if dist < 2:
            if moduleX > 64 or moduleY > 64:
                walkpoints.append(context['cavebot']['closestCreature']['coordinate'])
        else:
            walkpoints = generateFloorWalkpoints(
                context['radar']['coordinate'], context['cavebot']['closestCreature']['coordinate'], nonWalkableCoordinates=nonWalkableCoordinates)
            hasWalkpoints = len(walkpoints) > 0
            if hasWalkpoints:
                walkpoints.pop()
        for walkpoint in walkpoints:
            walkpointTask = makeWalkTask(context, walkpoint)
            taskToAppend = np.array([walkpointTask], dtype=Task)
            tasks = np.append(tasks, [taskToAppend])
        lootCorpseTasks = makeLootCorpseTask(corpse)
        lootCorpseTaskToAppend = np.array([lootCorpseTasks], dtype=Task)
        tasks = np.append(tasks, [lootCorpseTaskToAppend])
        return tasks
