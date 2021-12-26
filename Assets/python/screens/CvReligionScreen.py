## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005

# VET - NewChars # 1					SDK

from CvPythonExtensions import *
import PyHelpers
import CvUtil
import ScreenInput
import CvScreenEnums

PyPlayer = PyHelpers.PyPlayer

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class CvReligionScreen:
	"Religion Advisor Screen"

	def __init__(self):
		self.SCREEN_NAME = "ReligionScreen"
		self.BUTTON_NAME = "ReligionScreenButton"
		self.RELIGION_NAME = "ReligionText"
		self.CONVERT_NAME = "ReligionConvertButton"
		self.CANCEL_NAME = "ReligionCancelButton"
		self.CITY_NAME = "ReligionCity"
		self.HEADER_NAME = "ReligionScreenHeader"
		self.DEBUG_DROPDOWN_ID =  "ReligionDropdownWidget"
		self.AREA1_ID = "ReligionAreaWidget1"
		self.AREA2_ID = "ReligionAreaWidget2"
		self.BACKGROUND_ID = "ReligionBackground"
		self.RELIGION_PANEL_ID = "ReligionPanel"
 # LPlate insertion - Tamriel
		self.AREA3_ID = "ReligionAreaWidget3"
		self.DEVOTIONS_PANEL_ID = "DevotionsPanel"
		self.CIVICSBUTTON_NAME = "CivicsScreenButton"
		self.TEXT_NAME = "CivicsScreenText"
		self.EXIT_NAME = "CivicsExit"
		self.CIVICSCANCEL_NAME = "CivicsCancel"
		self.m_paeCurrentCivics = []
		self.m_paeDisplayCivics = []
		self.m_paeOriginalCivics = []
		self.HEADINGS_WIDTH = 233#199
		self.HEADINGS_TOP = 70
		self.HEADINGS_SPACING = 5
		self.HEADINGS_BOTTOM = 280
		self.HELP_HEADER_NAME = "CivicsScreenHeaderName"
		self.HELP_AREA_NAME = "CivicsScreenHelpArea"
		self.HELP_IMAGE_NAME = "CivicsScreenCivicOptionImage"
		self.HELP_TOP = 350
		self.HELP_BOTTOM = 610
		self.TEXT_MARGIN = 15
		self.X_SCREEN = 500
		self.BOTTOM_LINE_TOP = 630
		self.BOTTOM_LINE_WIDTH = 1014
		self.BOTTOM_LINE_HEIGHT = 60
		self.X_SELECTED_DEV = 1340
		self.X_CONVERT = 650#11Jul LPlate addition
 # End LPlate insertion - Tamriel
		self.RELIGION_ANARCHY_WIDGET = "ReligionAnarchyWidget"
		self.SCROLL_NAME = "ReligionScroll"

		self.SPACING = 10			# Растояние между элементами экрана
		self.RELIGION_SPACING = 60	# Дополнительная длинна области под кнопки религий
		self.MIN_DX_RELIGION = 100	# Минимальное растояние между кнопками религий
		self.MAX_DX_RELIGION = 120	# Максимальное растояние между кнопками религий, при котором сохраняется изображение в 2 уровня
		self.TEXT_SPACING = 5

		self.H_PANEL = 55
		self.Y_TOP_PANEL = -2

		self.BORDER_WIDTH = 2
		self.BUTTON_SIZE = 48

		self.Y_TITLE = 8
		self.Z_TEXT = -6.3
		self.DZ = -0.2

		self.LEFT_EDGE_TEXT = 5
		self.X_RELIGION_START = 155
		self.Y_RELIGION = 33

		self.Y_FOUNDED = 91
		self.Y_HOLY_CITY = 139
		self.Y_INFLUENCE = 181

		self.X_RELIGION_AREA = self.SPACING
		self.Y_RELIGION_AREA = self.Y_TOP_PANEL + self.H_PANEL + self.SPACING
		self.H_RELIGION_AREA = 215

## LPlate - original unmodified code
##		self.Y_CITY_AREA = self.Y_RELIGION_AREA + self.H_RELIGION_AREA + self.SPACING
## End LPlate - original unmodified code
# LPlate insertion - Tamriel
### Ramzay1945, adjust the self.X_DAEDRA and self.X_8 values to reposition the devotions buttons laterally
		self.H_DEVOTIONS = 280 #210
		self.X_DAEDRA = 120 #50 #120 # LPlate 11Jul - changed from 120 to 50
		self.X_8 = 115 #190 #100
		self.Y_DEVOTIONS_AREA = self.Y_RELIGION_AREA + self.H_RELIGION_AREA + self.SPACING
		self.Y_DEVOTIONS_POSITION = self.Y_DEVOTIONS_AREA + self.SPACING
		self.Y_CITY_AREA = self.Y_RELIGION_AREA + self.H_RELIGION_AREA + self.SPACING + self.H_DEVOTIONS + self.SPACING
# End LPlate insertion - Tamriel
		self.X_CITY = self.SPACING

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
# End LPlate insertion - Tamriel
			self.CIVICSBUTTON_NAME		: self.CivicsButton,
			self.TEXT_NAME			: self.CivicsButton,
			self.EXIT_NAME			: self.Revolution,
			self.CIVICSCANCEL_NAME		: self.Cancel,
# End LPlate insertion - Tamriel
			}

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.RELIGION_SCREEN)

	def interfaceScreen (self):
		self.SCREEN_ART = ArtFileMgr.getInterfaceArtInfo("TECH_BG").getPath()
		self.NO_STATE_BUTTON_ART = ArtFileMgr.getInterfaceArtInfo("INTERFACE_BUTTONS_CANCEL").getPath()
		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"
		self.CONVERT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_RELIGION_CONVERT", ()).upper() + "</font>"
		self.CANCEL_TEXT = u"<font=4>" + localText.getText("TXT_KEY_SCREEN_CANCEL", ()).upper() + "</font>"

		self.iActivePlayer = gc.getGame().getActivePlayer()
		self.pActivePlayer = gc.getPlayer(self.iActivePlayer)

# LPlate insertion - Tamriel
		self.m_paeCurrentCivics = []
		self.m_paeDisplayCivics = []
		self.m_paeOriginalCivics = []
		for i in range (gc.getNumCivicOptionInfos()):
			self.m_paeCurrentCivics.append(self.pActivePlayer.getCivics(i));
			self.m_paeDisplayCivics.append(self.pActivePlayer.getCivics(i));
			self.m_paeOriginalCivics.append(self.pActivePlayer.getCivics(i));
# End LPlate insertion - Tamriel

		self.bScreenUp = True

		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen( PopupStates.POPUPSTATE_IMMEDIATE, False)

		iXResolution = screen.getXResolution()
		iYResolution = screen.getYResolution()

		iAdd = 8
		self.X_CITY1_AREA = self.SPACING
		self.W_CITY_AREA = (iXResolution - 2 * self.X_CITY1_AREA - self.SPACING) / 2
		self.TEXT_WIDTH = self.W_CITY_AREA - 2 * self.TEXT_SPACING - iAdd

		iMaxLines = 0
		iMaxWidth = 0
		i = -1
		while i < gc.getNumReligionInfos():
			(szLeftCities, szRightCities) = self.getCityText(i)
			i += 1
			iNam = 1
			while iNam < 3:
				if iNam == 1:
					szText = szLeftCities
				else:
					szText = szRightCities
				iNam += 1
				iLines = 0
				iWidth = 0
				for line in szText.splitlines():
					iWidth = CyInterface().determineWidth(line)
					if iWidth > iMaxWidth:
						iMaxWidth = iWidth
					iLines += iWidth / self.TEXT_WIDTH
					if iWidth % self.TEXT_WIDTH > 0:
						iLines += 1
				if iLines > iMaxLines:
					iMaxLines = iLines

		if iMaxLines < 2:
			iMaxLines = 2
		self.H_CITY_AREA = iMaxLines * 22 + 2 * self.TEXT_SPACING + 2
	#	if self.H_CITY_AREA < 85:
	#		self.H_CITY_AREA = 85
		self.H_SCREEN  = self.Y_CITY_AREA + self.H_CITY_AREA + self.SPACING + self.H_PANEL
		if self.H_SCREEN > iYResolution:
			self.H_CITY_AREA -= (self.H_SCREEN - iYResolution)
			self.H_SCREEN = iYResolution
			iMaxWidth += 8 # поправка на скролинг

		self.TEXT_WIDTH = iMaxWidth + iAdd
		self.W_CITY_AREA = self.TEXT_WIDTH + 2 * self.TEXT_SPACING
		self.W_SCREEN = self.W_CITY_AREA * 2 + 2 * self.X_CITY1_AREA + self.SPACING

		if self.W_SCREEN > iXResolution:
			self.W_SCREEN = iXResolution
			self.W_CITY_AREA = (self.W_SCREEN - self.SPACING) / 2 - self.X_CITY1_AREA # (self.W_SCREEN - 2 * self.X_CITY1_AREA - self.SPACING) / 2
			self.TEXT_WIDTH = self.W_CITY_AREA - 2 * self.TEXT_SPACING

		iWidth = self.X_RELIGION_START + self.RELIGION_SPACING + self.MAX_DX_RELIGION * gc.getNumReligionInfos() + 2 * self.SPACING
		if iWidth > self.W_SCREEN:
			self.W_SCREEN = iWidth
		if self.W_SCREEN > iXResolution:
			self.W_SCREEN = iXResolution

	#	if self.W_CITY_AREA < 70:
	#		self.W_CITY_AREA = 70
	#		self.TEXT_WIDTH = self.W_CITY_AREA - 2 * self.TEXT_SPACING
		self.X_CITY1_AREA = (self.W_SCREEN - self.SPACING) / 2 - self.W_CITY_AREA # (self.W_SCREEN - self.SPACING - 2 * self.W_CITY_AREA) / 2
		self.X_CITY2_AREA = self.X_CITY1_AREA + self.W_CITY_AREA + self.SPACING # (self.W_SCREEN + self.SPACING) / 2

		self.W_RELIGION_AREA = self.W_SCREEN - 2 * self.SPACING
		if gc.getNumReligionInfos() > 1:
			self.DX_RELIGION = (self.W_RELIGION_AREA - self.X_RELIGION_START - self.RELIGION_SPACING) / gc.getNumReligionInfos()
		else:
			self.DX_RELIGION = 0

		self.Y_BOTTOM_PANEL = self.H_SCREEN - self.H_PANEL

		self.X_EXIT = self.W_SCREEN - 2 * self.SPACING
		self.Y_EXIT = self.H_SCREEN - 42

		self.X_CANCEL = self.W_SCREEN / 2
		self.Y_CANCEL = self.Y_EXIT

		self.X_ANARCHY = 2 * self.SPACING
		self.Y_ANARCHY = self.Y_EXIT

		# Set the background and exit button, and show the screen
		#screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setDimensions((iXResolution - self.W_SCREEN) / 2, (iYResolution - self.H_SCREEN) / 2, self.W_SCREEN, self.H_SCREEN)

		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, self.Y_TOP_PANEL, self.W_SCREEN, self.H_PANEL, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, self.Y_BOTTOM_PANEL, self.W_SCREEN, self.H_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.setText(self.CANCEL_NAME, "Background", self.CANCEL_TEXT, CvUtil.FONT_CENTER_JUSTIFY, self.X_CANCEL, self.Y_CANCEL, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)

		screen.showWindowBackground(False)

		# Header...
		screen.setLabel(self.HEADER_NAME, "Background", u"<font=4b>" + localText.getText("TXT_KEY_RELIGION_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_SCREEN / 2, self.Y_TITLE, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Make the scrollable areas for the city list...
		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		# Put everything on a scrollable area
		screen.addPanel(self.RELIGION_PANEL_ID, "", "", False, True, self.X_RELIGION_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA, self.H_RELIGION_AREA, PanelStyles.PANEL_STYLE_MAIN)

		# Make the scrollable area for the civics list...
		screen.addScrollPanel(self.SCROLL_NAME, u"", self.X_RELIGION_AREA, self.Y_RELIGION_AREA, self.W_RELIGION_AREA, self.H_RELIGION_AREA - 9, PanelStyles.PANEL_STYLE_EXTERNAL )
		#screen.setActivation(self.SCROLL_NAME, ActivationTypes.ACTIVATE_NORMAL )

		# Draw Religion info
		self.drawReligionInfo()
# LPlate insertion - Tamriel
		self.drawDevotionsInfo(self.iReligionSelected)
# End LPlate insertion - Tamriel
		self.drawCityInfo(self.iReligionSelected)

	# Draws the religion buttons and information
	def drawReligionInfo(self):
		if self.DX_RELIGION < self.MAX_DX_RELIGION:
			k = 8
			if self.DX_RELIGION < self.MIN_DX_RELIGION:
				self.DX_RELIGION = self.MIN_DX_RELIGION
		else:
			k = 0

		self.Y_mFOUNDED = [self.Y_FOUNDED - k, self.Y_FOUNDED + k]
		self.Y_mHOLY_CITY = [self.Y_HOLY_CITY - k, self.Y_HOLY_CITY + k]
		self.Y_mRELIGION_NAME = [59 - k, 59 +k]

		self.iReligionSelected = self.pActivePlayer.getStateReligion()
		screen = self.getScreen()
		szArea = self.SCROLL_NAME

		# Religion buttons at the top
		xLoop = self.X_RELIGION_START
		for i in range(gc.getNumReligionInfos()):
			k = i % 2

		# Button
			szButtonName = self.getReligionButtonName(i)
			screen.addCheckBoxGFCAt(szArea, szButtonName, gc.getReligionInfo(i).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xLoop - self.BUTTON_SIZE/2, self.Y_RELIGION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)
			if gc.getGame().getReligionGameTurnFounded(i) > -1:
				screen.enable(szButtonName, true)
			#	screen.setActivation(szButtonName, ActivationTypes.ACTIVATE_NORMAL )
			else:
				screen.enable(szButtonName, false)
		#		screen.setImageButtonAt(szArea, szButtonName, gc.getReligionInfo(i).getButtonDisabled(), xLoop - self.BUTTON_SIZE/2, self.Y_RELIGION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			#	screen.setActivation(szButtonName, ActivationTypes.ACTIVATE_NORMAL )

		# Name
			szName = self.getReligionTextName(i)
			szLabel = u"<font=3>" + gc.getReligionInfo(i).getDescription() + "</font>"
			if self.iReligionSelected == i:
				szLabel = localText.changeTextColor(szLabel, gc.getInfoTypeForString("COLOR_GREEN"))
			#screen.setTextAt(szName, szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mRELIGION_NAME[k], 2*self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			screen.setLabelAt("", szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mRELIGION_NAME[k], 2*self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Date Founded:
			if (gc.getGame().getReligionGameTurnFounded(i) < 0):
				szFounded = localText.getText("TXT_KEY_RELIGION_SCREEN_NOT_FOUNDED", ())
			else:
				szFounded = CyGameTextMgr().getTimeStr(gc.getGame().getReligionGameTurnFounded(i), false)
			screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mFOUNDED[k], self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Holy City
			pHolyCity = gc.getGame().getHolyCity(i)
			if pHolyCity.isNone():
				szFounded = localText.getText("TXT_KEY_NONE", ())
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHOLY_CITY[k], self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			elif not pHolyCity.isRevealed(self.pActivePlayer.getTeam(), False):
				szFounded = localText.getText("TXT_KEY_UNKNOWN", ())
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHOLY_CITY[k], self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				szFounded = pHolyCity.getName()
				screen.setLabelAt("", szArea, "(%s)" % gc.getPlayer(pHolyCity.getOwner()).getCivilizationAdjective(0), CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHOLY_CITY[k]+16, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHOLY_CITY[k]-16, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Influence
			if (gc.getGame().getReligionGameTurnFounded(i) < 0):
				szFounded = "0%"
			else:
				szFounded = str(gc.getGame().calculateReligionPercent(i)) + "%"
			screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			xLoop += self.DX_RELIGION

	# Button
		szButtonName = self.getReligionButtonName(gc.getNumReligionInfos())
		screen.addCheckBoxGFCAt(szArea, szButtonName, self.NO_STATE_BUTTON_ART, ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xLoop - self.BUTTON_SIZE/2, self.Y_RELIGION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, false)

	# Name
		szName = self.getReligionTextName(gc.getNumReligionInfos())
		szLabel = u"<font=3>" + localText.getText("TXT_KEY_RELIGION_SCREEN_NO_STATE", ()) + "</font>"
		if self.iReligionSelected == -1:
			szLabel = localText.changeTextColor(szLabel, gc.getInfoTypeForString("COLOR_GREEN"))

		k = (i + 1) % 2
		#screen.setText(szName, szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop + self.X_RELIGION_AREA, self.Y_RELIGION_AREA + self.Y_mRELIGION_NAME[k], 2*self.DZ, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("", szArea, szLabel, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mRELIGION_NAME[k], 2*self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	# Founded
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_DATE_FOUNDED", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("", szArea, "", CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	# Holy City
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_HOLY_CITY", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("", szArea, "-", CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_HOLY_CITY, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	# Influence
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_INFLUENCE", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabelAt("", szArea, "-", CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_INFLUENCE, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if (self.iReligionSelected == -1):
			self.iReligionSelected = gc.getNumReligionInfos()
		self.iReligionExamined = self.iReligionSelected
		self.iReligionOriginal = self.iReligionSelected
		if (not self.bScreenUp):
			return
			
# LPlate insertion - Tamriel
	def drawDevotionsInfo(self, iReligion):
		if (not self.bScreenUp):
			return

		screen = self.getScreen()

		iDivineRel = gc.getInfoTypeForString('RELIGION_EIGHT_DIVINES')
		iDivineDev = gc.getInfoTypeForString('CIVICOPTION_8_DIVINES')
		iDaedraRel = gc.getInfoTypeForString('RELIGION_ISLAM')
		iDaedraDev = gc.getInfoTypeForString('CIVICOPTION_DAEDRA')
		iNordicRel = gc.getInfoTypeForString('RELIGION_CHRISTIANITY')
		iNordicDev = gc.getInfoTypeForString('CIVICOPTION_NORDIC')
		iAltmerRel = gc.getInfoTypeForString('RELIGION_JUDAISM')
		iAltmerDev = gc.getInfoTypeForString('CIVICOPTION_ALTMER')
		iTribunalRel = gc.getInfoTypeForString('RELIGION_TRIBUNAL')
		iTribunalDev = gc.getInfoTypeForString('CIVICOPTION_TRIBUNAL')
		iCurrentReligion = self.pActivePlayer.getStateReligion()
		# Leave out row if do not have applicable religion
		if (iCurrentReligion != iDivineRel and iCurrentReligion != iDaedraRel and iCurrentReligion != iNordicRel and iCurrentReligion != iAltmerRel and iCurrentReligion != iTribunalRel):
			return
		else:
			szArea3 = self.AREA3_ID
			screen.addPanel(self.DEVOTIONS_PANEL_ID, "", "", True, True, self.SPACING, self.Y_DEVOTIONS_AREA, (self.W_SCREEN - (2*self.SPACING)), self.H_DEVOTIONS, PanelStyles.PANEL_STYLE_MAIN)

		iExtraYRowDrop = 0 # 11Jul LPlate addition
		iExtraDropCheck = 0 # 11Jul LPlate addition

		if (iCurrentReligion == iDivineRel):
			iX_DEVOTIONS = self.X_8
			iCivicOption = gc.getInfoTypeForString('CIVICOPTION_8_DIVINES')
			iDevotions = 12
		elif (iCurrentReligion == iDaedraRel):
			iExtraDropCheck = iExtraDropCheck + 1
			iX_DEVOTIONS = self.X_DAEDRA
			iCivicOption = gc.getInfoTypeForString('CIVICOPTION_DAEDRA')
			iDevotions = 10
		elif (iCurrentReligion == iNordicRel):
			iX_DEVOTIONS = self.X_8
			iCivicOption = gc.getInfoTypeForString('CIVICOPTION_NORDIC')
			iDevotions = 12
		elif (iCurrentReligion == iAltmerRel):
			iX_DEVOTIONS = self.X_8
			iCivicOption = gc.getInfoTypeForString('CIVICOPTION_ALTMER')
			iDevotions = 12
		elif (iCurrentReligion == iTribunalRel):
			iX_DEVOTIONS = self.X_8
			iCivicOption = gc.getInfoTypeForString('CIVICOPTION_TRIBUNAL')
			iDevotions = 12

		iYRowDrop = 2*self.TEXT_MARGIN + self.BUTTON_SIZE + 2*self.TEXT_SPACING
		iDevCount = 0

		fX = self.SPACING * 2 - self.X_DAEDRA
		fY = self.Y_DEVOTIONS_AREA + 2*self.SPACING + 5
		for j in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(j).getCivicOptionType() == iCivicOption):
				iDevCount += 1
				if iDevCount == 1:
					fX = self.SPACING * 2 - self.X_DAEDRA
					fY = self.Y_DEVOTIONS_AREA + self.SPACING + 5
				if iDevCount == iDevotions:
				#if iDevCount == iDevotions:
					fX = self.SPACING * 2 - self.X_DAEDRA + 120
					fY += iYRowDrop

				fX += iX_DEVOTIONS
				screen.addCheckBoxGFC(self.getCivicsButtonName(j), gc.getCivicInfo(j).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), fX, fY, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL)
				screen.setText(self.getCivicsTextName(j), "", gc.getCivicInfo(j).getDescription(), CvUtil.FONT_LEFT_JUSTIFY, fX, fY+self.BUTTON_SIZE, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)# LPlate - pre 11Jul
#				screen.setText(self.getCivicsTextName(j), "", gc.getCivicInfo(j).getDescription(), CvUtil.FONT_LEFT_JUSTIFY, fX, fY+self.BUTTON_SIZE+iExtraYRowDrop, 0, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)# 11Jul LPlate addition

# 11Jul LPlate addition
#				if (iCivicOption == gc.getInfoTypeForString('CIVICOPTION_DAEDRA') and iExtraYRowDrop == 40):
#					iExtraYRowDrop = 0
#				elif (iCivicOption == gc.getInfoTypeForString('CIVICOPTION_DAEDRA') and iExtraYRowDrop == 20):
#					iExtraYRowDrop = 40
#				elif (iCivicOption == gc.getInfoTypeForString('CIVICOPTION_DAEDRA') and iExtraYRowDrop == 0):
#					iExtraYRowDrop = 20
# End 11Jul LPlate addition
		for j in range(gc.getNumCivicInfos()):
			if (gc.getCivicInfo(j).getCivicOptionType() == iDivineDev):
				screen.setState(self.getCivicsButtonName(j), self.m_paeCurrentCivics[iCivicOption] == j)
			elif (gc.getCivicInfo(j).getCivicOptionType() == iDaedraDev):
				screen.setState(self.getCivicsButtonName(j), self.m_paeCurrentCivics[iCivicOption] == j)
			elif (gc.getCivicInfo(j).getCivicOptionType() == iNordicDev):
				screen.setState(self.getCivicsButtonName(j), self.m_paeCurrentCivics[iCivicOption] == j)
			elif (gc.getCivicInfo(j).getCivicOptionType() == iAltmerDev):
				screen.setState(self.getCivicsButtonName(j), self.m_paeCurrentCivics[iCivicOption] == j)
			elif (gc.getCivicInfo(j).getCivicOptionType() == iTribunalDev):
				screen.setState(self.getCivicsButtonName(j), self.m_paeCurrentCivics[iCivicOption] == j)
				if (self.m_paeDisplayCivics[iCivicOption] == j):
					#screen.setState(self.getCivicsButtonName(j), True)
					screen.show(self.getCivicsButtonName(j))
				elif (self.pActivePlayer.canDoCivics(j)):
					#screen.setState(self.getCivicsButtonName(j), False)
					screen.show(self.getCivicsButtonName(j))
				else:
					screen.hide(self.getCivicsButtonName(j))

	def getCivicsButtonName(self, iCivic):
		szName = self.CIVICSBUTTON_NAME + str(iCivic)
		return szName

	def getCivicsTextName(self, iCivic):
		szName = self.TEXT_NAME + str(iCivic)
		return szName

	def CivicsButton(self, inputClass):
	
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			if (inputClass.getFlags() & MouseFlags.MOUSE_RBUTTONUP):
				CvScreensInterface.pediaJumpToCivic((inputClass.getID(), ))
			else:
				# Select button
				self.select(inputClass.getID())
				self.drawHelpText(gc.getCivicInfo(inputClass.getID()).getCivicOptionType())
				self.updateAnarchy()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON) :
			# Highlight this button
			if self.highlight(inputClass.getID()):
				self.drawHelpText(gc.getCivicInfo(inputClass.getID()).getCivicOptionType())
				self.updateAnarchy()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF) :
			if self.unHighlight(inputClass.getID()):
				self.drawHelpText(gc.getCivicInfo(inputClass.getID()).getCivicOptionType())
				self.updateAnarchy()

		return 0

	def Cancel(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			for i in range (gc.getNumCivicOptionInfos()):
				self.m_paeCurrentCivics[i] = self.m_paeOriginalCivics[i]
				self.m_paeDisplayCivics[i] = self.m_paeOriginalCivics[i]
			
			self.drawContents()

	def Revolution(self, inputClass):

		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			if (self.pActivePlayer.canRevolution(0)):
				messageControl = CyMessageControl()
				messageControl.sendUpdateCivics(self.m_paeDisplayCivics)
			screen = self.getScreen()
			screen.hideScreen()

	def highlight(self, iCivic):
		iCivicOption = gc.getCivicInfo(iCivic).getCivicOptionType()
		if self.m_paeDisplayCivics[iCivicOption] != iCivic:
			self.m_paeDisplayCivics[iCivicOption] = iCivic
			self.drawCivicOptionButtons(iCivicOption)
			return True
		return False
		
	def unHighlight(self, iCivic):		
		iCivicOption = gc.getCivicInfo(iCivic).getCivicOptionType()
		if self.m_paeDisplayCivics[iCivicOption] != self.m_paeCurrentCivics[iCivicOption]:
			self.m_paeDisplayCivics[iCivicOption] = self.m_paeCurrentCivics[iCivicOption]
			self.drawCivicOptionButtons(iCivicOption)
			return True
		return False

	def drawCivicOptionButtons(self, iCivicOption):
		screen = self.getScreen()

		for j in range(gc.getNumCivicInfos()):

			if (gc.getCivicInfo(j).getCivicOptionType() == iCivicOption):
				screen.setState(self.getCivicsButtonName(j), self.m_paeCurrentCivics[iCivicOption] == j)

				if (self.m_paeDisplayCivics[iCivicOption] == j):
					#screen.setState(self.getCivicsButtonName(j), True)
					screen.show(self.getCivicsButtonName(j))
				elif (self.pActivePlayer.canDoCivics(j)):
					#screen.setState(self.getCivicsButtonName(j), False)
					screen.show(self.getCivicsButtonName(j))
				else:
					screen.hide(self.getCivicsButtonName(j))

	def drawHelpText(self, iCivicOption):
		iCivic = self.m_paeDisplayCivics[iCivicOption]

		szPaneID = "CivicsHelpTextBackground" + str(iCivicOption)
		screen = self.getScreen()

		szHelpText = u""

		# Upkeep string
		if ((gc.getCivicInfo(iCivic).getUpkeep() != -1) and not self.pActivePlayer.isNoCivicUpkeep(iCivicOption)):
			szHelpText = gc.getUpkeepInfo(gc.getCivicInfo(iCivic).getUpkeep()).getDescription()
		else:
			szHelpText = localText.getText("TXT_KEY_CIVICS_SCREEN_NO_UPKEEP", ())

		szHelpText += CyGameTextMgr().parseCivicInfo(iCivic, False, True, True)

		screen.setLabel(self.HELP_HEADER_NAME + str(iCivicOption), "Background",  u"<font=3>" + gc.getCivicInfo(self.m_paeDisplayCivics[iCivicOption]).getDescription().upper() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, (self.W_SCREEN - (2*self.SPACING) - self.HEADINGS_WIDTH), self.HELP_TOP + self.TEXT_MARGIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		fY = self.HELP_TOP - self.BUTTON_SIZE
		szHelpImageID = self.HELP_IMAGE_NAME + str(iCivicOption)
#		screen.setImageButton(szHelpImageID, gc.getCivicInfo(iCivic).getButton(), self.X_SELECTED_DEV, fY, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1)
		screen.setImageButton(szHelpImageID, gc.getCivicInfo(iCivic).getButton(), (self.W_SCREEN - (2*self.SPACING) - self.HEADINGS_WIDTH), fY, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIVIC, iCivic, 1)

		fY = self.HELP_TOP + 3 * self.TEXT_MARGIN
		szHelpAreaID = self.HELP_AREA_NAME + str(iCivicOption)
		screen.addMultilineText(szHelpAreaID, szHelpText, (self.W_SCREEN - (2*self.SPACING) - self.HEADINGS_WIDTH), fY, self.HEADINGS_WIDTH, self.HELP_BOTTOM - fY-2, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

	def updateAnarchy(self):

		screen = self.getScreen()

		bChange = False
		i = 0
		while (i  < gc.getNumCivicOptionInfos() and not bChange):
			if (self.m_paeCurrentCivics[i] != self.m_paeOriginalCivics[i]):
				bChange = True
			i += 1		
		
		# Make the revolution button
		screen.deleteWidget(self.EXIT_NAME)
		if (self.pActivePlayer.canRevolution(0) and bChange):			
# 11Jul LPlate - commenting out						screen.setText(self.EXIT_NAME, "Background", u"<font=4>" + localText.getText("TXT_KEY_CONCEPT_REVOLUTION", ( )).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, (self.X_EXIT-2*self.BUTTON_SIZE), self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_REVOLUTION, 1, 0)
			screen.setText(self.EXIT_NAME, "Background", u"<font=4>" + localText.getText("TXT_KEY_CONCEPT_REVOLUTION", ( )).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, (self.X_EXIT-4*self.BUTTON_SIZE), self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_REVOLUTION, 1, 0)# 11Jul LPlate, trying to shove revolution button sideways to avoid overlapping text


			screen.show(self.CANCEL_NAME)
		else:
			screen.setText(self.EXIT_NAME, "Background", u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ( )).upper() + u"</font>", CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, -1)
			screen.hide(self.CANCEL_NAME)

		# Anarchy
		iTurns = self.pActivePlayer.getCivicAnarchyLength(self.m_paeDisplayCivics);
		
		if (self.pActivePlayer.canRevolution(0)):
			szText = localText.getText("TXT_KEY_ANARCHY_TURNS", (iTurns, ))
		else:
			szText = CyGameTextMgr().setRevolutionHelp(self.iActivePlayer)

		#screen.setLabel("CivicsRevText", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, (self.W_SCREEN - (self.SPACING) - (2*self.BUTTON_SIZE)), self.BOTTOM_LINE_TOP - 90 + self.TEXT_MARGIN//2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("CivicsRevText", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 20, self.BOTTOM_LINE_TOP - 150 + self.TEXT_MARGIN//2, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Maintenance		
		szText = localText.getText("TXT_KEY_CIVIC_SCREEN_UPKEEP", (self.pActivePlayer.getCivicUpkeep(self.m_paeDisplayCivics, True), ))
		#screen.setLabel("CivicsUpkeepText", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, (self.W_SCREEN - (self.SPACING) - (2*self.BUTTON_SIZE)), self.BOTTOM_LINE_TOP - 90 + self.BOTTOM_LINE_HEIGHT - 2 * self.TEXT_MARGIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setLabel("CivicsUpkeepText", "Background", u"<font=3>" + szText + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, 20, self.BOTTOM_LINE_TOP - 150 + self.BOTTOM_LINE_HEIGHT - 2 * self.TEXT_MARGIN, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def select(self, iCivic):
		if (not self.pActivePlayer.canDoCivics(iCivic)):
			# If you can't even do this, get out....
			return 0

		iCivicOption = gc.getCivicInfo(iCivic).getCivicOptionType()

		# Set the previous widget
		iCivicPrev = self.m_paeCurrentCivics[iCivicOption]

		# Switch the widgets
		self.m_paeCurrentCivics[iCivicOption] = iCivic

		# Unhighlight the previous widget
		self.unHighlight(iCivicPrev)
		self.getScreen().setState(self.getCivicsButtonName(iCivicPrev), False)

		# highlight the new widget
		self.highlight(iCivic)
		self.getScreen().setState(self.getCivicsButtonName(iCivic), True)

		return 0
# End LPlate insertion - Tamriel
	# Draws the city list
	def drawCityInfo(self, iReligion):
		if (not self.bScreenUp):
			return

		if (iReligion == gc.getNumReligionInfos()):
			iLinkReligion = -1
		else:
			iLinkReligion = iReligion

		screen = self.getScreen()
# LPlate insertion - Tamriel
		iDivineRel = gc.getInfoTypeForString('RELIGION_EIGHT_DIVINES')
		iDaedraRel = gc.getInfoTypeForString('RELIGION_ISLAM')
		iNordicRel = gc.getInfoTypeForString('RELIGION_CHRISTIANITY')
		iAltmerRel = gc.getInfoTypeForString('RELIGION_JUDAISM')
		iTribunalRel = gc.getInfoTypeForString('RELIGION_TRIBUNAL')
		iCurrentReligion = self.pActivePlayer.getStateReligion()
		# Leave out row if do not have applicable religion
		if (iCurrentReligion != iDivineRel and iCurrentReligion != iDaedraRel and iCurrentReligion != iNordicRel and iCurrentReligion != iAltmerRel and iCurrentReligion != iTribunalRel):
			iYPos = self.Y_RELIGION_AREA + self.H_RELIGION_AREA + self.SPACING
		else:
			iYPos = self.Y_CITY_AREA
		szArea1 = self.AREA1_ID
		screen.addPanel(self.AREA1_ID, "", "", True, True, self.X_CITY1_AREA, iYPos, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)
		szArea2 = self.AREA2_ID
		screen.addPanel(self.AREA2_ID, "", "", True, True, self.X_CITY2_AREA, iYPos, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)
# End LPlate insertion - Tamriel
# LPlate Unmodified Code
#		szArea1 = self.AREA1_ID
#		screen.addPanel(self.AREA1_ID, "", "", True, True, self.X_CITY1_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)
#		szArea2 = self.AREA2_ID
#		screen.addPanel(self.AREA2_ID, "", "", True, True, self.X_CITY2_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)
# End LPlate Unmodified Code

		szArea = self.RELIGION_PANEL_ID
		for i in range(gc.getNumReligionInfos()):
			if (self.iReligionSelected == i):
				screen.setState(self.getReligionButtonName(i), True)
			else:
				screen.setState(self.getReligionButtonName(i), False)

		if (self.iReligionSelected == gc.getNumReligionInfos()):
			screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), True)
		else:
			screen.setState(self.getReligionButtonName(gc.getNumReligionInfos()), False)

		(szLeftCities, szRightCities) = self.getCityText(iLinkReligion)

# End LPlate insertion - Tamriel
		screen.addMultilineText("Child" + self.AREA1_ID, szLeftCities, self.X_CITY1_AREA + self.TEXT_SPACING, iYPos + self.TEXT_SPACING, self.TEXT_WIDTH, self.H_CITY_AREA - 2 * self.TEXT_SPACING, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addMultilineText("Child" + self.AREA2_ID, szRightCities, self.X_CITY2_AREA + self.TEXT_SPACING, iYPos + self.TEXT_SPACING, self.TEXT_WIDTH, self.H_CITY_AREA - 2 * self.TEXT_SPACING, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# End LPlate insertion - Tamriel
# LPlate Unmodified Code
#		screen.addMultilineText("Child" + self.AREA1_ID, szLeftCities, self.X_CITY1_AREA + self.TEXT_SPACING, self.Y_CITY_AREA + self.TEXT_SPACING, self.TEXT_WIDTH, self.H_CITY_AREA - 2 * self.TEXT_SPACING, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
#		screen.addMultilineText("Child" + self.AREA2_ID, szRightCities, self.X_CITY2_AREA + self.TEXT_SPACING, self.Y_CITY_AREA + self.TEXT_SPACING, self.TEXT_WIDTH, self.H_CITY_AREA - 2 * self.TEXT_SPACING, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
# End LPlate Unmodified Code

		# Convert Button....
		iLink = 0
		if (self.pActivePlayer.canChangeReligion()):
			iLink = 1

		if (not self.canConvert(iLinkReligion) or iLinkReligion == self.iReligionOriginal):
			screen.setText(self.CONVERT_NAME, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)
			screen.hide(self.CANCEL_NAME)
			szAnarchyTime = CyGameTextMgr().setConvertHelp(self.iActivePlayer, iLinkReligion)
		else:
# 11Jul LPlate commenting out			screen.setText(self.CONVERT_NAME, "Background", self.CONVERT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CONVERT, iLinkReligion, 1)
			screen.setText(self.CONVERT_NAME, "Background", self.CONVERT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_CONVERT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CONVERT, iLinkReligion, 1)# 11Jul LPlate - moving sideways to avoid text overlaps

			screen.show(self.CANCEL_NAME)
			szAnarchyTime = localText.getText("TXT_KEY_ANARCHY_TURNS", (self.pActivePlayer.getReligionAnarchyLength(), ))

		# Turns of Anarchy Text...
		screen.setLabel(self.RELIGION_ANARCHY_WIDGET, "Background", u"<font=3>" + szAnarchyTime + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_ANARCHY, self.Y_ANARCHY, self.Z_TEXT, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def getCityText(self, iLinkReligion):
		cityList = PyPlayer(self.iActivePlayer).getCityList()

		# Loop through the cities
# VET - NewChars - 1/1 - start
		szNoneIcon = self.getSpaces(22)
		#szNoneIcon = u"%c" %CyGame().getSymbolID(FontSymbols.TRANSPARENT_CHAR)
# VET - NewChars - 1/1 - end

		iWidth = 0 # Максимальная длина названия города в пикселях
		iMaxHeadRel = 0 # Максимальное количество святых религий в городе

		iNumRel = gc.getNumReligionInfos()
		mbNam = [[]] * iNumRel
		for i in range(iNumRel):
			mbNam[i] = false

		pLoopCity, iter = self.pActivePlayer.firstCity(false)
		while pLoopCity:
			iNam = CyInterface().determineWidth(pLoopCity.getName())
			if iNam > iWidth:
				iWidth = iNam
			iHeadRel = 0
			if pLoopCity.isCapital() or pLoopCity.isGovernmentCenter():
				iHeadRel += 1
			for iR in range(iNumRel):
				if pLoopCity.isHasReligion(iR):
					mbNam[iR] = true
					if pLoopCity.isHolyCityByType(iR):
						iHeadRel += 1

			if iHeadRel > iMaxHeadRel:
				iMaxHeadRel = iHeadRel
			pLoopCity, iter = self.pActivePlayer.nextCity(iter, false)
		szLeftCities = u""
		szRightCities = u""
		i = 0
		pCity, iter = self.pActivePlayer.firstCity(false)
		while pCity:
			iHeadRel = iMaxHeadRel
			bFirstColumn = (i % 2 == 0)
			if bFirstColumn:
				if szLeftCities:
					szLeftCities += u"\n"
			else:
				if szRightCities:
					szRightCities += u"\n"
			pLoopCity = cityList[i]

			# Constructing the City name...
			szCityName = u""
			if pLoopCity.isCapital():
				szCityName += u"%c" % CyGame().getSymbolID(FontSymbols.STAR_CHAR)
				iHeadRel -= 1
			elif pCity.isGovernmentCenter():
				szCityName += u"%c" %CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)
				iHeadRel -= 1
			lReligions = pLoopCity.getReligions()
			szBufer = u""
			for iR in range(iNumRel):
				if pCity.isHasReligion(iR) and pCity.isHolyCityByType(iR):
					iHeadRel -= 1
					szBufer += u"%c" %gc.getReligionInfo(iR).getHolyCityChar()
			while iHeadRel > 0:
				szCityName += szNoneIcon
				iHeadRel -= 1
			szCityName += szBufer + pCity.getName()
			iNam = CyInterface().determineWidth(pCity.getName())
			szCityName += self.getSpaces(iWidth - iNam)

			for iR in range(iNumRel):
				if mbNam[iR]:
					if pCity.isHasReligion(iR):
						if pCity.isHolyCityByType(iR):
							szCityName += u"%c" % gc.getReligionInfo(iR).getHolyCityChar()
						else:
							szCityName += u"%c" % gc.getReligionInfo(iR).getChar()
					else:
						szCityName += szNoneIcon
			szCityName += " "
			#szCityName += pLoopCity.getName()[0:17] + "  "
			if iLinkReligion == -1:
				bNotFirst = false
				for iI in range(len(lReligions)):
					szTempBuffer = CyGameTextMgr().getReligionHelpCity(lReligions[iI], pLoopCity.GetCy(), False, False, False, True)
					if szTempBuffer:
						if bNotFirst:
							szCityName += u", "
						szCityName += szTempBuffer
						bNotFirst = true
			else:
				szCityName += CyGameTextMgr().getReligionHelpCity(iLinkReligion, pLoopCity.GetCy(), False, False, True, False)

			if bFirstColumn:
				szLeftCities += szCityName
			else:
				szRightCities += szCityName
			i += 1
			pCity, iter = self.pActivePlayer.nextCity(iter, false)
		return szLeftCities, szRightCities

	def getReligionButtonName(self, iReligion):
		szName = self.BUTTON_NAME + str(iReligion)
		return szName

	def getReligionTextName(self, iReligion):
		szName = self.RELIGION_NAME + str(iReligion)
		return szName

	def canConvert(self, iReligion):
		iCurrentReligion = self.pActivePlayer.getStateReligion()
		if (iReligion == gc.getNumReligionInfos()):
			iConvertReligion = -1
		else:
			iConvertReligion = iReligion
		return (iConvertReligion != iCurrentReligion and self.pActivePlayer.canConvert(iConvertReligion))

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
			self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
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

	def getSpaces(self, iWidth):
		if iWidth < 1:
			return u""
		szImage = "Art/Interface/VetScreen/_.dds"
		szText = u""
		iImgSize = 14
		iNumSpases = iWidth / iImgSize
		iMinWidth = iWidth - iNumSpases * iImgSize
		while iNumSpases > 0:
			szText += "<img=%s size=%d></img>" %(szImage, iImgSize)
			iNumSpases -= 1
		if iMinWidth > 0:
			szText += "<img=%s size=%d></img>" %(szImage, iMinWidth)
		return szText
