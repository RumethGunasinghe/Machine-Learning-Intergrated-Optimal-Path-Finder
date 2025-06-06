class Location:
    def __init__(self, name, latitude, longitude, direction, located_on, compared_to):
        self.name = name.strip()
        self.located_on = located_on.strip()
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.direction = direction
        self.compared_to = compared_to.strip()

    def __repr__(self):
        return f"{self.name} ({self.latitude}, {self.longitude}) | Dir: {self.direction}, On: {self.located_on}, ComparedTo: {self.compared_to}"
