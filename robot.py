import pygame 
import math

class Robot:
	"""
	A class to represent a car-like robot dimensions, start position, 
	heading angle, and velocity.

	Attributes
	----------
	start_pos : tuple
		Initial position of the robot in X and Y respectively.
	robot_img : str
		The robot image path.
	length : float
		The length between the rear wheels and front wheels of the
		car-like robot.
	"""	

	def __init__(self, start_pos, robot_img, length):
		# Robot settings
		self.x = start_pos[0] # X position
		self.y = start_pos[1] # Y position
		self.theta = 0 # Initial heading angle
		self.phi = 0 # Initial steering angle
		self.v = self.meters_to_pixels(meters=0.01) # m/s 
		self.L = self.meters_to_pixels(meters=length) # m (meters)
		self.max_speed = self.meters_to_pixels(meters=0.02) # m/s
		self.min_speed = self.meters_to_pixels(meters=-0.02) # m/s

		# Graphics 
		self.img = pygame.image.load(robot_img)
		self.rotated = self.img
		self.rect = self.rotated.get_rect(center=(self.x, self.y))
		
		# Time variant 
		self.dt = 0 # Delta time
		self.last_time = pygame.time.get_ticks() # Last time recorded
	
	def meters_to_pixels(self, meters):
		"""Converts from pixel to meters.
		
		Parameters
		----------
		meters: float
			The meters to be converted into pixels.
		"""
		return meters*3779.52

	def draw(self, map):
		"""Draws the robot on map.
		
		Parameters
		----------
		map : pygame.Surface
			The where the robot will be drawn.
		"""
		map.blit(source=self.rotated, dest=self.rect)

	def move(self, event=None):
		"""Moves the robot with key strokes.
		
		Takes the screen only if it is available.

		Parameters
		----------
		event : Event
			All events happenning in the screen.
		"""
		if event is not None:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					self.v += self.meters_to_pixels(0.0001)
				elif event.key == pygame.K_LEFT:
					self.v -= self.meters_to_pixels(0.0001)
				elif event.key == pygame.K_UP:
					self.phi += math.radians(0.03)
				elif event.key == pygame.K_DOWN:
					self.phi -= math.radians(0.03)

		# Bound the steering angle between -pi/2 and pi/2
		if self.phi < -math.pi/2:
			self.phi = -math.pi/2
		elif self.phi > math.pi/2:
			self.phi = math.pi/2

		# Car-like kinematic robot model
		self.x += self.v * math.cos(self.theta) * math.cos(self.phi) \
			* self.dt
		self.y -= self.v * math.sin(self.theta) * math.cos(self.phi) \
			* self.dt 			
		self.theta += self.v * (math.tan(self.phi) / self.L) * self.dt
		
		# Create the translation and rotation animation 
		self.rotated = pygame.transform.rotozoom(surface=self.img,
			angle=math.degrees(self.theta), scale=1)
		self.rect = self.rotated.get_rect(center=(self.x, self.y))
