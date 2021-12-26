from CvPythonExtensions import *
gc = CyGlobalContext()

class UniqueCivics:
	def __init__(self,):
		self.Civics = [	["CIVILIZATION_NOVGOROD", "CIVIC_REPRESENTATION", "CIVIC_REPRESENTATION_NOVGOROD"],
				["CIVILIZATION_MUSCOVY", "CIVIC_HEREDITARY_RULE", "CIVIC_HEREDITARY_RULE_MUSCOVY"],
				]

	def checkUniqueCivics(self, iCivic, iPlayer):
		iCiv = gc.getPlayer(iPlayer).getCivilizationType()
		for i in self.Civics:
			iGenericCivic = gc.getInfoTypeForString(i[1])
			iSpecificCiv = gc.getInfoTypeForString(i[0])
			if iGenericCivic == -1: continue
			if iSpecificCiv == -1: continue
			if iCivic == iGenericCivic:
				if iCiv == iSpecificCiv: return True
			iUniqueCivic = gc.getInfoTypeForString(i[2])
			if iUniqueCivic == -1: continue
			if iCivic == iUniqueCivic:
				if iCiv != iSpecificCiv: return True
		return False