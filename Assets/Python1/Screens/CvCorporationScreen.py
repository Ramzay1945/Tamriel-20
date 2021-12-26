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

class CvCorporationScreen:
	"Corporation Advisor Screen"

	def __init__(self):

		self.SCREEN_NAME = "CorporationScreen"
		self.BUTTON_NAME = "CorporationScreenButton"
		self.CORPORATION_NAME = "CorporationText"
		self.CITY_NAME = "CorporationCity"
		self.HEADER_NAME = "CorporationScreenHeader"
		self.DEBUG_DROPDOWN_ID =  "CorporationDropdownWidget"
		self.AREA1_ID =  "CorporationAreaWidget1"
		self.AREA2_ID =  "CorporationAreaWidget2"
		self.BACKGROUND_ID = "CorporationBackground"
		self.CORPORATION_PANEL_ID = "CorporationPanel"
		self.EXIT_NAME = "CorporationExitButton"
		self.SCROLL_NAME = "CorporationScroll"

		self.SPACING = 10				# Растояние между элементами экрана
		self.CORPORATION_SPACING = 70	# Дополнительная длинна области под кнопки корпораций
		self.MIN_DX_CORPORATION = 100	# Минимальное растояние между кнопками корпораций
		self.MAX_DX_CORPORATION = 120	# Максимальное растояние между кнопками корпораций, при котором сохраняется изображение в 2 уровня
		self.H_ROW = 16					# Растояние между рядами ресурсов и городов-оснавателей
		self.TEXT_SPACING = 5

		self.H_PANEL = 55
		self.Y_TOP_PANEL = -2

		self.BORDER_WIDTH = 2
		self.BUTTON_SIZE = 48

		self.Y_TITLE = 8
		self.Z_TEXT = -6.3
		self.DZ = -0.2

		self.LEFT_EDGE_TEXT = 5
		self.X_CORPORATION_START = 155
		self.Y_CORPORATION = 35
		self.Y_FOUNDED = 126
		self.Y_HEADQUARTERS = 174

		self.X_CORPORATION_AREA = self.SPACING
		self.Y_CORPORATION_AREA = self.Y_TOP_PANEL + self.H_PANEL + self.SPACING
		self.H_CORPORATION_AREA = 215

		self.X_CITY1_AREA = self.SPACING
		self.Y_CITY_AREA = self.Y_CORPORATION_AREA + self.H_CORPORATION_AREA + self.SPACING

		self.X_CITY = self.SPACING

		self.iCorporationExamined = -1
		self.iCorporationSelected = -1
		self.iCorporationOriginal = -1
		self.iActivePlayer = -1

		self.bScreenUp = False

		self.CorporationScreenInputMap = {
			self.CORPORATION_NAME	: self.CorporationScreenButton,
			self.EXIT_NAME			: self.Exit,
			self.BUTTON_NAME		: self.CorporationScreenButton,
			}

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, CvScreenEnums.CORPORATION_SCREEN)

	def interfaceScreen (self):
		self.SCREEN_ART = ArtFileMgr.getInterfaceArtInfo("TECH_BG").getPath()
		self.EXIT_TEXT = u"<font=4>" + localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>"

		self.iActivePlayer = gc.getGame().getActivePlayer()
		self.pActivePlayer = gc.getPlayer(self.iActivePlayer)

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
		while i < gc.getNumCorporationInfos():
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

		iWidth = self.X_CORPORATION_START + self.CORPORATION_SPACING + self.MAX_DX_CORPORATION * (gc.getNumCorporationInfos() - 1) + 2 * self.SPACING
		if iWidth > self.W_SCREEN:
			self.W_SCREEN = iWidth
		if self.W_SCREEN > iXResolution:
			self.W_SCREEN = iXResolution

	#	if self.W_CITY_AREA < 70:
	#		self.W_CITY_AREA = 70
	#		self.TEXT_WIDTH = self.W_CITY_AREA - 2 * self.TEXT_SPACING
		self.X_CITY1_AREA = (self.W_SCREEN - self.SPACING) / 2 - self.W_CITY_AREA # (self.W_SCREEN - self.SPACING - 2 * self.W_CITY_AREA) / 2
		self.X_CITY2_AREA = self.X_CITY1_AREA + self.W_CITY_AREA + self.SPACING # (self.W_SCREEN + self.SPACING) / 2

		self.W_CORPORATION_AREA = self.W_SCREEN - 2 * self.SPACING
		if gc.getNumCorporationInfos() > 1:
			self.DX_CORPORATION = (self.W_CORPORATION_AREA - self.X_CORPORATION_START - self.CORPORATION_SPACING) / (gc.getNumCorporationInfos() - 1)
		else:
			self.DX_CORPORATION = 0

		self.Y_BOTTOM_PANEL = self.H_SCREEN - self.H_PANEL

		self.X_EXIT = self.W_SCREEN - 2 * self.SPACING
		self.Y_EXIT = self.H_SCREEN - 42

		# Set the background and exit button, and show the screen
		#screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setDimensions((iXResolution - self.W_SCREEN) / 2, (iYResolution - self.H_SCREEN) / 2, self.W_SCREEN, self.H_SCREEN)

		screen.addDDSGFC(self.BACKGROUND_ID, ArtFileMgr.getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, self.Y_TOP_PANEL, self.W_SCREEN, self.H_PANEL, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, self.Y_BOTTOM_PANEL, self.W_SCREEN, self.H_PANEL, PanelStyles.PANEL_STYLE_BOTTOMBAR )

		screen.showWindowBackground(False)

		# Make the scrollable areas for the city list...
		if (CyGame().isDebugMode()):
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
			for j in range(gc.getMAX_PLAYERS()):
				if (gc.getPlayer(j).isAlive()):
					screen.addPullDownString(self.szDropdownName, gc.getPlayer(j).getName(), j, j, False )

		# Put everything on a scrollable area
		screen.addPanel(self.CORPORATION_PANEL_ID, "", "", False, True, self.X_CORPORATION_AREA, self.Y_CORPORATION_AREA, self.W_CORPORATION_AREA, self.H_CORPORATION_AREA, PanelStyles.PANEL_STYLE_MAIN)

		# Make the scrollable area for the civics list...
		screen.addScrollPanel(self.SCROLL_NAME, u"", self.X_CORPORATION_AREA, self.Y_CORPORATION_AREA, self.W_CORPORATION_AREA, self.H_CORPORATION_AREA - 9, PanelStyles.PANEL_STYLE_EXTERNAL )
		#screen.setActivation(self.SCROLL_NAME, ActivationTypes.ACTIVATE_NORMAL )

		# Draw Corporation info
		self.drawCorporationInfo()
		self.drawCityInfo(self.iCorporationSelected)

	# Draws the Corporation buttons and information
	def drawCorporationInfo(self):
		if self.DX_CORPORATION < self.MAX_DX_CORPORATION:
			k = 8
			if self.DX_CORPORATION < self.MIN_DX_CORPORATION:
				self.DX_CORPORATION = self.MIN_DX_CORPORATION
		else:
			k = 0

		self.Y_mGREAT_PERSON = [62 - k , 62 + k]
		self.Y_mBONUSES = [94 - k, 94 + k]
		self.Y_mFOUNDED = [self.Y_FOUNDED - k, self.Y_FOUNDED + k]
		self.Y_mHEADQUARTERS = [self.Y_HEADQUARTERS - k, self.Y_HEADQUARTERS + k]

		screen = self.getScreen()
		szArea = self.SCROLL_NAME

		xLoop = self.X_CORPORATION_START
		for i in range(gc.getNumCorporationInfos()):
			k = i % 2
		# Button
			szButtonName = self.getCorporationButtonName(i)
			screen.addCheckBoxGFCAt(szArea, szButtonName, gc.getCorporationInfo(i).getButton(), ArtFileMgr.getInterfaceArtInfo("BUTTON_HILITE_SQUARE").getPath(), xLoop - self.BUTTON_SIZE/2, self.Y_CORPORATION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1, ButtonStyles.BUTTON_STYLE_LABEL, False)
			if gc.getGame().getCorporationGameTurnFounded(i) > -1:
				screen.enable(szButtonName, true)
			#	screen.setActivation(szButtonName, ActivationTypes.ACTIVATE_NORMAL )
			else:
				screen.enable(szButtonName, false)
		#		screen.setImageButtonAt(szArea, szButtonName, gc.getReligionInfo(i).getButton(), xLoop - self.BUTTON_SIZE/2, self.Y_RELIGION - self.BUTTON_SIZE/2, self.BUTTON_SIZE, self.BUTTON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1)
			#	screen.setActivation(szButtonName, ActivationTypes.ACTIVATE_NORMAL )

		# Great Person
			szGreatPerson = ""
			for iBuilding in range(gc.getNumBuildingInfos()):
				if (gc.getBuildingInfo(iBuilding).getFoundsCorporation() == i):
					break
			for iUnit in range(gc.getNumUnitInfos()):
				if gc.getUnitInfo(iUnit).getBuildings(iBuilding) or gc.getUnitInfo(iUnit).getForceBuildings(iBuilding):
					szGreatPerson = gc.getUnitInfo(iUnit).getDescription()
					break
			screen.setLabelAt("", szArea, szGreatPerson, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mGREAT_PERSON[k], self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Bonuses
			szListLabels = []
			iNum = 0
			szList = u""
			for iRequired in range(gc.getDefineINT("NUM_CORPORATION_PREREQ_BONUSES")):
				eBonus = gc.getCorporationInfo(i).getPrereqBonus(iRequired)
				if -1 != eBonus:
					if iNum == 0:
						szList = u""
					else:
						szList += u", "
					iNum += 1
					szList += u"%c" % (gc.getBonusInfo(eBonus).getChar(), )
					if iNum > 3:
						iNum = 0
						szListLabels.append(szList)
						szList = u""
			if len(szList) > 0:
				szListLabels.append(szList)
			iRow = 0
			for szList in szListLabels:
				screen.setLabelAt("", szArea, szList, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mBONUSES[k] + iRow, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				iRow += self.H_ROW

		# Date Founded
			if (gc.getGame().getCorporationGameTurnFounded(i) < 0):
				szFounded = localText.getText("TXT_KEY_RELIGION_SCREEN_NOT_FOUNDED", ())
			else:
				szFounded = CyGameTextMgr().getTimeStr(gc.getGame().getCorporationGameTurnFounded(i), false)
			screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mFOUNDED[k], self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# Headquarters
			pHeadquarters = gc.getGame().getHeadquarters(i)
			if pHeadquarters.isNone():
				szFounded = u"-"
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHEADQUARTERS[k], self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			elif not pHeadquarters.isRevealed(self.pActivePlayer.getTeam(), False):
				szFounded = localText.getText("TXT_KEY_UNKNOWN", ())
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHEADQUARTERS[k], self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				szFounded = pHeadquarters.getName()
				screen.setLabelAt("", szArea, "(%s)" % gc.getPlayer(pHeadquarters.getOwner()).getCivilizationAdjective(0), CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHEADQUARTERS[k]+self.H_ROW, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				screen.setLabelAt("", szArea, szFounded, CvUtil.FONT_CENTER_JUSTIFY, xLoop, self.Y_mHEADQUARTERS[k]-self.H_ROW, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			xLoop += self.DX_CORPORATION

	# Founded
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_RELIGION_SCREEN_DATE_FOUNDED", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_FOUNDED, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
	# Headquarters
		screen.setLabelAt("", szArea, localText.getText("TXT_KEY_CORPORATION_SCREEN_HEADQUARTERS", ()), CvUtil.FONT_LEFT_JUSTIFY, self.LEFT_EDGE_TEXT, self.Y_HEADQUARTERS, self.DZ, FontTypes.SMALL_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		self.iCorporationSelected = -1
		self.iCorporationExamined = self.iCorporationSelected
		self.iCorporationOriginal = self.iCorporationSelected

	# Draws the city list
	def drawCityInfo(self, iCorporation):
		if (not self.bScreenUp):
			return

		screen = self.getScreen()

		if (iCorporation == gc.getNumCorporationInfos()):
			iLinkCorporation = -1
		else:
			iLinkCorporation = iCorporation

		szArea1 = self.AREA1_ID
		screen.addPanel(self.AREA1_ID, "", "", True, True, self.X_CITY1_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)

		szArea2 = self.AREA2_ID
		screen.addPanel(self.AREA2_ID, "", "", True, True, self.X_CITY2_AREA, self.Y_CITY_AREA, self.W_CITY_AREA, self.H_CITY_AREA, PanelStyles.PANEL_STYLE_MAIN)

		szArea = self.CORPORATION_PANEL_ID
		for i in range(gc.getNumCorporationInfos()):
			if (self.iCorporationSelected == i):
				screen.setState(self.getCorporationButtonName(i), True)
			else:
				screen.setState(self.getCorporationButtonName(i), False)

		# Loop through the cities
		(szLeftCities, szRightCities) = self.getCityText(iCorporation)
		screen.addMultilineText("Child" + self.AREA1_ID, szLeftCities, self.X_CITY1_AREA + self.TEXT_SPACING, self.Y_CITY_AREA + self.TEXT_SPACING, self.TEXT_WIDTH, self.H_CITY_AREA - 2 * self.TEXT_SPACING, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.addMultilineText("Child" + self.AREA2_ID, szRightCities, self.X_CITY2_AREA + self.TEXT_SPACING, self.Y_CITY_AREA + self.TEXT_SPACING, self.TEXT_WIDTH, self.H_CITY_AREA - 2 * self.TEXT_SPACING, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)

		# Header...
		if self.iCorporationExamined != -1:
			screen.setLabel(self.HEADER_NAME, "Background", u"<font=4b>" + gc.getCorporationInfo(self.iCorporationExamined).getDescription().upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_SCREEN / 2, self.Y_TITLE, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setLabel(self.HEADER_NAME, "Background", u"<font=4b>" + localText.getText("TXT_KEY_CORPORATION_SCREEN_TITLE", ()).upper() + u"</font>", CvUtil.FONT_CENTER_JUSTIFY, self.W_SCREEN / 2, self.Y_TITLE, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setText(self.EXIT_NAME, "Background", self.EXIT_TEXT, CvUtil.FONT_RIGHT_JUSTIFY, self.X_EXIT, self.Y_EXIT, self.Z_TEXT, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, 1, 0)

	def getCityText(self, iLinkCorporation):
		pPlayer = PyPlayer(self.iActivePlayer)
		cityList = pPlayer.getCityList()

		# Loop through the cities
# VET - NewChars - 1/1 - start
		szNoneIcon = self.getSpaces(22)
		#szNoneIcon = u"%c" %CyGame().getSymbolID(FontSymbols.TRANSPARENT_CHAR)
# VET - NewChars - 1/1 - end
		pPlayer = gc.getPlayer(gc.getGame().getActivePlayer())

		iWidth = 0 # Максимальная длина названия города в пикселях
		iMaxHeadCorp = 0 # Максимальное количество штабов корпораций в городе

		iNumCorp = gc.getNumCorporationInfos()
		mbNam = [[]] * iNumCorp
		for i in range(iNumCorp):
			mbNam[i] = false

		pLoopCity, iter = pPlayer.firstCity(false)
		while pLoopCity:
			iNam = CyInterface().determineWidth(pLoopCity.getName())
			if iNam > iWidth:
				iWidth = iNam
			iHeadCorp = 0
			if pLoopCity.isCapital() or pLoopCity.isGovernmentCenter():
				iHeadCorp += 1
			for iC in range(iNumCorp):
				if pLoopCity.isHeadquartersByType(iC):
					iHeadCorp += 1
					mbNam[iC] = true
				elif pLoopCity.isActiveCorporation(iC):
					mbNam[iC] = true
			if iHeadCorp > iMaxHeadCorp:
				iMaxHeadCorp = iHeadCorp
			pLoopCity, iter = pPlayer.nextCity(iter, false)
		szLeftCities = u""
		szRightCities = u""
		i = 0
		pCity, iter = pPlayer.firstCity(false)
		while pCity:
			iHeadCorp = iMaxHeadCorp
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
				szCityName += u"%c" %CyGame().getSymbolID(FontSymbols.STAR_CHAR)
				iHeadCorp -= 1
			elif pCity.isGovernmentCenter():
				szCityName += u"%c" %CyGame().getSymbolID(FontSymbols.SILVER_STAR_CHAR)
				iHeadCorp -= 1
			lCorporations = pLoopCity.getCorporations()
			szBufer = u""
			for iC in range(iNumCorp):
				if pCity.isHeadquartersByType(iC):
					iHeadCorp -= 1
					szBufer += u"%c" %gc.getCorporationInfo(iC).getHeadquarterChar()
			while iHeadCorp > 0:
				szCityName += szNoneIcon
				iHeadCorp -= 1
			szCityName += szBufer + pCity.getName()
			iNam = CyInterface().determineWidth(pCity.getName())
			szCityName += self.getSpaces(iWidth - iNam)

			for iC in range(iNumCorp):
				if mbNam[iC]:
					if pCity.isHeadquartersByType(iC):
						szCityName += u"%c" %gc.getCorporationInfo(iC).getHeadquarterChar()
					elif pCity.isActiveCorporation(iC):
						szCityName += u"%c" %gc.getCorporationInfo(iC).getChar()
					else:
						szCityName += szNoneIcon
			szCityName += " "
			#szCityName += pLoopCity.getName()[0:17] + "  "
			if iLinkCorporation == -1:
				bNotFirst = false
				for iI in range(len(lCorporations)):
					szTempBuffer = CyGameTextMgr().getCorporationHelpCity(lCorporations[iI], pLoopCity.GetCy(), False, False)
					if szTempBuffer:
						if bNotFirst:
							szCityName += u", "
						szCityName += szTempBuffer
						bNotFirst = true
			else:
				szCityName += CyGameTextMgr().getCorporationHelpCity(iLinkCorporation, pLoopCity.GetCy(), False, True)

			if bFirstColumn:
				szLeftCities += szCityName
			else:
				szRightCities += szCityName
			i += 1
			pCity, iter = pPlayer.nextCity(iter, false)
		return szLeftCities, szRightCities

	def Exit(self, inputClass):
		screen = self.getScreen()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED) :
			screen.hideScreen()

	def getCorporationButtonName(self, iCorporation):
		szName = self.BUTTON_NAME + str(iCorporation)
		return szName

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			screen = self.getScreen()
			iIndex = screen.getSelectedPullDownID(self.DEBUG_DROPDOWN_ID)
			self.iActivePlayer = screen.getPullDownData(self.DEBUG_DROPDOWN_ID, iIndex)
			self.pActivePlayer = gc.getPlayer(self.iActivePlayer)
			self.drawCorporationInfo()
			self.drawCityInfo(self.iCorporationSelected)
			return 1
		elif (self.CorporationScreenInputMap.has_key(inputClass.getFunctionName())):
			'Calls function mapped in CorporationScreenInputMap'
			# only get from the map if it has the key

			# get bound function from map and call it
			self.CorporationScreenInputMap.get(inputClass.getFunctionName())(inputClass)
			return 1
		return 0

	def update(self, fDelta):
		return

	# Corporation Button
	def CorporationScreenButton( self, inputClass ):
		if ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ) :
			if self.iCorporationSelected == inputClass.getID():
				self.iCorporationSelected = -1
			else:
				self.iCorporationSelected = inputClass.getID()
			self.iCorporationExamined = self.iCorporationSelected
			self.drawCityInfo(self.iCorporationSelected)
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_ON ) :
			self.iCorporationExamined = inputClass.getID()
			self.drawCityInfo(self.iCorporationExamined)
		elif ( inputClass.getNotifyCode() == NotifyCode.NOTIFY_CURSOR_MOVE_OFF ) :
			self.iCorporationExamined = self.iCorporationSelected
			self.drawCityInfo(self.iCorporationSelected)
		return 0

	def getSpaces(self, iWidth):
		if iWidth < 1:
			return u""
		szImage = "Art/Interface/VetScreen/_.dds"
		szText = u""
		iImgSize = 16
		iNumSpases = iWidth / iImgSize
		iMinWidth = iWidth - iNumSpases * iImgSize
		while iNumSpases > 0:
			szText += "<img=%s size=%d></img>" %(szImage, iImgSize)
			iNumSpases -= 1
		if iMinWidth > 0:
			szText += "<img=%s size=%d></img>" %(szImage, iMinWidth)
		return szText
