## Copyright (c) 2005-2006, Gillmer J. Derge.

## This file is part of Civilization IV Unit Allegiance Mod
##
## Civilization IV Unit Allegiance Mod is free software; you can redistribute
## it and/or modify it under the terms of the GNU General Public
## License as published by the Free Software Foundation; either
## version 2 of the License, or (at your option) any later version.
##
## Civilization IV Unit Allegiance Mod is distributed in the hope that it will
## be useful, but WITHOUT ANY WARRANTY; without even the implied
## warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Civilization IV Unit Allegiance Mod; if not, write to the Free
## Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
## 02110-1301 USA
	

from CvPythonExtensions import *
import CvUtil
import CvEventManager

## Below are Sub-Eventmanagers
import MongolCamp

gc = CyGlobalContext()
class CvCustomEventManager(CvEventManager.CvEventManager, object):

	CustomEvents = {}
		
	def __init__(self, *args, **kwargs):

		super(CvCustomEventManager, self).__init__(*args, **kwargs)
		# map the initial EventHandlerMap values into the new data structure
		for eventType, eventHandler in self.EventHandlerMap.iteritems():
			self.setEventHandler(eventType, eventHandler)
		
		# --> INSERT EVENT HANDLER INITIALIZATION HERE <--
		MongolCamp.MongolCamp(self)

	def beginEvent( self, context, argsList=-1 ):
		"Begin Event"
		if(self.CustomEvents.has_key(context)):
			return self.CustomEvents[context][2](argsList)
		else:
			return CvEventManager.CvEventManager.beginEvent(self, context, argsList)
			
	def applyEvent( self, argsList ):
		'Apply the effects of an event '
		context, playerID, netUserData, popupReturn = argsList
		
		if(self.CustomEvents.has_key(context)):
			entry = self.CustomEvents[context]
			# the apply function
			return entry[1]( playerID, netUserData, popupReturn )   
		else:
			return CvEventManager.CvEventManager.applyEvent(self, argsList)


	def addCustomEventDefinition(self, eventType, eventDefinition):
		self.CustomEvents[eventType] = eventDefinition

	def removeCustomEventDefinition(self, eventType):
		del self.CustomEvents[eventType]

	def setCustomEventDefinition(self, eventType, eventDefinition):
		self.CustomEvents[eventType] = eventDefinition

	def addEventHandler(self, eventType, eventHandler):
		"""Adds a handler for the given event type.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.

		"""
		self.EventHandlerMap[eventType].append(eventHandler)

	def removeEventHandler(self, eventType, eventHandler):
		"""Removes a handler for the given event type.
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  It is an error if 
		the given handler is not found in the list of installed handlers.

		"""
		self.EventHandlerMap[eventType].remove(eventHandler)
	
	def setEventHandler(self, eventType, eventHandler):
		"""Removes all previously installed event handlers for the given 
		event type and installs a new handler .
		
		A list of supported event types can be found in the initialization 
		of EventHandlerMap in the CvEventManager class.  This method is 
		primarily useful for overriding, rather than extending, the default 
		event handler functionality.

		"""
		self.EventHandlerMap[eventType] = [eventHandler]

	def setPopupHandler(self, eventType, popupHandler):
		"""Removes all previously installed popup handlers for the given 
		event type and installs a new handler.

		The eventType should be an integer.  It must be unique with respect
		to the integers assigned to built in events.  The popupHandler should
		be a list made up of (name, beginFunction, applyFunction).  The name
		is used in debugging output.  The begin and apply functions are invoked
		by beginEvent and applyEvent, respectively, to manage a popup dialog
		in response to the event.

		"""
		self.Events[eventType] = popupHandler

	def handleEvent(self, argsList):
		"""Handles events by calling all installed handlers."""
		self.origArgsList = argsList
		flagsIndex = len(argsList) - 6
		self.bDbg, self.bMultiPlayer, self.bAlt, self.bCtrl, self.bShift, self.bAllowCheats = argsList[flagsIndex:]		
		eventType = argsList[0]
		return {
			"kbdEvent": self._handleConsumableEvent,
			"mouseEvent": self._handleConsumableEvent,
			"OnSave": self._handleOnSaveEvent,
			"OnLoad": self._handleOnLoadEvent
		}.get(eventType, self._handleDefaultEvent)(eventType, argsList[1:])

	def _handleDefaultEvent(self, eventType, argsList):
		if self.EventHandlerMap.has_key(eventType):
			for eventHandler in self.EventHandlerMap[eventType]:
				# the last 6 arguments are for internal use by handleEvent
				eventHandler(argsList[:len(argsList) - 6])

	def _handleConsumableEvent(self, eventType, argsList):
		"""Handles events that can be consumed by the handlers, such as
		keyboard or mouse events.
		
		If a handler returns non-zero, processing is terminated, and no 
		subsequent handlers are invoked.

		"""
		if self.EventHandlerMap.has_key(eventType):
			for eventHandler in self.EventHandlerMap[eventType]:
				# the last 6 arguments are for internal use by handleEvent
				result = eventHandler(argsList[:len(argsList) - 6])
				if (result > 0):
					return result
		return 0

	# TODO: this probably needs to be more complex
	def _handleOnSaveEvent(self, eventType, argsList):
		"""Handles OnSave events by concatenating the results obtained
		from each handler to form an overall consolidated save string.

		"""
		result = ""
		if self.EventHandlerMap.has_key(eventType):
			for eventHandler in self.EventHandlerMap[eventType]:
				# the last 6 arguments are for internal use by handleEvent
				result = result + eventHandler(argsList[:len(argsList) - 6])
		return result

	# TODO: this probably needs to be more complex
	def _handleOnLoadEvent(self, eventType, argsList):
		"""Handles OnLoad events."""
		return self._handleDefaultEvent(eventType, argsList)
