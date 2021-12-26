# MongolCamp.py
#
# by Fierabras
# 3/22/2008

from CvPythonExtensions import *
from PyHelpers import PyPlayer
import CvUtil

# globals
gc = CyGlobalContext()

class MongolCamp :

    def __init__(self, eventManager):

        CvUtil.pyPrint("Initializing MongolCamp")
        
        self.iMongolCampSpawnChance = 16
        self.iCampNotMovedBonus = 8
        self.iHorseArcherChance = 33
        self.iKeshikChance = 33
        self.iArcherChance = 15
        self.iCampChance = 1
        self.iTrebuchetChance = 20
        self.iPlotChanceBonus = 60
        self.iMongolsID = -1
        
        eventManager.addEventHandler('GameStart', self.onGameStart)
        eventManager.addEventHandler('OnLoad', self.onLoadGame)
        eventManager.addEventHandler('BeginGameTurn', self.onBeginGameTurn)
        eventManager.addEventHandler('selectionGroupPushMission', self.onSelectionGroupPushMission)

    def initValues(self):

        self.iHorseArcherID = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_SKELETON')
        self.iKeshikID = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_SCAMP')
        self.iArcherID = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_ICE')
        self.iCampID = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_CONJURER')
        self.iTrebuchetID = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), 'UNIT_FIRE')

        self.iTechEngineeringID = CvUtil.findInfoTypeNum(gc.getTechInfo,gc.getNumTechInfos(),'TECH_CONJURATION')

        self.iPlains = CvUtil.findInfoTypeNum(gc.getTerrainInfo,gc.getNumTerrainInfos(),'TERRAIN_PLAINS')
        self.iDesert = CvUtil.findInfoTypeNum(gc.getTerrainInfo,gc.getNumTerrainInfos(),'TERRAIN_DESERT')
        self.iForest = CvUtil.findInfoTypeNum(gc.getFeatureInfo,gc.getNumFeatureInfos(),'FEATURE_FOREST')

        for iPlayer in range(gc.getMAX_PLAYERS()):
            player = gc.getPlayer(iPlayer)
            if (player.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_IMPERIAL')):
                self.iMongolsID = iPlayer

    def onGameStart(self, argsList):
        'Called at the start of the game'
        self.initValues()
    
    def onLoadGame(self, argsList):
        'Called when game is loaded'
        self.initValues()

    def onBeginGameTurn(self, argsList):
        'Called at the beginning of the end of each turn'
        iGameTurn = argsList[0]

        if (self.iMongolsID > -1):
                
            pTeam = gc.getTeam(gc.getPlayer(self.iMongolsID).getTeam())

            pPlayer = PyPlayer(self.iMongolsID)
            apUnitList = pPlayer.getUnitList()
            
            # Loop through all Mongol units
            for pUnit in apUnitList:
                if (pUnit.getUnitType() == self.iCampID):
            
                    # pUnit.NotifyEntity(MissionTypes.MISSION_FOUND)

                    # TODO: Turns since camp was last moved
                    # CURRENT: iGameTurn modulus 5

                    # iMovementBonus = 0
                    # if (self.getTurnsSinceUnitMoved(self.iMongolsID, pUnit) > 0):
                    #       iMovementBonus = self.iCampNotMovedBonus

                    iMovementBonus = iGameTurn % 5
                
                    iSpawnRand = CyGame().getSorenRandNum(99, "Camp Spawn Units")
                        
                    if (iSpawnRand < self.iMongolCampSpawnChance + iMovementBonus):
                        
                        # Determine any plot attribute bonuses for certain unit types
                        map = gc.getMap()        
                        plot = map.plot(pUnit.getX(), pUnit.getY())

                        iTerrain = plot.getTerrainType()
                        iFeature = plot.getFeatureType()
                        bHills = plot.isHills()

                        # Figure chance of each unit spawning including plot modifiers
                        iHorseArcherChance = self.iHorseArcherChance
                        iKeshikChance = self.iKeshikChance
                        iArcherChance = self.iArcherChance
                        iCampChance = self.iCampChance
                        iTrebuchetChance = 0
                        if (pTeam.isHasTech(self.iTechEngineeringID)):
                            iTrebuchetChance = self.iTrebuchetChance
                        
                        if (iTerrain == self.iPlains and iFeature != self.iForest and bHills != true):
                            iHorseArcherChance += self.iPlotChanceBonus
                        elif (iTerrain == self.iDesert and iFeature != self.iForest and bHills != true):
                            iKeshikChance += self.iPlotChanceBonus
                        if (iFeature != self.iForest and bHills == true):
                            iArcherChance += self.iPlotChanceBonus
                        if (iFeature == self.iForest and pTeam.isHasTech(self.iTechEngineeringID)):
                            iTrebuchetChance += self.iPlotChanceBonus
                        
                        # Sum together the chance of every unit being spawned from a camp
                        iTotalChance = iHorseArcherChance + iKeshikChance + iArcherChance + iCampChance + iTrebuchetChance
                        iUnitRand = CyGame().getSorenRandNum(iTotalChance, "Camp Spawn Units")

                        # Now with everything determined pick the unit
                        bPickedUnit = false
                        
                        if (bPickedUnit == false and iUnitRand < iHorseArcherChance):
                            iUnitType = self.iHorseArcherID
                            bPickedUnit = true
                        
                        if (bPickedUnit == false): iUnitRand -= iHorseArcherChance

                        if (bPickedUnit == false and iUnitRand < iKeshikChance):
                            iUnitType = self.iKeshikID
                            bPickedUnit = true
                        
                        if (bPickedUnit == false): iUnitRand -= iKeshikChance
                        
                        if (bPickedUnit == false and iUnitRand < iArcherChance):
                            iUnitType = self.iArcherID
                            bPickedUnit = true
                        
                        if (bPickedUnit == false): iUnitRand -= iArcherChance
                        
                        if (bPickedUnit == false and iUnitRand < iCampChance):
                            iUnitType = self.iCampID
                            bPickedUnit = true
                        
                        if (bPickedUnit == false): iUnitRand -= iCampChance
                        
                        if (bPickedUnit == false and iUnitRand < iTrebuchetChance and pTeam.isHasTech(self.iTechEngineeringID)):
                            iUnitType = self.iTrebuchetID

                        pPlayer.initUnit(iUnitType, plot.getX(), plot.getY(), UnitAITypes.NO_UNITAI)


    def onSelectionGroupPushMission(self, argsList):
        'selection group mission'
        eOwner = argsList[0]
        eMission = argsList[1]
        iNumUnits = argsList[2]
        listUnitIds = argsList[3]
        
        pHeadUnit = gc.getPlayer(eOwner).getUnit(listUnitIds[0])
                
        if (not pHeadUnit.isNone() and pHeadUnit.getUnitType() == CvUtil.findInfoTypeNum(gc.getUnitInfo,gc.getNumUnitInfos(),'UNIT_CONJURER')):
            
            if (eMission == MissionTypes.MISSION_SLEEP or
                eMission == MissionTypes.MISSION_SKIP or
                eMission == MissionTypes.MISSION_HEAL or
                eMission == MissionTypes.MISSION_SENTRY or
                eMission == MissionTypes.MISSION_FORTIFY):
                
                pHeadUnit.NotifyEntity(MissionTypes.MISSION_FOUND)
