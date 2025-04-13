from coordinates import Point2D


class Entity:
    """
    Represents an entity in the simulation. This could be a charge, particle, field, etc.
    The entity holds visual and logic elements and updates based on these elements.
    """

    def __init__(self, visual_elements: list, logic_elements: list, dynamic: bool = True,
                 position: Point2D = Point2D(0, 0)):
        """
        Initializes an entity with visual elements, logic elements, and dynamic behavior.

        :param visual_elements: List of visual elements that define the appearance of the entity.
        :param logic_elements: List of logic elements that define the entity's behavior (e.g., movement).
        :param dynamic: Whether the entity's state can change over time. Default is True.
        :param position: The initial position of the entity in the simulation space.
        """
        self.visual_elements = visual_elements
        self.logic_elements = logic_elements
        self.dynamic = dynamic
        self.position = position

    def update(self, **kwargs):
        """
        Updates the entity by running its logic and drawing its visual representation.

        - Runs the logic elements (such as updating position, velocity, etc.).
        - Draws the visual elements to represent the entity.

        The entity is destroyed if it moves beyond certain bounds (±10,000 units in either direction).

        :param kwargs: Arbitrary keyword arguments passed to the logic and visual elements.
        :return: A dictionary containing updated logic data. If the entity goes out of bounds, includes a 'destroy' key.
        """
        logic_data = self.logic(**kwargs)
        self.visual(**logic_data, **kwargs)
        if abs(self.position.x) > 10e3 or abs(self.position.y) > 10e3:
            return {"destroy": True}

        return logic_data

    def logic(self, **kwargs):
        """
        Runs the logic elements of the entity. Each logic element updates the state of the entity.

        :param kwargs: Arbitrary keyword arguments passed to each logic element.
        :return: A dictionary containing the updated logic data.
        """
        return_data = {}
        for element in self.logic_elements:
            run_data = element.run(position=self.position, **kwargs)
            if "position" in run_data:
                self.position = run_data["position"]
                del(run_data["position"])

            return_data.update(run_data)

        return return_data

    def visual(self, **kwargs):
        """
        Draws the visual elements of the entity.

        :param kwargs: Arbitrary keyword arguments passed to each visual element for rendering.
        """
        for element in self.visual_elements:
            element.draw(position=self.position, **kwargs)
