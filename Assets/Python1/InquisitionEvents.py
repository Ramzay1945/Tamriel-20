# Sid Meier's Civilization 4
# Copyright Firaxis Games 2007
# InquisitionEvents
# Inquisition Mod By Orion Veteran
# Modular python project to eliminate or reduce merging tasks 

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser
# Inquisition Mod
import pickle
import Inquisition
# Inquisition Mod

# globals
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
# Inquisition Mod
game = CyGame()
# Inquisition Mod

class InquisitionEvents:
	def __init__(self, eventMgr):
# ###############################################################################
#		Important!!!!															#
#		Each function added from CvEventManager.py must be initialized here 	#
# ###############################################################################
		self.__LOG_TECH = 0
		self.eventMgr = eventMgr
		eventMgr.addEventHandler("ModNetMessage", self.onModNetMessage)
		eventMgr.addEventHandler("GameStart", self.onGameStart)	
		eventMgr.addEventHandler("cityRazed", self.onCityRazed)
											
	def onModNetMessage(self, argsList):
		'Called whenever CyMessageControl().sendModNetMessage() is called - this is all for you modders!'
		
		iData1, iData2, iData3, iData4, iData5 = argsList
		
		print("Modder's net message!")
		
		CvUtil.pyPrint( 'onModNetMessage' )
# Inquisition Mod
		iMessageID = iData1
		
		#Inquisitor's Effect on a City
		if iMessageID == 691:
			
			iPlotX = iData2
			iPlotY = iData3
			iOwner = iData4
			iUnitID = iData5
			
			pPlot = CyMap( ).plot( iPlotX, iPlotY )
			pCity = pPlot.getPlotCity( )
			pPlayer = gc.getPlayer( iOwner )
			pUnit = pPlayer.getUnit( iUnitID )
			
			Inquisition.doInquisitorPersecution( pCity, pUnit )
			
		if iData1 == 200:
			iHPlayer = gc.getGame().getActivePlayer()
			iPlayer = iData2
			#iStateReligion = gc.getPlayer(iPlayer).getStateReligion()
			if iHPlayer != iData2:
				if iHPlayer.isHuman():
					# Get the state religion of the Human Player - Theocracy
					iHStateReligion = gc.getPlayer(iHPlayer).getStateReligion()
					if iHStateReligion == iData3:
						popupInfo = CyPopupInfo()
						popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON)
						popupInfo.setData1(iHPlayer)
						popupInfo.setData2(iHStateReligion)
						popupInfo.setText(CyTranslator().getText("Godless infadels have destroyed our Holy City.  Will you stand with your brothers in faith and declare war against the infidel? WARNING! Failure to declare war will result in a state of war between you and any AI player that has theocracy Civic and shares your state religion",()))
						popupInfo.setOnClickedPythonCallback("TheocracyHolyWaronClickedCallback")
						popupInfo.addPythonButton(CyTranslator().getText("Yes, Declare War!", ()), "")
						popupInfo.addPythonButton(CyTranslator().getText("No, I will not Declare War!", ()), "")
						popupInfo.addPopup(iHPlayer)
					
# End Inquisition Mod

	def onGameStart(self, argsList):
		# Limited Religions
		'Called at the start of the game'
# ###############################################
#            Orion's Game Options Status
# ###############################################
		iPlayerNum = 0
		iHumanCount = 0
		
		if (gc.getGame().getGameTurnYear() == gc.getDefineINT("START_YEAR") and not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START)):
			for iPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if player.isAlive():
					iPlayerNum = iPlayerNum + 1
					if player.isHuman():
						iHumanCount = iHumanCount + 1
						if iHumanCount == 1:
							# Orion's Game Options Status Popup
							Inquisition.DisplayOCCStatus(iPlayer)
							break
# End Orion's Game Options Status popup

		else:
			CyInterface().setSoundSelectionReady(true)

		if gc.getGame().isPbem():
			for iPlayer in range(gc.getMAX_PLAYERS()):
				player = gc.getPlayer(iPlayer)
				if (player.isAlive() and player.isHuman()):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_DETAILS)
					popupInfo.setOption1(true)
					popupInfo.addPopup(iPlayer)

		CvAdvisorUtils.resetNoLiberateCities()
	
	def onCityRazed(self, argsList):
		'City Razed'
		city, iPlayer = argsList
		iOwner = city.findHighestCulture()
# Inquisition Mod
		pPlayer = gc.getPlayer(iPlayer)
		iStateReligion = pPlayer.getStateReligion()
		
		# Removes all non-state Religious Buildings from the City
		Inquisition.RemoveAllNonStateReligiousBuildings(pPlayer, iStateReligion, city)
		# Remove all Non-State Religions from City
		Inquisition.RemoveAllNonStateReligions(pPlayer, iStateReligion, city)
# End Inquisition Mod
		CvUtil.pyPrint("City Razed Event: %s" %(city.getName(),))
# End Inquisition Mod
