from . import processor as proc
import copy

class convexHull:
    # This class includes methods which can return the convex hull of given points.
    # To get the convex hull, simply use get_hull method 

    def __init__(self):
        # initiate two empty lists of hull points' respective side
        self._hull_points = []
        self._hull_points_left = []
        self._hull_points_right = []
        self.proc = proc.processor()
        
    def get_hull(self, given_points):
        # Clear the 3 hull_points container (affected by main program iteration)
        self._clear_hull_containers()
        # Convert the type of given_points to list type
        given_points_list = given_points.tolist()
        # sort the given_points_list (in the form [x,y]) by the x, then y if there are equally x values between points. Both in ascending.
        given_points_list = sorted(given_points_list, key = lambda x: (x[0], x[1]))

        # Get the first_x point and last_x point
        first_x_point = given_points_list[0]
        last_x_point = given_points_list[len(given_points_list)-1]

        # first_x_point and last_x_point are hull points
        self._hull_points_left.append(first_x_point)
        self._hull_points_left.append(last_x_point)
        self._hull_points_right.append(first_x_point)
        self._hull_points_right.append(last_x_point)

        # These two lists collect the points which are on the left side or right side of a given line, respectively.
        pointsOnLeft = []
        pointsOnRight = []

        for point in (given_points_list):
            point_side = self.proc.whichSide(first_x_point, last_x_point, point)
            if (point_side == self.proc.LEFT):
                pointsOnLeft.append(point)
            elif (point_side == self.proc.RIGHT):
                pointsOnRight.append(point)
        # pointsOnLeft and pointsOnRight are fulfilled

        # Determining which points of given_points make up the convexHull
        # Divide and Conquer is implemented
        self._operateHull(first_x_point, last_x_point, pointsOnLeft, self._hull_points_left)
        self._operateHull(last_x_point, first_x_point, pointsOnRight, self._hull_points_right)

        return self._getHullPoints()

    def _operateHull(self, pi, pf, given_points, collect_hull_point):
        if (given_points):
            pointsOnLeft = []
            pointsOnRight = []

            # determining which point in given_points is the farthest from line by Pi and Pf
            idx_farthest = self.proc.idxFarthestPointFromLine(pi, pf,  given_points)
            point_farthest = copy.copy(given_points[idx_farthest])
            collect_hull_point.append(point_farthest)

            for point in given_points:
                isInside = self.proc.isInsideTriangle(pi, pf, point_farthest, point)
            # Eliminate points which are inside of triangle (Pi, point_farthest, given_points[idx_farthest])
                if (not isInside):
                    # if slope of line formed by pi and pf > 0, change orientation
                    point_side = self.proc.whichSide(pi, point_farthest, point)
                    if (point_side == self.proc.LEFT):
                        pointsOnLeft.append(point)
                    elif (point_side == self.proc.RIGHT):
                        pointsOnRight.append(point)
            # pointsOnRight and pointsOnLeft are gotten

            # Do _operateHull until given_points is empty
            self._operateHull(pi, point_farthest, pointsOnLeft, collect_hull_point)
            self._operateHull(point_farthest, pf, pointsOnRight, collect_hull_point)

    def _getHullPoints(self):
        self._hull_points_right = sorted(self._hull_points_right, key = lambda point: (point[0], point[1]), reverse = True)
        self._hull_points_left = sorted(self._hull_points_left, key = lambda point: (point[0], point[1]))
        self._hull_points.extend(self._hull_points_left)
        self._hull_points.extend(self._hull_points_right)
        # hull_points = 
        # [ [x1_left, y1_left], [x2_left, y2_left], ... [xn_left, yn_left], 
        #   [x1_right, y1_right], [x2_right, y2_right], ..., [xn_right, yn_right]   ]

        return self._modifyHullPoints()
        # hull_points = [[x1_left, ..., xn_left, x1_right, ..., xn_right], [y1_left, ..., yn_left, y1_right, ..., yn_right]]

    def _modifyHullPoints(self):
        x_container = []
        y_container = []
        for point in self._hull_points:
            x_container.append(point[0]) # x1_left, ..., xn_left, x1_right, ..., xn_right
            y_container.append(point[1]) # y1_left, ..., yn_left, y1_right, ..., yn_right
        
        self._hull_points.clear()
        self._hull_points.append(x_container)
        self._hull_points.append(y_container)

        return self._hull_points

    def _clear_hull_containers(self):
        self._hull_points.clear()
        self._hull_points_left.clear()
        self._hull_points_right.clear()

