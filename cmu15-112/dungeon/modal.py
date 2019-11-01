import uuid
import pygame
import scenario

class Config(object):
  def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class GameObject(object):
    def __init__(self, config):
        self.uuid = uuid.uuid4()
        self.name = config.name
    
    def __repr__(self):
        return "%s - %s" % (self.__class__.name, self.name)
    
    def getUUID(self):
        return self.uuid
    
    def getName(self):
        return self.name

class PygModal(GameObject):
    def __init__(self, config):
        pygame.init()
        self.FPS = config.fps
        self.width = config.width
        self.height = config.height
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        
        self.running = False
        
        self.scenarios = dict()
        self.scenario = None
        
    def appendScenario(self, scenario):
        self.scenarios[scenario.getName()] = scenario
    
    def setActiveScenario(self, scenario):
        if name in self.scenarios:
            self.scenario = self.scenarios[name]
    
    def getActiveScenario(self):
        return self.scenario
    
    def run(self):
        self.running = True
        
        while self.running:
            milliseconds = self.clock.tick(self.FPS)
            
            for e in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                
                self.scenario.on_event(e)

            self.scenario.on_action()
            
            self.scenario.on_render(view)
        
        pygame.quit()


class View(GameObject):
#     def __init__(self, screen, config):
#         self.screen = screen
    
    def rendor(self, s):
        print(s)
        text = "FPS: %0.2f" % (self.clock.get_fps(), 
        pygame.display.set_caption(text)

        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
        