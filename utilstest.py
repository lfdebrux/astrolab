"""
unit test for utils.py, based on 
http://www.diveintopython.net/unit_testing/romantest.html
"""

import utils
import unittest

class KnownValues(unittest.TestCase):
	knownRaValues = ( (('18','36','56'),18.616,279.23),
					  (('20','41','26'),20.691,310.36),
					  (('12','26','36'),12.443,186.65)
					)

	knownDecValues = ( (('38','46','59'),38.783),
					   (('45','16','49'),45.28),
					   (('-63','5','57'),-63.099)
					 )

	def testToKnownRaHrValues(self):
		"""
		ra2hr should give known result to known input,
		within error
		"""

		for ra,hr,deg in self.knownRaValues:
			result = utils.ra2hr(ra)
			self.assertAlmostEqual(hr,result,places=2)

	def testToKnownRaDegValues(self):
		"""
		ra2hr should give known result to known input,
		within error
		"""

		for ra,hr,deg in self.knownRaValues:
			result = utils.ra2deg(ra)
			self.assertAlmostEqual(deg,result,places=2)

	def testToKnownDecValues(self):
		"""
		dec2deg should give known result to known input,
		within error
		"""

		for dec,deg in self.knownDecValues:
			result = utils.dec2deg(dec)
			self.assertAlmostEqual(deg,result,places=2)


if __name__ == '__main__':
	unittest.main()