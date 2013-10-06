import numpy as np

class Result:
		def __init__(self):
			self.clear()
			self._image = None

		def setImage(self, image):
			self._image = image

		def getImage(self):
			return self._image

		def noResult(self):
			return self._noResult

		def match(self):
			return self.match

		def noMatch(self):
			return self._noMatch

		def multFaces(self):
			return self._multFaces

		def noFace(self):
			return self._noFace

		def setNoResult(self):
			self.clear()
			self._noResult = True

		def setMatch(self):
			self.clear()
			self._match = True

		def setNoMatch(self):
			self.clear()
			self._noMatch = True

		def setMultFaces(self):
			self.clear()
			self._multFaces = True

		def setNoFace(self):
			self.clear()
			self._noFace = True

		def clear(self):
			self._noResult = False
			self._match = False
			self._noMatch = False
			self._multFaces = False
			self._noFace = False

result = Result()