## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import CvTechChooser
import traceback
import os
import sys
import PyHelpers
import GodsOfOld
import pickle
import CvGameUtils
import CvEventInterface

# for C++ compatibility
false=False
true=True

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
#RELIGIOUS_TECH_MAX_RELIGIONS = {}
#bReligiousTechInitDone = False
LR_iPlayer = gc.getGame().getActivePlayer()	

# #####################################################################
# Note to Modders:  If you add a new religion to the game, then you   #
# must add one line in dReligionData to get the python to recognize   #
# the new religion.  dReligionData is now the standard location that  #
# allows you to add a new religion with ease.  No more changing       #
# multiple functions in Python.                                       #
# ##################################################################### 
dReligionData = {
		"RELIGION_AEDRA": ("BUILDING_AEDRA_SHRINE"),
	}

# #######################################
#   Begin Inquisition Functions		#				
# #######################################
	
def isOC_FOREIGN_INQUISITIONS():
	# Orion's Inquisition Mod
	return gc.getDefineINT("OC_FOREIGN_INQUISITIONS") != 0
	
def	isOC_RESPAWN_HOLY_CITIES():
	# Orion's Inquisition Mod
	return gc.getDefineINT("OC_RESPAWN_HOLY_CITIES") != 0
	
def	isOC_INQUISITOR_CAN_REMOVE_HOLY_CITY():
	# Orion's Inquisition Mod
	return gc.getDefineINT("OC_INQUISITOR_CAN_REMOVE_HOLY_CITY") != 0
	
def getReligionInquisitor(iStateReligion):
	# Orion's Inquisition Mod
	# Returns the Religion Inquisitor for the specified State Religion
		
	#for szReligion, (iMonastery, iTemple, iShrine, iHolyOffice, iMissionary, iInquisitor) in dReligionData.iteritems():
	#	iReligion = gc.getInfoTypeForString(szReligion)
	#	if iReligion == iStateReligion:
	#		break
			
	#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,str(iInquisitor),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
	#return str(iInquisitor)	
	# Deliverator - may want Religion specific Inquisitors at some stage, but for now...
	return "UNIT_INQUISITOR"

def RemoveAllNonStateReligiousBuildings(pPlayer, iStateReligion, pCity):
	# Orion's Inquisition Mod
	# Removes all non-state religious buildings from the City
	iGoldTotal = 0
	iPlayer = pPlayer.getID( )
	
	for iBuildingLoop in range(gc.getNumBuildingInfos( )):
		if pCity.isHasBuilding( iBuildingLoop ):
			pBuilding = gc.getBuildingInfo( iBuildingLoop )
			iRequiredReligion = pBuilding.getReligionType( )
			for iReligionLoop in range(gc.getNumReligionInfos()):
				if iReligionLoop != pPlayer.getStateReligion( ):
					if iRequiredReligion == iReligionLoop:
						if OCHasNonStateShrine(pPlayer, iBuildingLoop):
							# Greatly increases Anger for all AIs who share the religion of the destroyed Shrine
							AIAttitudeAdjustment(iPlayer, iRequiredReligion, -3, True)
							# Removes Building
							pCity.setNumRealBuilding ( iBuildingLoop,0 )
							# Add gold to treasury for pillaging the non-state Shrine
							iGoldTotal = iGoldTotal + 500
							CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'Destruction of a non-state Holy Shrine has angered one or more AI Civs!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(7),0,0,False,False)
							# Add code to increase shrine income
						else:											
							# Removes Building
							pCity.setNumRealBuilding ( iBuildingLoop,0 )
							# Add gold to treasury for pillaging the non-state Religious Building									
							iGoldTotal = iGoldTotal + 250
							# Increases Anger for all AIs who share the religion of a destroyed Temple, Monastery or Cathedral
							AIAttitudeAdjustment(iPlayer, iRequiredReligion, -1, False)
	
	# Total Pillage Reward
	pPlayer.changeGold(iGoldTotal)
	#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'All non-state religious buildings were removed!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)

def RemoveAllNonStateReligions(pPlayer, iStateReligion, pCity):
	# Orion's Inquisition Mod
	# Removes all non-state religions and Holy City identifier from City			
	iGoldTotal = 0
	iPlayer = pPlayer.getID( )
	
	for iReligionLoop in range(gc.getNumReligionInfos()):
		# Make sure only non-state religions are selected
		if iReligionLoop != iStateReligion:
			# Is this a non-state Holy City?
			if pCity.isHolyCityByType( iReligionLoop ):
				# Check default -- Does game option allow removal of a Holy City?
				if isOC_INQUISITOR_CAN_REMOVE_HOLY_CITY():
					# Increases Anger for all AIs who share the purged Holy City
					AIAttitudeAdjustment(iPlayer, iReligionLoop, -3, True)
					# Remove non-state Holy City identifier
					gc.getGame( ).clearHolyCity( iReligionLoop )
					# Add gold to treasury for pillaging the non-state Holy City
					iGoldTotal = iGoldTotal + 500
					# Increases Anger for all AIs who share the purged religion						
					AIAttitudeAdjustment(iPlayer, iReligionLoop, -1, False)
					# Remove non-state religion
					pCity.setHasReligion(iReligionLoop, 0, 0, 0)
					# Add gold to treasury to compensate for inquisition costs
					iGoldTotal = iGoldTotal + 100
					CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'Destruction of a non-state Holy City has angered one or more AI Civs!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(7),0,0,False,False)
					# Set Minimum of Two Cities required for Respawning a Holy City
					minCitiesForInfluence = 2
					
					# Check default -- Respawn Holy City?
					if isOC_RESPAWN_HOLY_CITIES():
						# Find player with the at least 2 Cities of religious influence to respawn the Holy City.
						eBestPlayer = getPlayerWithMaxInfluenceForReligion(iReligionLoop, minCitiesForInfluence)
						# If there is a player with enough Religious Influence for Religion
						if eBestPlayer >= 0:
							XpPlayer = gc.getPlayer(eBestPlayer)
							# Respawn the Holy City
							ReSpawnHolyCity(XpPlayer, iReligionLoop)
																		
			elif pCity.isHasReligion( iReligionLoop ):
				# Increases Anger for all AIs who share the purged religion						
				AIAttitudeAdjustment(iPlayer, iReligionLoop, -1, False)
				# Remove non-state religion
				pCity.setHasReligion(iReligionLoop, 0, 0, 0)
				# Add gold to treasury to compensate for inquisition costs						
				iGoldTotal = iGoldTotal + 100

	# Persecution succeeds
	# Total Pillage Reward
	pPlayer.changeGold(iGoldTotal)
	#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'All non-state religions were removed!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
		
def hasMatchingStateReligion(iPlayerA, iPlayerB):
	# Orion's Inquisition Mod
	#Checks for matching state religion between two players
	#Returns True if both players have the same state religion
	#Returns False if both players do not have the same state religion
	pPlayerA = gc.getPlayer(iPlayerA)
	pPlayerB = gc.getPlayer(iPlayerB)
	iStateReligionA = pPlayerA.getStateReligion()
	iStateReligionB = pPlayerB.getStateReligion()
		
	if iStateReligionA == iStateReligionB:
		return True
	
	return False

def hasOpenBordersAgreement (iPlayerA, iPlayerB):
	# Orion's Inquisition Mod
	#Check for Open Borders Agreement between two players.
	#Returns True if Open Borders Agreement Exists.
	#Returns False if Open Borders Agreement does not Exist.
	MyAgreement = False
		
	for iMyDeal in range(gc.getGame().getIndexAfterLastDeal()):
		deal = gc.getGame().getDeal(iMyDeal)
		if ((deal.getFirstPlayer() == iPlayerA and deal.getSecondPlayer() == iPlayerB) and not deal.isNone() or (deal.getSecondPlayer() == iPlayerB and deal.getFirstPlayer() == iPlayerA)) and not deal.isNone():
			for jTrade in range(deal.getLengthFirstTrades()):
				tradeData = deal.getFirstTrade(jTrade)
				if tradeData.ItemType == TradeableItems.TRADE_OPEN_BORDERS:
					MyAgreement = True
					break
						
	if MyAgreement:
		#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'Open Borders Agreement!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
		return True
	else:
		#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'No Open Borders Agreement!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
		return False

def isHoly(iCity):
	# Orion's Inquisition Mod
	HCConfirmed = False

	for iReligion in range(gc.getNumReligionInfos()):
		# Confirm City is a Holy City and get the religion
		if iCity.isHolyCityByType(iReligion):
			HCConfirmed = True
			break
	
	return HCConfirmed
	
def getHolyCityReligion(iCity):
	# Orion's Inquisition Mod	
	for iReligion in range(gc.getNumReligionInfos()):
		# Confirm City is a Holy City and get the religion
		if iCity.isHolyCityByType(iReligion):
			MyHCReligion = iReligion
			break	
	
	return MyHCReligion

def isReligionExist(iReligion):
	# Orion's Inquisition Mod
	#checks if the religion exists anywhere in the world
	#regardless of whether it has a founding holy city or not
	for rPlayer in range(gc.getMAX_PLAYERS()):
		RyPlayer = gc.getPlayer(rPlayer)
		if RyPlayer.isAlive():
			if RyPlayer.getHasReligionCount(iReligion):
				return True
				
	return False

def getBestReligion():
	# Orion's Inquisition Mod
	lReligions = [ ]
	iBestReligionPercent = 0
	iBestReligion = -1
	
	#Checks religion percents	
	for iReligionLoop in range(gc.getNumReligionInfos( )):
		iReligionPercent = gc.getGame().calculateReligionPercent(iReligionLoop)			
		lReligions.append( iReligionLoop )
		if iReligionPercent > iBestReligionPercent:
			iBestReligionPercent = iReligionPercent
			iBestReligion = iReligionLoop						

	return iBestReligion
	
def getBestReligionPercent():
	# Orion's Inquisition Mod
	lReligions = [ ]
	iBestReligionPercent = 0
		
	#Checks religion percents	
	for iReligionLoop in range(gc.getNumReligionInfos( )):
		iReligionPercent = gc.getGame().calculateReligionPercent(iReligionLoop)			
		lReligions.append( iReligionLoop )
		if iReligionPercent > iBestReligionPercent:
			iBestReligionPercent = iReligionPercent
			
	return iBestReligionPercent
	
def getPlayerWithMaxInfluenceForReligion(MyHCReligion, minCitiesRequired):
	# Orion's Inquisition Mod
	eBestPlayer = -1
	iBestCount = 0
	
	for ePlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(ePlayer)
		# skip invalid or dead players
		if not pPlayer.isNone():
			if pPlayer.isAlive():
				iCount = pPlayer.getHasReligionCount(MyHCReligion)
				if iCount > iBestCount:
					iBestCount = iCount
					eBestPlayer = ePlayer
	
	if iBestCount >= minCitiesRequired:
		return eBestPlayer
	else:
		return -1

def ocCityHasNonStateReligion(ocCity, ocStateReligion):
	# Orion's Inquisition Mod
	iCount = 0
	
	for iocReligionLoop in range(gc.getNumReligionInfos( )):
		if ocCity.isHasReligion( iocReligionLoop ):
			if iocReligionLoop != ocStateReligion:
				# Must not be a Holy City Religion - Only a non-state religion
				if not ocCity.isHolyCityByType(iocReligionLoop):
					iCount = iCount + 1  
	
	if iCount > 0:
		return True
	else:
		return False

def ReSpawnHolyCity(XpPlayer, MyHCReligion):
	# Orion's Inquisition Mod
	RHC = False
	
	# Execute Relocation of Holy City 
	for iCity in range(XpPlayer.getNumCities()):
		XpCity = XpPlayer.getCity(iCity)
		for iReligion1 in range(gc.getNumReligionInfos()):
			if MyHCReligion == iReligion1:
				if XpCity.isHasReligion(MyHCReligion):
					RHC = True
					break
												
		if RHC:
			CyGame().setHolyCity(MyHCReligion, XpCity, True)
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'A Holy City Religion has been Respawned','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
			break
					
def findCityWithXReligion(xReligion):
	# Orion's Inquisition Mod
	MyXCityCount = 0
	FoundReligion = False
		
	for iPlayer in range(gc.getMAX_PLAYERS()):		
		pPlayer = gc.getPlayer(iPlayer)				
		if pPlayer.isAlive() and not pPlayer.isBarbarian():
			lCities = PyHelpers.PyPlayer(iPlayer).getCityList()
			for iCity in range( len( lCities ) ):				
				pCity = pPlayer.getCity( lCities[ iCity ].getID( ) )
				for iReligionX in range(gc.getNumReligionInfos()):
					if iReligionX == xReligion: 						
						if pCity.isHasReligion(xReligion):
							if not pCity.isHolyCityByType(xReligion):
								MyXCityCount = MyXCityCount + 1
								FoundReligion = True
								break
						
		if MyXCityCount > 0:		
			break
							
	if not FoundReligion:	
		#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'False!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
		return False
	else:	
		#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'True!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
		return True

def OCHasNonStateShrine(Player, iBuilding):
	# Orion's Inquisition Mod
	iStateReligion = Player.getStateReligion()
	FoundNonStateShrine = False
		
	for szReligion, (iShrine) in dReligionData.iteritems():
		iReligion = gc.getInfoTypeForString(szReligion)
		if iReligion != iStateReligion:		
			if iBuilding == gc.getInfoTypeForString(iShrine):
				FoundNonStateShrine = True
				break

	return FoundNonStateShrine

def AIAttitudeAdjustment(iPlayer, iRequiredReligion, intAdjustment, bDeclareWar):
	# Orion's Inquisition Mod
	# Increases anger for Civs who share the religion purged. 
	# Friendly: 10 or above; Pleased: 3 to 9; Cautious: -2 to 2; Annoyed: -9 to -3; Furious: -10 and below
	# AI Civs who share the religion purged, will declare war if Holy City or Religious Shrine is destroyed 
	eCivicTypeReligion = gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT')
	eCivicTheocracy = gc.getInfoTypeForString('CIVIC_THEOCRACY')
	CvRunTheocracyDeclaredWarMsg = False
		
	for AIiPlayer in range(gc.getMAX_PLAYERS()):
		if AIiPlayer != iPlayer:
			AIpPlayer = gc.getPlayer(AIiPlayer)
			if not AIpPlayer.isNone() and not AIpPlayer.isBarbarian() and not AIpPlayer.isHuman( ) and AIpPlayer.isAlive():
				if AIpPlayer.getStateReligion( ) == iRequiredReligion:
					PyPlayer(AIiPlayer).AI_changeAttitude( iPlayer, intAdjustment )
					
					if bDeclareWar == 1:
						# Does the AI Civ have the Theocracy Civic ***********
						if AIpPlayer.getCivics(eCivicTypeReligion) == eCivicTheocracy:
							AIpPlayerTeam =	gc.getTeam(AIpPlayer.getTeam())
							if (not AIpPlayerTeam.isAtWar(iPlayer)):
								# -3 Attitude adjustments means a Holy City and/or a Shrine is being destroyed.
								if intAdjustment == -3:
									# Declare total war
									AIpPlayerTeam.declareWar(iPlayer, false, WarPlanTypes.WARPLAN_TOTAL)
									CvRunTheocracyDeclaredWarMsg = True
								
								elif intAdjustment == -7:
									# Declare Limited war
									AIpPlayerTeam.declareWar(iPlayer, false, WarPlanTypes.WARPLAN_LIMITED)
								
	if CvRunTheocracyDeclaredWarMsg:
		# iPlayer is the Civ who destroyed the Holy City
		# iRequiredReligion is the state religion of the Holy City
		CyMessageControl().sendModNetMessage(200, iPlayer, iRequiredReligion, -1, -1)
		
	return

def doInquisitorPersecution( pCity, pUnit ):
	# Orion's Inquisition Mod
	pPlayer = gc.getPlayer( pCity.getOwner( ) )
	iPlayer = pPlayer.getID( )
	iStateReligion = pPlayer.getStateReligion( )
	iHC = 0
	
	# gets a list of all religions in the city except state religion
	CyInterface().playGeneralSound("AS3D_UN_CHRIST_MISSIONARY_ACTIVATE")
	lCityReligions = [ ]
	for iReligionLoop in range(gc.getNumReligionInfos( )):
		if pCity.isHasReligion( iReligionLoop ):
			if iStateReligion != iReligionLoop:
				lCityReligions.append( iReligionLoop )
				iHC = 0
				if pCity.isHolyCityByType(iReligionLoop):
					iHC = -50
			else:
				if pCity.isHolyCityByType(iReligionLoop):
					iHC = 10
	
	# Does Persecution succeed
	irandom = gc.getGame().getSorenRandNum(100,"")
	if irandom < 95 - ((len( lCityReligions ))*5) + iHC:
		
		# Removes all non-state Religious Buildings from the City
		RemoveAllNonStateReligiousBuildings(pPlayer, iStateReligion, pCity)
		# Remove Non-State Religions from City
		RemoveAllNonStateReligions(pPlayer, iStateReligion, pCity)
		CyInterface().addMessage(CyGame().getActivePlayer(),False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION",(pCity.getName(),)),"AS2D_PLAGUE",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
					
	else:
		# Persecution fails
		CyInterface().addMessage(CyGame().getActivePlayer(),False,25,CyTranslator().getText("TXT_KEY_MESSAGE_INQUISITION_FAIL",(pCity.getName(),)),"AS2D_SABOTAGE",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
		
	# Unit expended
	pUnit.kill( 0, -1 )
	
def getRandomNumber(int):
	# Orion's Inquisition Mod ????????
	return CyGame().getSorenRandNum(int, "Gods_CvGameUtils")
	
def doInquisitorCore_AI( pUnit ):
	# Orion's Inquisition Mod
	iOwner = pUnit.getOwner( )
	iStateReligion = gc.getPlayer( iOwner ).getStateReligion( )
	lCities = PyPlayer( iOwner ).getCityList( )		

	#Looks to see if the AI controls a City that has a non-State Religion
	for iCity in range( len( lCities ) ):
		for iReligion in range( gc.getNumReligionInfos( ) ):
			if iReligion != iStateReligion:
				pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
				if pCity.isHasReligion( iReligion ) and pCity.isHasReligion( iStateReligion ):
					if not pCity.isHolyCityByType( iReligion ):
						#Makes the unit move to the City and purge it
						if pUnit.generatePath( pCity.plot( ), 0, False, None ):
							doHolyCitySeekAndDestroy( pUnit, pCity )
							return
		
	#Looks to see if the AI controls a Holy City that is not the State Religion
	for iCity in range( len( lCities ) ):
		for iReligion in range( gc.getNumReligionInfos( ) ):
			if iReligion != iStateReligion:
				pCity = gc.getPlayer( iOwner ).getCity( lCities[ iCity ].getID( ) )
				if pCity.isHolyCityByType( iReligion ) and pCity.isHasReligion( iStateReligion ):
					# Verify option for Inquisitors to remove a non-state Holy City
					if isOC_INQUISITOR_CAN_REMOVE_HOLY_CITY():
						#Makes the unit move to the City and purge it
						if pUnit.generatePath( pCity.plot( ), 0, False, None ):
							doHolyCitySeekAndDestroy(pUnit, pCity)
							return
							
def doHolyCitySeekAndDestroy(pUnit, pCity ):
	# Orion's Inquisition Mod
	if isInquisitionConditions(pCity.getOwner()):
		if pUnit.getX( ) != pCity.getX( ) or pUnit.getY( ) != pCity.getY( ):
			pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pCity.getX( ), pCity.getY( ), 0, False, True, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
		else:
			doInquisitorPersecution(pCity, pUnit)

def isInquisitionConditions(playerID):
	# Orion's Inquisition Mod
	# These are conditions which prevent an inquisition
	pPlayer = gc.getPlayer(playerID)

	if not gc.getTeam(pPlayer.getTeam()).isHasTech(gc.getInfoTypeForString('TECH_DIVINE_MANDATE')):
		return False

	# If player does not have a State Religion
	if pPlayer.getStateReligion( ) < 0:
		return False

	# If Player has one of the prohibited Civics	
	if hasProhibitedCivic(playerID):
		return False

	return True

def hasProhibitedCivic(playerID):
	# Orion's Inquisition Mod
	# Returns True if the player has a prohibited Civic
	# Returns False if the player does not have a prohibited Civic
	pPlayer = gc.getPlayer(playerID)
	bFoundProhibitedCivic = False
#	lProhibitedCivics = [
#		"CIVIC_PAGANISM",
#		"CIVIC_PACIFISM",
#		"CIVIC_FREE_RELIGION"
#	]
	lProhibitedCivics = []
	
	for iCivic in range( len( lProhibitedCivics ) ):
		MyCivic = str(lProhibitedCivics[iCivic])
		if (pPlayer.isCivic(gc.getInfoTypeForString(MyCivic))):
			bFoundProhibitedCivic = True
			#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'Found Probibited Civic!','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
			break
			
	return bFoundProhibitedCivic
		
def showInquisitionButton(pUnit):
	# Orion's Inquisition Mod
	pUnitOwner = gc.getPlayer(pUnit.getOwner())
	iStateReligion = pUnitOwner.getStateReligion()
	iUnitType = pUnit.getUnitType()
	ProceedWithInquisition = False
	zShowButton = False

	if iStateReligion != -1 :
	
		MyXInquisitor = str(getReligionInquisitor(iStateReligion))
		InquisitorType = CvUtil.findInfoTypeNum(gc.getUnitInfo, gc.getNumUnitInfos(), MyXInquisitor)

		if iUnitType == InquisitorType:
			# Need to find a better way to fix the next line
			#pUnit.setUnitAIType(UnitAITypes.UNITAI_UNKNOWN)
			pCity = gc.getMap().plot( pUnit.getX(), pUnit.getY() ).getPlotCity()
			pCityPlayer = gc.getPlayer(pCity.getOwner())
			if ( pCity.getOwner( ) == pUnit.getOwner( ) ) or ( gc.getTeam( pCityPlayer.getTeam( ) ).isVassal( gc.getPlayer( pUnit. getOwner( ) ).getTeam( ) ) ): 
				ProceedWithInquisition = True
			elif isOC_FOREIGN_INQUISITIONS():
				#Foriegn Inquisition Check
				if (pCity.getOwner() != pUnit.getOwner()):
					iPlayerA = pUnit.getOwner( )
					iPlayerB = pCity.getOwner( )
					if hasOpenBordersAgreement(iPlayerA, iPlayerB):
						if hasMatchingStateReligion(iPlayerA, iPlayerB):
							ProceedWithInquisition = True
							
			if ProceedWithInquisition:
				#if pCity.isHasReligion(iStateReligion):
					for iReligionLoop in range(gc.getNumReligionInfos( )):
						if pCity.isHasReligion(iReligionLoop):
							if iReligionLoop != iStateReligion:
								# If game option prevents Inquisition of Holy City.
								if not isOC_INQUISITOR_CAN_REMOVE_HOLY_CITY():
									# Does City Have one or more non-state religions that are not Holy City religions
									if ocCityHasNonStateReligion(pCity, iStateReligion):
										zShowButton = True
								elif isOC_INQUISITOR_CAN_REMOVE_HOLY_CITY():
									zShowButton = True

	return zShowButton
	
def TheocracyHolyWaronClickedCallback(argsList):
	# Orion's Inquisition Mod
	iButtonId = argsList[0]
	iData1 = argsList[1]
	iData2 = argsList[2]
	iData3 = argsList[3]
	iData4 = argsList[4]
	szText = argsList[5]
	bOption1 = argsList[6]
	bOption2 = argsList[7]
		
	if iButtonId == 0:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("Together we shall strike back at the infidel who desecrated our Holy City!",()))
		popupInfo.addPythonButton(CyTranslator().getText("Let the crusade begin!", ()), "")
		popupInfo.addPopup(CyGame().getActivePlayer())
		# Execute AI change in Attitude + 7
		AIAttitudeAdjustment(iData1, iData2, +7, False)		
		
	elif iButtonId == 1:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
		popupInfo.setText(CyTranslator().getText("You shall pay the price for betraying our religious faith. We are now at WAR!",()))
		popupInfo.addPythonButton(CyTranslator().getText("So be it!", ()), "")
		popupInfo.addPopup(CyGame().getActivePlayer())
		# Execute AI change in Attitude - 7 and delare war
		AIAttitudeAdjustment(iData1, iData2, -7, True)	
	
def setLR_Player(bPlayer):
	# Orion's Inquisition Mod
	global LR_Player

def getCityCountReligion(zReligion, pPlayer):
	# Orion's Inquisition Mod
	iCityCount = 0
	
	for iCity in range( len( lCities ) ):
		pCity = pPlayer.getCity(iCity)		
		if pCity.isHasReligion(iCity):
			iCityCount = iCityCount + 1

	return iCityCount
	
def InquisitorProductionConditionsCheck(iPlayer):
		# Orion's Inquisition Mod
		AIpPlayer = gc.getPlayer(iPlayer)
		iStateReligion = AIpPlayer.getStateReligion()
		
		if iStateReligion == -1:
			iStateReligionPercent = -1
		else:
			iStateReligionPercent = gc.getGame().calculateReligionPercent(iStateReligion)
			BestReligionPercent = getBestReligionPercent()
			
			if iStateReligion >= 0 or iBestReligionPercent >= 60:
				return True
		
		return False
# ###################################################################################################################
	
def isOC_FOREIGN_INQUISITIONS():
	# Orion's Inquisition Mod
	return gc.getDefineINT("OC_FOREIGN_INQUISITIONS") != 0
	
def	isOC_RESPAWN_HOLY_CITIES():
	# Orion's Inquisition Mod
	return gc.getDefineINT("OC_RESPAWN_HOLY_CITIES") != 0
	
def	isOC_INQUISITOR_CAN_REMOVE_HOLY_CITY():
	# Orion's Inquisition Mod
	return gc.getDefineINT("OC_INQUISITOR_CAN_REMOVE_HOLY_CITY") != 0
	
def DisplayOCCStatus(iPlayer):
	return
	# Limited Religions & Orions Inquisition Mod
	# Runs the popup Menus for the Game Options
	popupInfo = CyPopupInfo()
	popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
	
	szText = CyTranslator().getText("TXT_KEY_OCC_TEXT", ())
	szText += "\n\n"
	szGreenText = CyTranslator().getColorText("On\n", (), gc.getInfoTypeForString("COLOR_GREEN"))
	szRedText = CyTranslator().getColorText("Off\n", (), gc.getInfoTypeForString("COLOR_RED"))
	
	# Inquisition Mod
	if isOC_FOREIGN_INQUISITIONS():
		szText += "FOREIGN INQUISITIONS: " + szGreenText
	else:
		szText += "FOREIGN INQUISITIONS: " + szRedText
		
	if isOC_RESPAWN_HOLY_CITIES():
		szText += "RESPAWN HOLY CITIES: " + szGreenText
	else:
		szText += "RESPAWN HOLY CITIES: " + szRedText
		
	if isOC_INQUISITOR_CAN_REMOVE_HOLY_CITY():
		szText += "INQUISITOR CAN REMOVE HOLY CITY: " + szGreenText
	else:
		szText += "INQUISITOR CAN REMOVE HOLY CITY: " + szRedText
	# Inquisition Mod
	
	popupInfo.setText(szText)
	popupInfo.addPythonButton(CyTranslator().getText("OK", ()), "")
	popupInfo.addPopup(iPlayer)
	
	return
# End Orion's Inquisition Mod Functions
