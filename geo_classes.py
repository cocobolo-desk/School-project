import math


class GeoObject:
    """
    General class for a feature in a geoJSON file.
    """

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name


class Path(GeoObject):

    def __init__(self, coordinates, name, bicycle_friendly):
        """Initializing attributes
        :param list of coordinates for the path instance, name of path
        and bike-friendliness."""

        super().__init__(name)
        self.bicycle_friendly = bicycle_friendly
        self.coordinates = coordinates

        # iterates through all points (coordinates)
        # Creates an instance of the related class Point
        # and puts it in the list of the attribute "points"

    @property
    def bicycle_friendly(self):
        return self._bicycle_friendly

    @bicycle_friendly.setter
    def bicycle_friendly(self, is_bicycle_friendly):
        if not isinstance(is_bicycle_friendly, bool):
            raise ValueError('The bicycle-friendly parameter should be a boolean.')
        else:
            self._bicycle_friendly = is_bicycle_friendly

    @property
    def points(self):
        list_points = []
        for point in self.coordinates:
            list_points.append(Point(point[0], point[1]))
        return list_points

    def path_length(self):
        """
        Sums up the length of all path segments for
        the given path and returns the total.

        :return: The length of the path
        """
        total_distance = 0
        i = 1
        total_points = len(self.points)

        while i < total_points:
            total_distance += self.points[i - 1].distance(self.points[i])
            i += 1

        return total_distance

    def __len__(self):
        """
        len(Path) gives the number of points that make up the path
        The actual length of the path is given by path_length
        """
        return len(self.points)

    def __str__(self):
        """
        Returns the name, length and bike-friendliness of the path.
        """
        output = \
            f'\nPath name: {self._name}' + \
            f'\nPath length: {int(1000 * self.path_length())} m' + \
            f'\nBicycle-friendly: {self.bicycle_friendly}'
        return output


# class Building(GeoObject):


# class Area(GeoObject):


class Point:
    """Class to represent coordinates. Longitude and latitude are required."""
    def __init__(self, longitude, latitude):
        """Defines x and y variables"""

        self.longitude = longitude
        self.latitude = latitude

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        if not (type(longitude) == int or type(longitude) == float):
            raise TypeError('Longitude should be represented by a number.')
        if not -180 <= longitude <= 180:
            raise ValueError('Longitude should be in the interval -180 to 180 degrees')
        else:
            self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        if not (type(latitude) == int or type(latitude) == float):
            raise TypeError('Longitude should be represented by an number.')
        if not -90 <= latitude <= 90:
            raise ValueError('Longitude should be in the interval -180 to 180 degrees')
        else:
            self._latitude = latitude

    def __str__(self):
        return f'Longitude:{self.longitude}, Latitude:{self.latitude}'

    def distance(self, other):
        """Calculates the distance between self and other point."""
        dx = 111 * (self.longitude - other.longitude) * math.cos(self.latitude * math.pi / 180)
        dy = 111 * (self.latitude - other.latitude)  # Assumes that one degree corresponds to 111 km.
        return math.sqrt(dx ** 2 + dy ** 2)
