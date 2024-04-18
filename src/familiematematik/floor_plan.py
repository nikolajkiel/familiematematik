# utf-8
import svg
WALL_THICKNESS = 0.1


class Room:
    """
    A class to represent a room in a building.
    All units are in meters [m].

    Attributes:
    -----------
    width : float
        The width of the room.
    length : float
        The length of the room.
    height : float
        The height of the room.
    location : tuple
        The location of the room in the building.

    Examples:
    ---------
    >>> room = Room(2.5, 3.5)
    >>> room.location
    [0, 0]
    """
    def __init__(self, width, length, name=None, location=(0,0), rect_kwargs={}):
        self.width = width
        self.length = length
        self.name = name
        self._location = location
        self.rect_kwargs = rect_kwargs

    def __repr__(self):
        return f"Room({self.width}, {self.length}, {self.name}, {self._location})"
    
    # @staticmethod
    def resolve_location(self, dir=0):
        xy = self._location[dir]
        if not isinstance(xy, Room):
            return xy
        else:
            wd = xy.width if dir == 0 else xy.length
            if dir == 0:
                return xy.location[dir] + WALL_THICKNESS + wd
            elif dir == 1:
                return xy.location[dir] - WALL_THICKNESS - wd


    @property
    def location(self):
        resolved_location = []
        for dir, xy in enumerate(self._location):
            resolved_location.append(self.resolve_location(dir=dir))

        return resolved_location
    
    # @property
    # def loc(self):
    #     """Flipped y-axis"""
    #     return (self.location[0], -self.location[1])


class FloorPlan:
    """
    A class to represent a floor plan of a building.
    All units are in meters [m].

    Attributes
    ----------
    rooms : list
        A list of Room objects.

    Examples
    --------
    >>> FloorPlan()
    FloorPlan([], (0, -10, 22, 10))
    
    >>> fp = FloorPlan()
    ... room1 = Room(2.5, 3.5, name="Room 1", rect_kwargs={"fill": "red"})
    ... room2 = Room(2.5, 3.5, name="Room 2", location=(room1, 0), rect_kwargs={"fill": "blue"})
    ... room3 = Room(7.8, 3.9, name="Room 3", location=(room2, 0), rect_kwargs={"fill": "green"})
    ... room4 = Room(2.7, 3.5, name="Room 4", location=(room2, room3), rect_kwargs={"fill": "yellow"})
    ... room5 = Room(5.1, 1.5, name="Room 5", location=(0, room1), rect_kwargs={"fill": "orange"})
    ... room6 = Room(5, 3.9, name="Room 6", location=(room3, 0), rect_kwargs={"fill": "purple"})
    ... rooms = [room1, room2, room3, room4, room5, room6]
    ... for room in rooms:
    ...     fp.add_room(room)
    ... fp
    FloorPlan([Room(2.5, 3.5, 'Room 1', (0, 0)), Room(2.5, 3.5, 'Room 2', (2.6, 0)), Room(7.8, 3.9, 'Room 3', (5.1, 0)), Room(2.7, 3.5, 'Room 4', (2.6, 3.9)), Room(5.1, 1.5, 'Room 5', (0, 3.5)), Room(5, 3.9, 'Room 6', (5.1, 3.9))], (0, -10, 22, 10))

    Returns
    -------
    FloorPlan
    """

    def __init__(self, viewbox=(0, -10, 22, 10)):
        self.rooms = []
        self.elements = []
        self.viewbox = viewbox

    def __repr__(self):
        return f"FloorPlan({self.rooms}, {self.viewbox})"
    
    def get_show_title(self):
        return """
        function showTitle(evt) {
            var title = evt.target.getAttributeNS(null, "title");
            var titleText = document.createTextNode(title);
            var titleElement = document.createElementNS("http://www.w3.org/2000/svg", "title");
            titleElement.appendChild(titleText);
            evt.target.appendChild(titleElement);
        }
        """

    def add_room(self, room: Room, first=[True]):
        self.rooms.append(room)

    def location_resolve(self):
        ...


    def grid(self, xspace=5, yspace=5):
        """
        return a grid of the floor plan
        as elements
        """
        grid_x, grid_y = [], []
        for x in range(self.viewbox[0], (self.viewbox[2] - self.viewbox[0]), xspace):
            grid_x.append(svg.Line(
                x1=x, y1=self.viewbox[1], x2=x, y2=self.viewbox[3],
                stroke="black",
                stroke_width=0.01
            ))
        
        for y in range(self.viewbox[1], (self.viewbox[3] - self.viewbox[1]), yspace):
            grid_y.append(svg.Line(
                x1=self.viewbox[0], y1=y, x2=self.viewbox[2], y2=y,
                stroke="black",
                stroke_width=0.01
            ))

        group = svg.G(elements=grid_x + grid_y)
        return group


    def draw(self) -> svg.SVG:
        for room in self.rooms:
            print(f"Make grid")
            self.elements.append(self.grid())
            print(f"Drawing room at location {room.location} with width {room.width} and length {room.length}.")
            # Draw the room
            rect_kwargs = dict(fill="none",
                stroke="black",
                stroke_width=WALL_THICKNESS) | room.rect_kwargs
            rect = svg.elements.Rect(
                x=room.location[0],
                y=room.location[1] - room.length,
                width=room.width + WALL_THICKNESS,
                height=abs(room.length) + WALL_THICKNESS,
                **rect_kwargs
            )
            text = svg.elements.Text(
                class_="title",
                x=room.location[0] + room.width/2 + WALL_THICKNESS/2,
                y=room.location[1] - room.length/2 + WALL_THICKNESS/2,
                text=room.name,
                font_size=0.3,
                text_anchor="middle",
                onmouseover="showTitle(evt)",
            )
            # call method to add title on hover
            group = svg.G(class_='room',
                elements=[rect, text],
                # onmouseover="showTitle(evt)",
            )
            self.elements.append(group)
        
        # self.svg.save("floor_plan.svg")
        # script = svg.elements.Script(self.get_show_title())
        # self.elements.append(script)
        canvas =  svg.SVG(
            viewBox=svg.ViewBoxSpec( *self.viewbox),
            # unit
            width="100%",
            height="100%",
            elements=self.elements,
    )
        with open("floor_plan.svg", 'w') as fout:
            fout.write(str(canvas))
        # append show_title function
        return canvas
    

if __name__ == "__main__":
    # fp = FloorPlan()
    # room1 = Room(2.5, 3.5, name="Room 1", rect_kwargs={"fill": "red"})
    # room2 = Room(2.5, 3.5, name="Room 2", location=(room1, 0), rect_kwargs={"fill": "blue"})
    # room3 = Room(7.8, 3.9, name="Room 3", location=(room2, 0), rect_kwargs={"fill": "green"})
    # room4 = Room(2.7, 3.5, name="Room 4", location=(room2, room3), rect_kwargs={"fill": "yellow"})
    # room5 = Room(5.1, 1.5, name="Room 5", location=(0, room1), rect_kwargs={"fill": "orange"})
    # room6 = Room(5, 3.9, name="Room 6", location=(room3, 0), rect_kwargs={"fill": "purple"})
    # rooms = [room1, room2, room3, room4, room5, room6]
    # for room in rooms:
    #     fp.add_room(room)
    # fp.draw()
    import doctest
    doctest.testmod()