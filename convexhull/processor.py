import copy
import numpy as np

class processor:
    LEFT = "left"
    RIGHT = "right"
    INTERSECT = "intersect"

    def __init__(self):
        pass

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Methods for determining which side a point is from a given line 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def whichSide(self, pi, pf, p_observed):
        # return which side P_Observed is from a line formed by Pi and Pf
        matrix = []

        firstRow_matrix = copy.copy(pi)
        secondRow_matrix = copy.copy(pf)
        thirdRow_matrix = copy.copy(p_observed)

        firstRow_matrix.append(1)
        secondRow_matrix.append(1)
        thirdRow_matrix.append(1)

        # build: matrix = [[xi, yi, 1], [xf, yf, 1], [x_observed, y_observed, 1]]
        matrix.append(firstRow_matrix)
        matrix.append(secondRow_matrix)
        matrix.append(thirdRow_matrix)

        # Determine which side p_Observed is from line of Pi and Pf by using determinant
        det = np.linalg.det(matrix)

        if (det < 0):
            return self.RIGHT
        elif (det == 0):
            return self.INTERSECT
        else:
            return self.LEFT

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Methods for determining which point of a given points is the farthest from a given line 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def idxFarthestPointFromLine(self, pi, pf, given_points):
        # Return index of a point from given_points which the point is the farthest from line formed by pi and pf
        point_max_distance = given_points[0]
        max_distance = self._distancePointToLine(pi, pf, point_max_distance)

        idx_farthest = 0
        idx_challenger = 0

        for point in given_points:
            # Eliminate the point that is the same as Pi or Pf
            if (point != pi and point != pf):
                # If distance of point > distance of current point_max_distance
                point_distance = self._distancePointToLine(pi, pf, point)
                if (point_distance > max_distance):
                    point_max_distance = point
                    max_distance = point_distance
                    idx_farthest = idx_challenger

                # If distance of given_points[i] = distance of current point_max_distance
                elif (point_distance == max_distance):
                    pointsComparing = [point, point_max_distance]
                    
                    # search for a point who has a bigger angle
                    idx_returned = self._idxTheBiggestAngle(pi, pf, pointsComparing)

                    # If angle of point in respect to line formed by Pi and Pf is bigger than angle of current point_max_distance to that line
                    if (idx_returned == 0):
                        idx_farthest = idx_challenger
                        point_max_distance = given_points[idx_farthest]
            
            idx_challenger += 1

        # idx_farthest is idx of the farthest point from the line
        return idx_farthest

    def _distancePointToLine(self, pi, pf, p_observed):
        # convert each type of points to the np.array
        p1 = np.array(pi)
        p2 = np.array(pf)
        p3 = np.array(p_observed)

        # calculate the shortest distance of p_observed to the line of pi and pf
        distance = np.abs(np.cross(p2-p1, p1-p3)) / np.linalg.norm(p2-p1)
        return distance
    
    def _idxTheBiggestAngle(self, pi, pf, given_points):
        # return the biggest angle of points from given points with respect to line of Pi and Pf
        biggestAngle = -1
        idx_biggestAngle = -1

        # idx is point's index identifier
        idx = 0

        for point in given_points:
            if(pi != point and pf != point):
                points = np.array([pi, pf, point])
                m = points[2] - points[0]
                n = points[1] - points[0]
                o = points[2] - points[1]

                angles = []
                for e1, e2 in ((m, n), (m, o), (n, -o)):
                    num = np.dot(e1, e2)
                    denom = np.linalg.norm(e1) * np.linalg.norm(e2)
                    angles.append(np.arccos(num/denom) * 180 / np.pi)

                if (angles[1] > biggestAngle):
                    biggestAngle = angles[1]
                    idx_biggestAngle = idx
            idx += 1

        # biggestAngle is gotten
        return idx_biggestAngle

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Methods for determining whether a point (pt) is inside of a triangle (v1, v2, v3) or not 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def isInsideTriangle (self, pi, pf, p_farthest, pt):
        b1 = self._sign(pt, pi, pf) < 0.0  
        b2 = self._sign(pt, pf, p_farthest) < 0.0  
        b3 = self._sign(pt, p_farthest, pi) < 0.0  
        return ((b1 == b2) and (b2 == b3))
        
    def _sign (self, pi, pf, p_farthest):
       return float((pi[0] - p_farthest[0]) * (pf[1] - p_farthest[1]) - (pf[0] - p_farthest[0]) * (pi[1] - p_farthest[1]))