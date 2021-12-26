## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import PyHelpers
import CvUtil
import ScreenInput
import CvScreenEnums

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()

## Civ4 Religion screen as adapted by johny smith (scrolling bar for more than 7 religions)
## Revisited by isenchine: added a list of other players' cities with or without selected religion (February 2015)
##johny smith start##
class CvReligionScreen:
	"Religion Advisor Screen"

	def __init__(self):
		
		# original Civ4 settings commented out when replaced or not used
		self.SCREEN_NAME = "ReligionScreen"
		self.BUTTON_NAME = "ReligionScreenButton"
		self.RELIGION_NAME = "ReligionText"
		self.CONVERT_NAME = "ReligionConvertButton"
		self.CANCEL_NAME = "ReligionCancelButton"
		# self.CITY_NAME = "ReligionCity" # not used
		# self.HEADER_NAME = "ReligionScreenHeader"
		self.DEBUG_DROPDOWN_ID =  "ReligionDropdownWidget"
		self.AREA1_ID =  "ReligionAreaWidget1"
		self.AREA2_ID =  "ReligionAreaWidget2"
		self.BACKGROUND_ID = "ReligionBackground"
		# self.RELIGION_PANEL_ID = "ReligionPanel"
		self.RELIGION_ANARCHY_WIDGET = "ReligionAnarchyWidget"
		
		# self.BORDER_WIDTH = 2 # not used
		self.BUTTON_SIZE = 48
		# self.HIGHLIGHT_EXTRA_SIZE = 4 # not used
		
		# self.X_SCREEN = 500 # not used
		# self.Y_SCREEN = 396 # not used
		self.W_SCREEN = 1024 #1024 # can be changed in def interfaceScreen
		self.H_SCREEN = 768 #768 # can be changed in def interfaceScreen
		# self.Z_SCREEN = -6.1 # not used
		
		self.LEFT_EDGE_TEXT = 20
		self.SPACE = 30
		self.PANEL_HEIGHT = 50 # js (was hardcoded)
		
		# self.X_TITLE = 500 # (was X_SCREEN in original file)
		self.X_TITLE = ((self.W_SCREEN - self.SPACE) / 2) # See also def interfaceScreen
		self.Y_TITLE = 8
		# self.Z_TEXT = self.Z_SCREEN - 0.2
		self.Z_TEXT = 0
		self.DZ = -0.2
		# self.Z_CONTROLS = self.Z_TEXT # not used
		
		# self.X_EXIT = 994
		self.X_EXIT = self.W_SCREEN - self.SPACE #js / See also def interfaceScreen
		# self.Y_EXIT = 726
		self.Y_EXIT = self.H_SCREEN - 40 #js / See also def interfaceScreen
		
		# self.X_CANCEL = 552 # X_TITLE used instead
		# self.Y_CANCEL = 726 # Y_EXIT used instead
		# self.X_ANARCHY = 21 # LEFT_EDGE_TEXT used instead
		# self.Y_ANARCHY = 726 # Y_EXIT used instead
		
		self.Y_SCROLL_RELIGION = 20 # is
		# self.X_RELIGION_START = 180
		# self.DX_RELIGION = 98
###2 row religions - start		
		self.X_RELIGION_START = 140		
		#self.DX_RELIGION = 98
		self.DX_RELIGION = 93
###2 row religions - end		
		# self.Y_RELIGION = 35 # not used
		# self.Y_RELIGION_NAME = 58
		self.Y_RELIGION_NAME = 70
		self.Y_FOUNDED = 90
		# self.Y_HOLY_CITY = 115
		self.Y_HOLY_CITY = 110
		self.Y_INFLUENCE = 150
		
		# self.X_RELIGION_AREA = 45 # not used
		# self.Y_RELIGION_AREA = 84 # not used
		# self.W_RELIGION_AREA = 934 # not used
		self.H_RELIGION_AREA = 180 #175

		# self.W_CITY_AREA = 457
		self.W_CITY_AREA = (self.W_SCREEN - (self.SPACE * 3)) / 2 # See also def interfaceScreen
		# self.H_CITY_AREA = 395 #468
		self.H_CITY_AREA = (self.H_SCREEN - 298) # See also def interfaceScreen
		# self.X_CITY1_AREA = 45 #30
		self.X_CITY1_AREA = self.SPACE
		# self.X_CITY2_AREA = 522 #527
		self.X_CITY2_AREA = (self.SPACE + self.W_CITY_AREA + self.SPACE) # See also def interfaceScreen
		# self.Y_CITY_AREA = 282 #268
		self.Y_CITY_AREA = 248
		
		# self.X_CITY = 10 # not used
		# self.DY_CITY = 38 # not used
		
		
		self.iReligionExamined = -1
		self.iReligionSelected = -1
		self.iReligionOriginal = -1
		self.iActivePlayer = -1
		
		self.bScreenUp = False
		
		self.ReligionScreenInputMap = {
			self.RELIGION_NAME		: self.ReligionScreenButton,
			self.BUTTON_NAME		: self.ReligionScreenButton,
			self.CONVERT_NAME		: self.ReligionConvert,
			self.CANCEL_NAME		: self.ReligionCancel,
			}
			
	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.RELIGION_SCREEN)


	def interfaceScreen (self):
		# self.SCREEN_ART = CyArtFileMgr().getInterfaceArtInfo("TECH_BG").getPath() # not used
		self.NO_STATE_BUTTON_ART = CyArtFileMgr().getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
		self.EXIT_TEXT = u"<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.CONVERT_TEXT = u"<font=4>" + CyTranslator().getText("TXT_KEY_RELIGION_CONVERT", ()).upper() + "</font>"
		self.CANCEL_TEXT = u"<font=4>" + CyTranslator().getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + "</font>"

		self.iActivePlayer = gc.getGame().getActivePlayer()

		self.bScreenUp = True

		screen = self.getScreen()
		if screen.isActive():
			return
		
		if screen.getXResolution() > (self.W_SCREEN + 210):
			self.W_SCREEN = (screen.getXResolution() - 210)
			self.X_TITLE = ((self.W_SCREEN - self.SPACE) / 2)
			self.X_EXIT = self.W_SCREEN - self.SPACE #js
			self.W_CITY_AREA = (self.W_SCREEN - (self.SPACE * 3)) / 2
			self.X_CITY2_AREA = (self.SPACE + self.W_CITY_AREA + self.SPACE)
		
		if screen.getYResolution() != self.H_SCREEN:
			self.H_SCREEN = screen.getYResolution()
			self.Y_EXIT = self.H_SCREEN - 40 #js
			self.H_CITY_AREA = (self.H_SCREEN - 298)
		
		
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

		# johny smith ScreenTweaks LINE:
		# Set the background and exit button, and show the screen
		# screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setDimensions(0, 0, self.W_SCREEN, self.H_SCREEN)
		screen.addDDSGFC(self.BACKGROUND_ID, CyArtFileMgr().getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		## Panels on the Top(name of screen) and bottom(Cancel, Exit, Revolution buttons)
		# screen.addPanel( "ReligionsTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, self.PANEL_HEIGHT, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "ReligionsBottomPanel", u"", u"", True, False, 0, self.H_SCREEN - self.PANEL_HEIGHT, self.W_SCREEN, self.PANEL_HEIGHT, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		# screen.addPanel( "ReligionPanel", u"", u"", False, True, -10, 50, self.W_SCREEN + 20, self.H_RELIGION_AREA, PanelStyles.PANEL_STYLE_MAIN)
		# note: the "ReligionPanel" is now just a blue background panel, as all info is linked to the "ScrollReligion" "panel": disabled for now
		screen.setText(self.CANCEL_NAME, "ReligionsBottomPanel", self.CANCEL_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)

		screen.showWindowBackground(False)

		# Header...
		screen.setLabel("ReligionScreenHeader", "ReligionsTopPanel", u"<font=4b>" + CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.X_TITLE, self.Y_TITLE, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


		if (CyGame().isDebugMode()):
			screen.addDropDownBoxGFC(self.DEBUG_DROPDOWN_ID, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.DEBUG_DROPDOWN_ID, gc.getPlayer(j).getName(), j, j, False )

		# Make the scrollable area for the Religion panel... (johny smith)
		# note: the "ScrollReligion" is another panel and everything that should scroll with it must refer to this name
		screen.addScrollPanel( "ScrollReligion", "", self.LEFT_EDGE_TEXT, self.Y_SCROLL_RELIGION, self.W_SCREEN, self.H_RELIGION_AREA, PanelStyles.PANEL_STYLE_EXTERNAL )
		# screen.setActivation( "ScrollReligion", ActivationTypes.ACTIVATE_NORMAL ) # does not seem to be needed

		# Draw infos
		self.drawReligionInfo()
		self.drawCityInfo(self.iReligionSelected)

	# Draws the Religion buttons and information
	def drawReligionInfo(self):

		screen = self.getScreen()
		
		## johny smith
		## This draws the symbols
		## Puts the symbols in a loop # isenchine: 1 function instead of 2, 1 loop instead of 5!
		## Attachs the symbols so they will scroll 
		xLoop = self.X_RELIGION_START
		for i in xrange(gc.getNumReligionInfos()):
			if gc.getGame().getReligionGameTurnFounded(i) >= 0:
				screen.addCheckBoxGFCAt("ScrollReligion", self.getReligionButtonName(i), gc.getReligionInfo(i).getButton(), CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xLoop - 25, self.Y_SCROLL_RELIGION, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)

				szName = self.getReligionTextName(i) # isenchine: bof ?
				szLabel = gc.getReligionInfo(i).getDescription()
				screen.setLabelAt(szName, "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_RELIGION_NAME, self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Founded...
				screen.setLabelAt("", "ScrollReligion", CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_DATE_FOUNDED", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
				# Date Founded:
				szLabel = CyGameTextMgr().getTimeStr(gc.getGame().getReligionGameTurnFounded(i), false)
				screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Holy City...
				screen.setLabelAt("", "ScrollReligion", CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_HOLY_CITY", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				
				pHolyCity = gc.getGame().getHolyCity(i)
				if pHolyCity.isNone():
					szLabel = CyTranslator().getText("TXT_KEY_NONE", ())
					screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				elif not pHolyCity.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam(), False):
					szLabel = CyTranslator().getText("TXT_KEY_UNKNOWN", ())
					screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				else:
					szLabel = pHolyCity.getName()
					screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
					screen.setLabelAt("", "ScrollReligion", "(%s)" % gc.getPlayer(pHolyCity.getOwner()).getCivilizationAdjective(0), CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY+20, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				# Influence...
				screen.setLabelAt("", "ScrollReligion", CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_INFLUENCE", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				szLabel = str(gc.getGame().calculateReligionPercent(i)) + "%"
				screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)


				xLoop += self.DX_RELIGION

		# No State Religion...
		screen.addCheckBoxGFCAt("ScrollReligion", "", self.NO_STATE_BUTTON_ART, CyArtFileMgr().getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xLoop - 25, self.Y_SCROLL_RELIGION, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)
		
		szLabel = CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_NO_STATE", ())
		screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_RELIGION_NAME, self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# szLabel = "-" # useless...
		# screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# screen.setLabelAt("", "ScrollReligion", szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
##johny smith end##

		# the following line is a dummy to have a proper end of the scrolled area
		screen.setLabelAt("", "ScrollReligion", "", CvUtil.FONT_CENTER_JUSTIFY, (xLoop + 70 ), self.Y_RELIGION_NAME, self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.iReligionSelected = gc.getPlayer(self.iActivePlayer).getStateReligion()
		if (self.iReligionSelected == -1):
			self.iReligionSelected = gc.getNumReligionInfos()
		self.iReligionExamined = self.iReligionSelected
		self.iReligionOriginal = self.iReligionSelected


	# Draws the city lists
	def drawCityInfo(self, iReligion):
	
		if (not self.bScreenUp):
			return
		
		screen = self.getScreen()

		if (iReligion == gc.getNumReligionInfos()):
			iLinkReligion = -1
		else:
			iLinkReligion = iReligion

		# szArea1 = self.AREA1_ID
		screen.addPanel(self.AREA1_ID, "", "", True, True, self.X_CITY1_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN_BLACK25)
		
		# szArea2 = self.AREA2_ID
		screen.addPanel(self.AREA2_ID, "", "", True, True, self.X_CITY2_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN_BLACK25)

		# szArea = self.RELIGION_PANEL_ID
		for i in xrange(gc.getNumReligionInfos()):
			if (self.iReligionSelected == i):
				screen.setState(self.getReligionButtonName(i), True)
			else:
				screen.setState(self.getReligionButtonName(i), False)

		if (self.iReligionSelected == gc.getNumReligionInfos()):
			screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), True)
		else:
			screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), False)
		
		# City selection
		# PyActivePlayer = PyPlayer(self.iActivePlayer)
		# cityList = PyActivePlayer.getCityList()
		
		# Loop through the cities
		# for i in range(len(cityList)):
		
			# # bFirstColumn = (i % 2 == 0) # isenchine
		
			# pLoopCity = cityList[i]

			# # Constructing the City name...
			# szCityName = u""
			# szCityName += pLoopCity.getName()[0:14] + " "
			# if pLoopCity.isCapital():
				# szCityName += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
			
			# lHolyCity = pLoopCity.getHolyCity()
			# if lHolyCity:
				# for iI in range(len(lHolyCity)):
					# szCityName += u"%c" %(gc.getReligionInfo(lHolyCity[iI]).getHolyCityChar())
			
			# lReligions = pLoopCity.getReligions()
			# if lReligions:
				# for iI in range(len(lReligions)):
					# if lReligions[iI] not in lHolyCity:
						# szCityName += u"%c" %(gc.getReligionInfo(lReligions[iI]).getChar())
			
			# if (iLinkReligion == -1):
				# bFirst = True
				# for iI in range(len(lReligions)):
					# szTempBuffer = CyGameTextMgr().getReligionHelpCity(lReligions[iI], pLoopCity.GetCy(), False, False, False, True)
					# if (szTempBuffer):
						# if (not bFirst):
							# szCityName += u", "
						# szCityName += szTempBuffer
						# bFirst = False
			# else:
				# szCityName += CyGameTextMgr().getReligionHelpCity(iLinkReligion, pLoopCity.GetCy(), False, False, True, False)

			# if bFirstColumn:
				# szLeftCities += u"<font=3>" + szCityName + u"</font>\n"
			# else:
				# szRightCities += u"<font=3>" + szCityName + u"</font>\n"
		
		# isenchine: the left panel will now display all cities of all players with the selected religion.
		# isenchine: the right panel will now display all cities of all players without the selected religion.
		cityList = []
		szLeftCities = u""
		szRightCities = u""

		for iPlayerX in xrange(gc.getMAX_PLAYERS()):
		
			pPlayerX = gc.getPlayer(iPlayerX)
			if pPlayerX.isAlive() and not pPlayerX.isBarbarian():
				cityList = PyPlayer(iPlayerX).getCityList()
				sLeaderColor = u"<color=%d,%d,%d,%d>" %(pPlayerX.getPlayerTextColorR(), pPlayerX.getPlayerTextColorG(), pPlayerX.getPlayerTextColorB(), pPlayerX.getPlayerTextColorA())
				if iPlayerX == self.iActivePlayer:
					sLeaderName = sLeaderColor + "<font=3b>" + u"%s" %(pPlayerX.getName()) + "</font></color>"
				else:
					sLeaderName = sLeaderColor + u"%s" %(pPlayerX.getName()) + "</color>"
				
				for i in xrange(len(cityList)):
					
					pLoopCity = cityList[i]
					# if pLoopCity.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam(), False): for Cy, not for Py
					if pLoopCity.isRevealed(gc.getPlayer(self.iActivePlayer).getTeam()):
						
						# Constructing the City name...
						szCityName = u""
						szCityName = sLeaderName + ": " + pLoopCity.getName() + " "
						
						if pLoopCity.isCapital():
							szCityName += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
						
						lHolyCity = pLoopCity.getHolyCity()
						if lHolyCity:
							for iI in range(len(lHolyCity)):
								szCityName += u"%c" %(gc.getReligionInfo(lHolyCity[iI]).getHolyCityChar())
						
						lReligions = pLoopCity.getReligions()
						for iI in range(len(lReligions)):
							if lReligions[iI] not in lHolyCity:
								szCityName += u"%c" %(gc.getReligionInfo(lReligions[iI]).getChar())
						
						if iPlayerX == self.iActivePlayer:
							if (iLinkReligion == -1):
								bFirst = True
								for iI in range(len(lReligions)):
									szTempBuffer = CyGameTextMgr().getReligionHelpCity(lReligions[iI], pLoopCity.GetCy(), False, False, False, True)
									if (szTempBuffer):
										if (not bFirst):
											szCityName += u", "
										szCityName += szTempBuffer
										bFirst = False
							else:
								szCityName += CyGameTextMgr().getReligionHelpCity(iLinkReligion, pLoopCity.GetCy(), False, False, True, False)
						
						# note: \n = Newline
						if iLinkReligion in lReligions:
							szLeftCities += u"<font=3>" + szCityName + u"</font>\n"
						else:
							szRightCities += u"<font=3>" + szCityName + u"</font>\n"
		
		szLeftLabel = u"<font=3b>" + CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_LEFT_PANEL_TITLE", ()) + u"</font>"
		szRightLabel = u"<font=3b>" + CyTranslator().getText("TXT_KEY_RELIGION_SCREEN_RIGHT_PANEL_TITLE", ()) + u"</font>"
		screen.setLabelAt("ReligionsLeftPanelTitle", self.BACKGROUND_ID, szLeftLabel, CvUtil.FONT_LEFT_JUSTIFY, self.X_CITY1_AREA+5, self.Y_CITY_AREA-20, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("ReligionsRightPanelTitle", self.BACKGROUND_ID, szRightLabel, CvUtil.FONT_LEFT_JUSTIFY, self.X_CITY2_AREA+5, self.Y_CITY_AREA-20, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		# End isenchine
		
		screen.addMultilineText("Child" + self.AREA1_ID, szLeftCities, self.X_CITY1_AREA+5, self.Y_CITY_AREA+5, self.W_CITY_AREA-10, self.H_CITY_AREA-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addMultilineText("Child" + self.AREA2_ID, szRightCities, self.X_CITY2_AREA+5, self.Y_CITY_AREA+5, self.W_CITY_AREA-10, self.H_CITY_AREA-10, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		
		# Convert Button....
		iLink = 0
		if (gc.getPlayer(self.iActivePlayer).canChangeReligion()):
			iLink = 1
		
		if (not self.canConvert(iLinkReligion) or iLinkReligion == self.iReligionOriginal):
			screen.setText(self.CONVERT_NAME, self.BACKGROUND_ID, self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)
			screen.hide(self.CANCEL_NAME)
			szAnarchyTime = CyGameTextMgr().setConvertHelp(self.iActivePlayer, iLinkReligion)
		else:
			screen.setText(self.CONVERT_NAME, self.BACKGROUND_ID, self.CONVERT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CONVERT, iLinkReligion, 1)
			screen.show(self.CANCEL_NAME)
			szAnarchyTime = CyTranslator().getText("TXT_KEY_ANARCHY_TURNS", (gc.getPlayer(self.iActivePlayer).getReligionAnarchyLength(), ))

		# Turns of Anarchy Text...
		screen.setLabel(self.RELIGION_ANARCHY_WIDGET, self.BACKGROUND_ID, u"<font=3>" + szAnarchyTime + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_EXIT, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def getReligionButtonName(self, iReligion):
		szName = self.BUTTON_NAME + str(iReligion)
		return szName

	def getReligionTextName(self, iReligion):
		szName = self.RELIGION_NAME + str(iReligion)
		return szName

	def canConvert(self, iReligion):
		iCurrentReligion = gc.getPlayer(self.iActivePlayer).getStateReligion()
		if (iReligion == gc.getNumReligionInfos()):
			iConvertReligion = -1
		else:
			iConvertReligion = iReligion
		
		return (iConvertReligion != iCurrentReligion and gc.getPlayer(self.iActivePlayer).canConvert(iConvertReligion))		

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
			self.drawReligionInfo()
			self.drawCityInfo(self.iReligionSelected)
			return 1
		elif (self.ReligionScreenInputMap.has_key(inputClass.getFunctionName())):	
			'Calls function mapped in ReligionScreenInputMap'
			# only get from the map if it has the key
			
			# get bound function from map and call it
			self.ReligionScreenInputMap.get(inputClass.getFunctionName())(inputClass)
			return 1
		return 0
		
	def update(self, fDelta):
		return

	# Religion Button
	def ReligionScreenButton( self, inputClass ):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ) :
			if (inputClass.getID() == gc.getNumReligionInfos() or gc.getGame().getReligionGameTurnFounded(inputClass.getID()) >= 0) :
				self.iReligionSelected = inputClass.getID()
				self.iReligionExamined = self.iReligionSelected
				self.drawCityInfo(self.iReligionSelected)
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ) :
			if ( inputClass.getID() == gc.getNumReligionInfos() or gc.getGame().getReligionGameTurnFounded(inputClass.getID()) >= 0) :
				self.iReligionExamined = inputClass.getID()
				self.drawCityInfo(self.iReligionExamined)
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ) :
			self.iReligionExamined = self.iReligionSelected
			self.drawCityInfo(self.iReligionSelected)
		return 0

	def ReligionConvert(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			screen.hideScreen()
		
	def ReligionCancel(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			self.iReligionSelected = self.iReligionOriginal
			if (-1 == self.iReligionSelected):
				self.iReligionSelected = gc.getNumReligionInfos()
			self.drawCityInfo(self.iReligionSelected)
		
