from swarmy.perception import Perception
import pygame
import math
import numpy as np

class LightIntensitySensor_L(Perception):
    def __init__(self, agent, environment, config):
        super().__init__(agent, environment)
        self.agent = agent
        self.environment = environment
        self.config = config

    def sensor(self):
        """ Returns the light intensity at the point of the sensor.
        Light intensity is calculated as the average of the RGB values of the pixel.
        """

        robot_position_x, robot_position_y, robot_heading = self.agent.get_position()
        rob_pos = pygame.Vector2(robot_position_x, robot_position_y)

        sensor_1_direction_x_l = math.sin(math.radians(robot_heading + 40))
        sensor_1_direction_y_l = math.cos(math.radians(robot_heading + 40))

        #trying to "install" the sensor to left front of robot
        # Calculate sensor position and clamp it to surface boundaries
        sensor_x = int(robot_position_x + (sensor_1_direction_x_l * 35))
        sensor_y = int(robot_position_y + (sensor_1_direction_y_l * 35))
        sensor_x = max(0, min(sensor_x, self.environment.displaySurface.get_width() - 1))
        sensor_y = max(0, min(sensor_y, self.environment.displaySurface.get_height() - 1))

        sensor_l_pos = [sensor_x, sensor_y]

        sensor_color = (255, 0, 0)

        self.environment.add_dynamic_circle_object([sensor_color, sensor_l_pos, 3, 3])

        # helper to transform lines to rectange objects, allows for collision detection
        helper_object = pygame.draw.line(self.agent.environment.displaySurface, sensor_color, rob_pos, sensor_l_pos)
        #self.environment.bumper_object_list.append(helper_object)

        # Get the surface of the environment
        surface = self.environment.displaySurface

        # Calculate the light intensity at the point of the sensor
        r, g, b, _ = surface.get_at((sensor_l_pos[0], sensor_l_pos[1]))

        light_intensity_L = (r + g + b) / (3*255)  # Average of RGB values
        print("x: ", sensor_l_pos[0], "y: ", sensor_l_pos[1])#print coordinates of the robot
        print("Light Intensity: ", light_intensity_L)#print light intensity

        return light_intensity_L #to be used in controller