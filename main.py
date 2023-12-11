import pygame, numpy as np, moderngl as mgl
from graphics import Texture, Canvas
from sys import exit


class Main():

    shader_paths: dict = {
        "main": {
            "frag": r"shaders\display.frag", 
            "vert": r"shaders\display.vert"
        }   
    }

    def __init__(self):
        self.screen: pygame.Surface    = None
        self.clock:  pygame.time.Clock = None
        self.fps:    int               = None

        self.shaders:          dict        = None
        self.ctx:              mgl.Context = None
        
        self.buffers:  dict = {}
        self.programs: dict = {}
        self.vaos:     dict = {}

        self.load_shader_data()
        self.load_pygame()
        self.load_moderngl()

    def load_shader_data(self):
        paths: dict = Main.shader_paths

        shader_data: dict = {}
        for key in paths:
            vert: str = paths[key]["vert"]
            frag: str = paths[key]["frag"]
            
            if vert != None: vert = self.read_file(path=vert)
            if frag != None: frag = self.read_file(path=frag)

            shader_data[key] = {"vert": vert, "frag": frag}
        
        self.shaders = shader_data

    def read_file(self, path:str):
        with open(file=path, mode="r") as f:
            return f.read()


    def load_pygame(self):
        """
        Load the pygame variables for window
        """
        self.screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(title="Custom Graphics API | FPS: 0")
        self.clock  = pygame.time.Clock()
        self.fps    = 120

    def load_moderngl(self):
        """
        Load the moderngl variables for rendering
        """

        self.ctx:              mgl.Context     = mgl.create_context()
        self.buffers["main"]:  mgl.Buffer      = self.ctx.buffer(np.array([-1.0, -1.0, 0.0, 0.0, 1.0, -1.0, 1.0, 0.0,-1.0,  1.0, 0.0, 1.0, 1.0,  1.0, 1.0, 1.0], dtype='f4'))
        self.programs["main"]: mgl.Program     = self.ctx.program(vertex_shader=self.shaders["main"]["vert"], fragment_shader=self.shaders["main"]["frag"]) 
        self.vaos["main"]:     mgl.VertexArray = self.ctx.vertex_array(self.programs["main"], [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        
        self.ctx.wireframe = False

    
    def update(self):
        pygame.display.set_caption(title=f"Custom Graphics API | FPS: {round(self.clock.get_fps())}")
    
    def draw(self):


        pygame.display.flip()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.garbage_collection()
                pygame.quit()
                exit()

    def garbage_collection(self):
        pass

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    Main: Main = Main()
    Main.run()