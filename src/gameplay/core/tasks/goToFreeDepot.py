import numpy as np
from scipy.spatial import distance
from src.features.battleList.typings import CreatureList
from src.shared.typings import Coordinate, CoordinateList, Waypoint
from src.wiki.cities import cities
from ...typings import Context
from ..factories.makeWalk import makeWalkTask
from ..typings import Task
from ..waypoint import generateFloorWalkpoints
from .groupTask import GroupTask


class GoToFreeDepotTask(GroupTask):
    def __init__(self, context: Context, waypoint: Waypoint):
        super().__init__()
        self.didTask = False
        self.name = 'goToFreeDepot'
        self.closestFreeDepotCoordinate = None
        self.terminable = False
        self.value = waypoint
        self.state = 'findingVisibleCoordinates'
        self.tasks = self.makeTasks(context, waypoint)
        self.visitedOrBusyCoordinates = {}

    # TODO: add unit tests
    # TODO: add typings
    def makeTasks(self, context: Context, waypoint: Waypoint):
        city = waypoint['options']['city']
        depotCoordinates = cities[city]['depotCoordinates']
        coordinate = context['radar']['coordinate']
        visibleDepotCoordinates = self.getVisibleDepotCoordinates(coordinate, depotCoordinates)
        if len(visibleDepotCoordinates) > 0:
            self.state = 'walkingIntoFreeDepot'
            battleListPlayers = context['gameWindow']['players']
            freeDepotCoordinates = self.getFreeDepotCoordinates(battleListPlayers, visibleDepotCoordinates)
            hasNoFreeDepotCoordinates = len(freeDepotCoordinates) == 0
            if hasNoFreeDepotCoordinates:
                self.state = 'walkingIntoVisibleCoordinates'
                for visibleDepotCoordinate in visibleDepotCoordinates:
                    self.visitedOrBusyCoordinates[tuple(visibleDepotCoordinate)] = True
                return np.array([], dtype=Task)
            freeDepotCoordinatesDistances = distance.cdist([coordinate], freeDepotCoordinates, 'euclidean').flatten()
            closestFreeDepotCoordinateIndex = np.argmin(freeDepotCoordinatesDistances)
            closestFreeDepotCoordinate = freeDepotCoordinates[closestFreeDepotCoordinateIndex]
            self.closestFreeDepotCoordinate = closestFreeDepotCoordinate
            walkpoints = generateFloorWalkpoints(coordinate, closestFreeDepotCoordinate, nonWalkableCoordinates=None)
            return np.array([makeWalkTask(context, walkpoint) for walkpoint in walkpoints], dtype=Task)
        else:
            self.state = 'walkingIntoVisibleCoordinates'
            # - gerar caminho até visualizar os próximos depots se necessário
        # -- Se sim
        # --- gerar caminho até a coordenada. Ficar pingando para verificar se alguem entra nesse tempo, cancela e calcula novamente.
        # -- Se não
        # - marcar as coordenadas atuais como ocupadas
        # - começar de novo
        # Observação: ao saber que todas as coordenadas estão ocupadas, marcar todas como não ocupadas, parar o boneco e ficar verificando se sai ou alguem, ou se começa o novo tempo de ronda
        return []

    # TODO: add unit tests
    def getFreeDepotCoordinates(self, battleListPlayers: CreatureList, visibleDepotCoordinates: CoordinateList) -> CoordinateList:
        hasNoPlayers = len(battleListPlayers) == 0
        if hasNoPlayers:
            return visibleDepotCoordinates
        battleListPlayersCoordinates = [playerCoordinate for playerCoordinate in battleListPlayers['coordinate'].tolist()]
        delta = set(map(tuple, battleListPlayersCoordinates))
        freeDepotCoordinates = np.array([x for x in visibleDepotCoordinates if tuple(x) not in delta])
        return freeDepotCoordinates

    # TODO: add unit tests
    def getVisibleDepotCoordinates(self, coordinate: Coordinate, depotCoordinates: CoordinateList) -> CoordinateList:
        visibleDepotCoordinates = []
        for depotCoordinate in depotCoordinates:
            if depotCoordinate[0] >= (coordinate[0] - 7) and depotCoordinate[0] <= (coordinate[0] + 7) and depotCoordinate[1] >= (coordinate[1] - 5) and depotCoordinate[1] <= (coordinate[1] + 5):
                visibleDepotCoordinates.append(depotCoordinate)
        return visibleDepotCoordinates

    # TODO: add unit tests
    def ping(self, context: Context) -> Context:
        if self.closestFreeDepotCoordinate is None:
            return context
        if self.state == 'walkingIntoFreeDepot' and context['radar']['coordinate'][0] == self.closestFreeDepotCoordinate[0] and context['radar']['coordinate'][1] == self.closestFreeDepotCoordinate[1]:
            self.terminable = True
            city = self.value['options']['city']
            closestFreeDepotCoordinateAsTuple = tuple(self.closestFreeDepotCoordinate)
            context['deposit']['lockerCoordinate'] = cities[city]['depotGoalCoordinates'][closestFreeDepotCoordinateAsTuple]
        return context
