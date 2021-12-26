# # Sid Meier's Civilization 4
# # Copyright Firaxis Games 2007
# # InquisitionGameUtils

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import CvGameUtils
import Popup as PyPopup
import PyHelpers
import GodsOfOld
import Inquisition

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame

# Inquisition Mod By Orion Veteran
# Modular Python to eliminate Merging

def AI_chooseProduction(argsList):
		pCity = argsList[0]
		iOwner = pCity.getOwner( )
		AIpPlayer = gc.getPlayer(iOwner)
		ExecuteUnitProduction = False

		# Inquisition Mod
		if Inquisition.InquisitorProductionConditionsCheck(iOwner):
			iStateReligion = AIpPlayer.getStateReligion()
			MyInquisitor = str(Inquisition.getReligionInquisitor(iStateReligion))
			iInquisitor = gc.getInfoTypeForString(MyInquisitor)
			iUnitToProduce = iInquisitor
			ExecuteUnitProduction = True
		# Inquisition Mod

		if ExecuteUnitProduction:
			#CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'Message 2','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
			if pCity.canTrain( iUnitToProduce, 0, 0 ):
				#if not Inquisition.hasProhibitedCivic(iOwner):
				lUnits = PyPlayer( AIpPlayer.getID( ) ).getUnitList( )
				for iUnit in range( len( lUnits) ):
					# if there are any iUnitToProduce, don't Build one
					if AIpPlayer.getUnit( lUnits[ iUnit ].getID( ) ).getUnitType( ) != iUnitToProduce:
						return False
						# 1 out of 3 chance or 33%
				if Inquisition.getRandomNumber( 2 ) == 0:
					# Makes the City produce the unit
					pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnitToProduce, -1, False, False, False, True)
					#gc.getMap( ).plot( pCity.getX( ), pCity.getY( ) ).getPlotCity( ).pushOrder( OrderTypes.ORDER_TRAIN, iUnitToProduce, -1, False, False, False, True )
					CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'Produce Unit','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
					return True

		return False

def AI_unitUpdate(argsList):
		pUnit = argsList[0]
		# Orion's Inquisition Mod
		iOwner = pUnit.getOwner( )
		AIpPlayer = gc.getPlayer(iOwner)
		iStateReligion = AIpPlayer.getStateReligion()

		if iStateReligion != -1:
			MyInquisitor = str(Inquisition.getReligionInquisitor(iStateReligion))
			iInquisitor = gc.getInfoTypeForString(MyInquisitor)

			if not gc.getPlayer( iOwner ).isHuman( ):
				if pUnit.getUnitType( ) == iInquisitor:
					Inquisition.doInquisitorCore_AI( pUnit )
					return True
		# End Inquisition Mod

		return False
	
# End Inquisition Mod









