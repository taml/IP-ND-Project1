"""The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, these objects handle all of the quirks of the data set,
such as missing names and unknown diameters.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but populated in the `NEODatabase`
    constructor.
    """
    def __init__(self, designation, name = None, diameter = 0.0, hazardous = False):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation of the NEO (string).
        :param name: The name of the NEO (string or None).
        :param diameter: The diameter of the NEO (float or float('nan')).
        :param hazardous: Whether the NEO is hazardous (string 'Y', 'N' or None).
        """
        self.designation = designation
        self.name = name if name else None
        self.diameter = float(diameter) if diameter else float('nan')
        self.hazardous = (hazardous == 'Y')

        # Empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})" if self.name else self.designation

    def serialize(self):
        """Return `dict(self)`, a serialized representation of this NEO."""
        return {'designation': self.designation, 'name': self.name, 'diameter_km': self.diameter, 'potentially_hazardous': self.hazardous}

    def __str__(self):
        """Return `str(self)`, a human-readable representation of this NEO."""
        hazard_status = "is" if self.hazardous else "is not"
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {hazard_status} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, _designation, time, distance, velocity):
        """Create a new `CloseApproach`.

        :param _designation: The primary designation of the NEO (string).
        :param time: The date and time of the NEO (NASA date/time).
        :param distance: The distance of the NEO (float).
        :param velocity: The velocity of the NEO (float).
        """
        self._designation = _designation
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Attribute for the referenced NEO.
        self.neo = None

    @property
    def time_str(self):
        """Return `str(self)`, a formatted representation of this `CloseApproach`'s
        approach time.

        While a `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't
        exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def serialize(self):
        """Return `dict(self)`, a serialized representation of this `CloseApproach`."""
        return {'datetime_utc': self.time, 'distance_au': self.distance, 'velocity_km_s': self.velocity}

    def __str__(self):
        """Return `str(self)`, a human-readable representation of this `CloseApproach`."""
        return f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
