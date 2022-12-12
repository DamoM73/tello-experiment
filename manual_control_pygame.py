from djitellopy import Tello
import cv2
import pygame
import time
import numpy as np
import sys

SPEED = 60
FPS = 120

class Drone():
    """
    Maintains the display and moves Tello in response to keys
    Press esc key to quit
    The controls are:
        - T: takeoff
        - L: land
        - Arrow keys: Forward, backwards, left and right
        - A and D: counter clockwise and clockwise roations (yaw)
        - W and S: up and down
        - SPACE: capture image
    """
    
    def __init__(self):
        # initalise pygame
        pygame.init()
        
        # create pygame window
        pygame.display.set_caption("Drone video stream")
        self.screen = pygame.display.set_mode((480,360))        
        
        # init Tello object
        self.drone = Tello()
        
        # set initial drone velocities
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10
        self.img = None
        
        # disable drone control
        self.send_rc_control = False
        
        # create an update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)
        
    def run(self):
        """
        The main loop for the drone. This will run as long until exited.
        """
        
        # intialise the drone's settings
        self.drone.connect()
        self.drone.set_speed(self.speed)
        self.drone.streamoff()
        self.drone.streamon()
        
        # gets the stream from the drone
        frame_read = self.drone.get_frame_read()
        
        running = True
        
        # main loop
        while running:
            # ---- Dealing with Events
            # iterates over all the registered PyGame events since last loop interval
            for event in pygame.event.get():
                # if event is update timer finish, run update
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                # if the event user clicking on PyGame window X then exit loop
                elif event.type == pygame.QUIT:
                    running = False
                # if the event is a pressing a keydown
                elif event.type == pygame.KEYDOWN:
                    # if its the escape key then exit loop
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # if it's any other key send they key details to the key_down function
                    else:
                        self.key_down(event.key)
                # if the event is the release of a key send details to kep_up function
                elif event.type == pygame.KEYUP:
                    self.key_up(event.key)
            
            # if the drone is out of range (no feed) break loop                    
            if frame_read.stopped:
                break
            
            # ---- Updating Display
            # set background to black
            self.screen.fill((0, 0, 0))
            
            # capture current frame from the stream
            self.img = frame_read.frame
            
            # --- process image for display on PyGame           
            
            # resize to make stream smoother
            frame = cv2.resize(self.img, (480,360))
            
            # add current battery level to image
            text = f"Battery: {self.drone.get_battery()}%"
            cv2.putText(frame, text, (5, 360 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)            
            
            # convert OpenCV colourspace (BGR) to PyGame colourspace (RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # rotate frame to correct orientation
            frame = np.rot90(frame)
            
            # flip frame horizontally for correct orientation
            frame = np.flipud(frame)
            
            # add image to PyGame window
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()
            
            # pause for next image (prevents lag)
            time.sleep(1 / FPS)
        
        # drone shutdown proceedure    
        self.drone.end()
        pygame.quit()
        sys.exit()
        
    
    def key_down(self, key):
        """
        Update velocities based on key pressed
        Arguements:
            key: pygame key
        """
        
        if key == pygame.K_UP:
            self.for_back_velocity = SPEED
        elif key == pygame.K_DOWN:
            self.for_back_velocity = -SPEED
        elif key == pygame.K_LEFT:
            self.left_right_velocity = -SPEED
        elif key == pygame.K_RIGHT:
            self.left_right_velocity = SPEED
        elif key == pygame.K_w:
            self.up_down_velocity = SPEED
        elif key == pygame.K_s:
            self.up_down_velocity = -SPEED
        elif key == pygame.K_a:
            self.yaw_velocity = -SPEED
        elif key == pygame.K_d:
            self.yaw_velocity = SPEED
            
    
    def key_up(self, key):
        """
        Update velocities based on key release
        Arguments:
            key: pygame key
        """
        
        if key in [pygame.K_UP, pygame.K_DOWN]:
            self.for_back_velocity = 0
        elif key in [pygame.K_LEFT, pygame.K_RIGHT]:
            self.left_right_velocity = 0
        elif key in [pygame.K_w, pygame.K_s]:
            self.up_down_velocity = 0
        elif key in [pygame.K_a, pygame.K_d]:
            self.yaw_velocity = 0
        elif key == pygame.K_t:
            self.drone.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:
            not self.drone.land()
            self.send_rc_control = False
        elif key == pygame.K_SPACE:
            cv2.imwrite(f"captures\\{time.time()}.jpg", self.img)
            
    def update(self):
        """
        Update routine. Send velocities to Tello
        """
        
        if self.send_rc_control:
            self.drone.send_rc_control(self.left_right_velocity,
                                       self.for_back_velocity,
                                       self.up_down_velocity,
                                       self.yaw_velocity)
            
    
def main():
    drone = Drone()
    
    drone.run()
    
    
if __name__ == "__main__":
    main()