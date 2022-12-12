import pygame

def init():
    pygame.init()
    win = pygame.display.set_mode((50,50))
    
def get_key(key_name):
    response = False
    for event in pygame.event.get():
        pass
    
    key_input = pygame.key.get_pressed()
    formatted_key = getattr(pygame, f"K_{key_name}")
    
    if key_input[formatted_key]:
        response = True
        
    pygame.display.update()
    
    return response
    
    
def main():
    print(get_key("e"))
    
if __name__ == "__main__":
    init()
    
    while True:
        main()