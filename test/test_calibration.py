 
#!/usr/bin/env python3
""" Unit testing calibration.py """
import rospy
import numpy
import unittest
from can_sort.calibration import Calibration # TODO

class TestCalibration(unittest.TestCase):
    """ Checks the python calibration library
    """
    def __init__(self, *args, **kwargs): # TODO
        super(TestCalibration, self).__init__(*args, **kwargs)
        self.point1_pix = [722.5, 937.5, 0]           # first calibration point [pixels] - measured from the image, z in not relevant
        self.point2_pix = [403.5, 417.5, 0]           # second calibration point [pixels] - measured from the image, z in not relevant
        self.point1_measure = [0.55, -0.50, 0]        # first calibration point [meters] - measured in the lab, z in not relevant
        self.point2_measure = [0.80, -0.10, 0]       # second calibration point [meters] - measured in the lab, z in not relevant
        self.calibration = Calibration(self.point1_pix, self.point2_pix)

    def test_equal_values_on_init(self):
        """ Function to check the python calibration library.
        We know the pixel-to-meter convertion for the following points from measurments in the lab:
        point1 = (722.5, 937.5, _)[pixels] = (0.55, -0.50, _)[meters], (z in not relevant)
        point2 = (403.5, 417.5, _)[pixels] = (0.80, -0.10, _)[meters], (z in not relevant)
        So we can check the calibration library using those two points.
        """
        # Find the linearization constants
        a, b, m, n = self.calibration.convert_position(self.point1_pix, self.point2_pix)

        # Calculate the new (x, y) for both point using linear equations (in meters)
        x1 = m*self.point1_pix[0] + n
        x2 = m*self.point2_pix[0] + n
        y1 = a*self.point1_pix[1] + b
        y2 = a*self.point2_pix[1] + b

        # Test the calibraion
        numpy.testing.assert_almost_equal([x1, y1], [self.point1_measure[0], self.point1_measure[1]], decimal = 2)
        numpy.testing.assert_almost_equal([x2, y2], [self.point2_measure[0], self.point2_measure[1]], decimal = 2)

if __name__ == "__main__":
    import rosunit
    rosunit.unitrun(can_sort, "test_calibration", TestCalibration)