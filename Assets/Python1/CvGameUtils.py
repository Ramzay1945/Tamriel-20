## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import GodsOfOld
import Popup as PyPopup
import PyHelpers
## Unique Civics ##
import UniqueCivics
## Unique Civics ##

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame

class CvGameUtils:
	"Miscellaneous game functions"
	def __init__(self): 
		pass
	
	def isVictoryTest(self):
		if ( gc.getGame().getElapsedGameTurns() > 10 ):
			return True
		else:
			return False

	def isVictory(self, argsList):
		eVictory = argsList[0]
		return True

	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]
		return True

	def getExtraCost(self, argsList):
		ePlayer = argsList[0]
		return 0

	def createBarbarianCities(self):
		return False
		
	def createBarbarianUnits(self):
		return False
		
	def skipResearchPopup(self,argsList):
		ePlayer = argsList[0]
		return False
		
	def showTechChooserButton(self,argsList):
		ePlayer = argsList[0]
		return True

	def getFirstRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		return TechTypes.NO_TECH

	def getSecondRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]
		return TechTypes.NO_TECH
	
	def canRazeCity(self,argsList):
		iRazingPlayer, pCity = argsList
		return True
	
	def canDeclareWar(self,argsList):
		iAttackingTeam, iDefendingTeam = argsList
		return True
	
	def skipProductionPopup(self,argsList):
		pCity = argsList[0]
		return False
		
	def showExamineCityButton(self,argsList):
		pCity = argsList[0]
		return True

	def getRecommendedUnit(self,argsList):
		pCity = argsList[0]
		return UnitTypes.NO_UNIT

	def getRecommendedBuilding(self,argsList):
		pCity = argsList[0]
		return BuildingTypes.NO_BUILDING

	def updateColoredPlots(self):
		return False

	def isActionRecommended(self,argsList):
		pUnit = argsList[0]
		iAction = argsList[1]
		return False

	def unitCannotMoveInto(self,argsList):
		ePlayer = argsList[0]		
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]
		return False

	def cannotHandleAction(self,argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]
		return False

	def canBuild(self,argsList):
		iX, iY, iBuild, iPlayer = argsList
		return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

	def cannotFoundCity(self,argsList):
		iPlayer, iPlotX, iPlotY = argsList
		return False

	def cannotSelectionListMove(self,argsList):
		pPlot = argsList[0]
		bAlt = argsList[1]
		bShift = argsList[2]
		bCtrl = argsList[3]
		return False

	def cannotSelectionListGameNetMessage(self,argsList):
		eMessage = argsList[0]
		iData2 = argsList[1]
		iData3 = argsList[2]
		iData4 = argsList[3]
		iFlags = argsList[4]
		bAlt = argsList[5]
		bShift = argsList[6]
		return False

	def cannotDoControl(self,argsList):
		eControl = argsList[0]
		return False

	def canResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def cannotResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def canDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		return False

	def cannotDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
##		return False ##
## Unique Civics ##
		return UniqueCivics.UniqueCivics().checkUniqueCivics(eCivic, ePlayer)
## Unique Civics ##
		
	def canTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		return False

	def cannotTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		return False

	def canConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		return False

	def cannotConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		return False

	def canCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def cannotCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def canMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def cannotMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def AI_chooseTech(self,argsList):
		ePlayer = argsList[0]
		bFree = argsList[1]
		return TechTypes.NO_TECH



	def AI_chooseProduction(self,argsList):
		pCity = argsList[0]
		iInquisitor = CvUtil.findInfoTypeNum( gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_INQUISITOR" )
		iOwner = pCity.getOwner( )

		if gc.getPlayer( iOwner ).getStateReligion( ) >= 0:
			if pCity.canTrain( iInquisitor, 0, 0 ):
				lUnits = PyPlayer( pPlayer.getID( ) ).getUnitList( )
				for iUnit in range( len( lUnits) ):
					# if there are any Inquisitors, don't Build one
					if pPlayer.getUnit( lUnits[ iUnit ].getID( ) ).getUnitType( ) == iInquisitor:
						return False
				if self.getRandomNumber( 2 ) == 0:
					gc.getMap( ).plot( pCity.getX( ), pCity.getY( ) ).getPlotCity( ).pushOrder( OrderTypes.ORDER_TRAIN, iInquisitor, -1, False, False, False, True )
					return True
		return False

	def AI_unitUpdate(self,argsList):
		pUnit = argsList[0]
		iOwner = pUnit.getOwner( )
		iInquisitor = CvUtil.findInfoTypeNum( gc.getUnitInfo, gc.getNumUnitInfos(), "UNIT_INQUISITOR" )
		
		if not gc.getPlayer( iOwner ).isHuman( ):
			if pUnit.getUnitType( ) == iInquisitor:
				self.doInquisitorCore_AI( pUnit )
				return True

		return False

	def AI_doWar(self,argsList):
		eTeam = argsList[0]
		return False

	def AI_doDiplo(self,argsList):
		ePlayer = argsList[0]
		return False

	def calculateScore(self,argsList):
		ePlayer = argsList[0]
		bFinal = argsList[1]
		bVictory = argsList[2]
		
		iPopulationScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getPopScore(), gc.getGame().getInitPopulation(), gc.getGame().getMaxPopulation(), gc.getDefineINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
		iLandScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getLandScore(), gc.getGame().getInitLand(), gc.getGame().getMaxLand(), gc.getDefineINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
		iTechScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getTechScore(), gc.getGame().getInitTech(), gc.getGame().getMaxTech(), gc.getDefineINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
		iWondersScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getWondersScore(), gc.getGame().getInitWonders(), gc.getGame().getMaxWonders(), gc.getDefineINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)
		return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)

	def doHolyCity(self):
		return False

	def doHolyCityTech(self,argsList):
		eTeam = argsList[0]
		ePlayer = argsList[1]
		eTech = argsList[2]
		bFirst = argsList[3]
		return False

	def doGold(self,argsList):
		ePlayer = argsList[0]
		return False

	def doResearch(self,argsList):
		ePlayer = argsList[0]
		return False

	def doGoody(self,argsList):
		ePlayer = argsList[0]
		pPlot = argsList[1]
		pUnit = argsList[2]
		return False

	def doGrowth(self,argsList):
		pCity = argsList[0]
		return False

	def doProduction(self,argsList):
		pCity = argsList[0]
		return False

	def doCulture(self,argsList):
		pCity = argsList[0]
		return False

	def doPlotCulture(self,argsList):
		pCity = argsList[0]
		bUpdate = argsList[1]
		ePlayer = argsList[2]
		iCultureRate = argsList[3]
		return False

	def doReligion(self,argsList):
		pCity = argsList[0]
		return False

	def cannotSpreadReligion(self,argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList[0]
		return False

	def doGreatPeople(self,argsList):
		pCity = argsList[0]
		return False

	def doMeltdown(self,argsList):
		pCity = argsList[0]
		return False
	
	def doReviveActivePlayer(self,argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]
		return False
	
	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot = argsList[0]
		pUnit = argsList[1]
		
		iPillageGold = 0
		iPillageGold = CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2")

		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100
		
		return iPillageGold
	
	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"
		
		pOldCity = argsList[0]
		
		iCaptureGold = 0
		
		iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")

		if (gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0):
			iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")
		
		return iCaptureGold
	
	def citiesDestroyFeatures(self,argsList):
		iX, iY= argsList
		return True
		
	def canFoundCitiesOnWater(self,argsList):
		iX, iY= argsList
		return False
		
	def doCombat(self,argsList):
		pSelectionGroup, pDestPlot = argsList
		return False

	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1 #return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system
		
		return iConscriptUnitType

	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1 # Any value besides -1 will be used
		
		return iFoundValue
		
	def canPickPlot(self, argsList):
		pPlot = argsList[0]
		return true
		
	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		iCostMod = -1 # Any value > 0 will be used
		
		return iCostMod

	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCityID)
		
		iCostMod = -1 # Any value > 0 will be used
		
		return iCostMod
		
	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList
		
		bCanUpgradeAnywhere = 0
		
		return bCanUpgradeAnywhere
		
	def getWidgetHelp(self, argsList):
		eWidgetType, iData1, iData2, bOption = argsList
##		if iData1 == 665:
##			return CyTranslator().getText("TXT_KEY_GODS_INQUISTOR_CLEANSE_MOUSE_OVER", ())		
## Civics Screen ##
		if eWidgetType == WidgetTypes.WIDGET_PYTHON:
			if iData1 == 8205 or iData1 == 8206:
				sText = CyGameTextMgr().parseCivicInfo(iData2, False, True, False)
				if gc.getCivicInfo(iData2).getUpkeep() > -1:
					sText += "\n" + gc.getUpkeepInfo(gc.getCivicInfo(iData2).getUpkeep()).getDescription()
				else:
					sText += "\n" + CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return sText
## Platypedia ##
			elif iData1 == 3333:
				SpecialistInfo = gc.getSpecialistInfo(iData2)
				szSpecialText = CyGameTextMgr().getSpecialistHelp(iData2, True)
				return CyTranslator().getText("TXT_KEY_PLATY_JOIN_CITY",(SpecialistInfo.getDescription(), szSpecialText))

			elif iData1 == 6781:
				if iData2 == -2:
					return CyTranslator().getText("TXT_KEY_PEDIA_ALL_GROUPS", ())
				elif iData2 == -1:
					return CyTranslator().getText("TXT_PEDIA_NON_COMBAT", ())
				else:
					return gc.getUnitCombatInfo(iData2).getDescription()
			elif iData1 == 6782:
				return CyGameTextMgr().parseCorporationInfo(iData2, False)
			elif iData1 == 6783:
				return CyTranslator().getText("TXT_KEY_MISC_RIVERS", ())
			elif iData1 == 6785:
				return CyGameTextMgr().getProjectHelp(iData2, False, CyCity())
			elif iData1 == 6786:
				return gc.getVictoryInfo(iData2).getDescription()
			elif iData1 == 6787:
				return gc.getProcessInfo(iData2).getDescription()
			elif iData1 == 6788:
				if iData2 == -1:
					return CyTranslator().getText("TXT_KEY_CULTURELEVEL_NONE", ())
				return gc.getRouteInfo(iData2).getDescription()
			elif iData1 == 6789:
				return gc.getTraitInfo(iData2).getDescription()
			elif iData1 == 6791:
				return gc.getCultureLevelInfo(iData2).getDescription()
			elif iData1 == 6792:
				return gc.getGameSpeedInfo(iData2).getDescription()
			elif iData1 == 6793:
				return gc.getHandicapInfo(iData2).getDescription()
			elif iData1 == 6795:
				return gc.getEraInfo(iData2).getDescription()
			elif iData1 == 6796:
				if iData2 == 999:
					return CyTranslator().getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())
				return gc.getUpkeepInfo(iData2).getDescription()
			elif iData1 == 6797:
				return gc.getWorldInfo(iData2).getDescription()
## Tech Help Text ##
			elif iData1 == 7800:
				return gc.getTechInfo(iData2).getHelp()
## Religion Widget Text##
			elif iData1 == 7869:
				return CyGameTextMgr().parseReligionInfo(iData2, False)
## Building Widget Text##
			elif iData1 == 7870:
				return CyGameTextMgr().getBuildingHelp(iData2, False, False, False, None)


		elif eWidgetType == WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC:
			for i in UniqueCivics.UniqueCivics().Civics:
				if iData1 == gc.getInfoTypeForString(i[2]):
					iGenericCivic = gc.getInfoTypeForString(i[1])
					if iGenericCivic > -1:
						return "\n" + CyTranslator().getText("TXT_KEY_REPLACES_UNIT", (gc.getCivicInfo(iGenericCivic).getDescription(),))
					break
## Civics Screen ##	
		return u""
		
	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList
		
		return -1	# Any value 0 or above will be used

	def getRandomNumber(self, int):
		return CyGame().getSorenRandNum(int, "Gods_CvGameUtils")
				
	def doInquisitorCore_AI( self, pUnit ):
		iOwner = pUnit.getOwner( )
		pOwner = gc.getPlayer( iOwner )
		iTurn = PyGame( ).getGameTurn()
		iOwnCulture = gc.getPlayer( iOwner ).getCultureHistory( iTurn )
		iStateReligion = gc.getPlayer( iOwner ).getStateReligion( )
		lCities = PyPlayer( iOwner ).getCityList( )
		lPlayers = PyGame( ).getCivPlayerList( )

		#Checks religion percents
		lReligions = [ ]
		bestReligionPercent = 0
		iBestReligion = -1
		for iReligionLoop in range(gc.getNumReligionInfos( )):
			iReligionLevel = gc.getGame().calculateReligionPercent(iReligionLoop)
			if iReligionLevel > gc.getGame().calculateReligionPercent(iStateReligion):
				lReligions.append( iReligionLoop )
			if (iReligionLoop != iStateReligion):
				religionPercent = gc.getGame().calculateReligionPercent(iReligionLoop)
				if (religionPercent > bestReligionPercent):
					bestReligionPercent = religionPercent
					iBestReligion = iReligionLoop

		#Prevent religious victory
		if bestReligionPercent >= 60:
			for iCity in range( len( lCities ) ):
				pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
				if pCity.isHasReligion( iBestReligion ):
					#Makes the unit move to the City and purge it
					if pUnit.generatePath( pCity.plot( ), 0, False, None ):
						self.doHolyCitySeekAndDestroy( pUnit, pCity )
						return

		# Should AI use inquisitor
		if iStateReligion >= 0:

			#Looks to see if the AI controls a Holy City
			for iCity in range( len( lCities ) ):
				pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
				for iReligion in range( gc.getNumReligionInfos( ) ):
					if iReligion == iStateReligion:
						if pCity.isHolyCityByType( iReligion ) or pOwner.isCivic(CvUtil.findInfoTypeNum(gc.getCivicInfo,gc.getNumCivicInfos(),'CIVIC_THEOCRACY')):

							#Checks culture levels
							lPlayerCultures = [ ]
							for iPlayerLoop in range( len( lPlayers ) ):
								iPlayer = lPlayers[ iPlayerLoop ].getID()
								iCulture = gc.getPlayer(iPlayer).getCultureHistory( iTurn )
								if iCulture >= iOwnCulture:
									lPlayerCultures.append( iPlayerLoop )
				
							if ( ( len( lPlayerCultures ) ) / ( len( lPlayers ) ) * 100 >= 33 ) and ( ( len( lReligions ) ) / ( gc.getNumReligionInfos( ) ) * 100 ) >= 33:

		
								#Looks to see if the AI controls a Holy City that is not the State Religion
								for iCity in range( len( lCities ) ):
									pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
									if pCity.isHasReligion( iStateReligion ):
										for iReligion in range( gc.getNumReligionInfos( ) ):
											if iReligion != iStateReligion:
												if pCity.isHolyCityByType( iReligion ):
													#Makes the unit move to the City and purge it
													if pUnit.generatePath( pCity.plot( ), 0, False, None ):
														self.doHolyCitySeekAndDestroy( pUnit, pCity )
														return
		
								for iCity in range( len( lCities ) ):
									pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
									if pCity.isHasReligion( iStateReligion ):
										for iReligion in range(gc.getNumReligionInfos( )):
											if iReligion != iStateReligion:
												if pCity.isHasReligion( iReligion ):
													if pUnit.generatePath( pCity.plot( ), 0, False, None ):
														self.doHolyCitySeekAndDestroy( pUnit, pCity )
														return						
								
	
	def doHolyCitySeekAndDestroy( self, pUnit, pCity ):
		Gods = CvEventInterface.getEventManager( )
		
		if pUnit.getX( ) != pCity.getX( ) or pUnit.getY( ) != pCity.getY( ):
			pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pCity.getX( ), pCity.getY( ), 0, False, True, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
		else:
			Gods.doInquisitorPersecution( pCity, pUnit )	
	
	def getExperienceNeeded(self, argsList):
		# use this function to set how much experience a unit needs
		iLevel, iOwner = argsList
		
		iExperienceNeeded = 0

		# regular epic game experience		
		iExperienceNeeded = iLevel * iLevel + 1

		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if (0 != iModifier):
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP
			
		return iExperienceNeeded
		