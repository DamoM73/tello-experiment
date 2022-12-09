from djitellopy import Tello
import cv2
import pygame
import time
import numpy as np

SPEED = 60
FPS = 120

class FrontEnd(object):
    """
    Maintains the display and moves Tello in response to keys
    Press esc key to quit
    The controls are:
        - T: takeoff
        - L: land
        - Arrow keys: Forward, backwards, left and right
        - A and D: counter clockwise and clockwise roations (yaw)
        - W and S: up and down
    """
    
    def __init__(self):
        # init pygame
        pygame.init()
        
        # create pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode((960,720))
        
        # init Tello object
        self.drone = Tello()
        
        # drone velocities between -100 and 100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10
        
        self.send_rc_control = False
        
        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)
        
    def run(self):
        
        self.drone.connect()
        self.drone.set_speed(self.speed)
        
        self.drone.streamoff()
        self.drone.streamon()
        
        frame_read = self.drone.get_frame_read()
        
        running = True
        
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.key_down(event.key)
                elif event.type == pygame.KEYUP:
                    self.key_up(event.key)
                    
            if frame_read.stopped:
                break
            
            self.screen.fill((0, 0, 0))
            
            frame = frame_read.frame
            
            text = f"Battery: {self.drone.get_battery()}%"            
            cv2.putText(frame, text, (5, 720 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()
            
            time.sleep(1 / FPS)
            
        self.drone.end()
        
    
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
        
        if key == pygame.K_UP or key == pygame.K_DOWN:
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:
            self.yaw_velocity = 0
        elif key == pygame.K_t:
            self.drone.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:
            not self.drone.land()
            self.send_rc_control = False
            
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
    frontend = FrontEnd()
    
    frontend.run()
    
    
if __name__ == "__main__":
    main()