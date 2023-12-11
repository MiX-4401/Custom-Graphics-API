import pygame, numpy as np, moderngl as mgl
from graphics import Texture, Canvas, Transform
from sys import exit


class Main():

    shader_paths: dict = {
        "main": {
            "frag": r"shaders\display.frag", 
            "vert": r"shaders\display.vert"
        },
        "blitting": {
            "frag": None,
            "vert": r"shaders\blitting.vert"
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
        self.load_programs()
        self.load_vaos()
        self.load_graphics()

        self.pos = [0,0]

        self.create()

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
        self.screen = pygame.display.set_mode((700, 700), pygame.DOUBLEBUF | pygame.OPENGL)
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

    def load_graphics(self):
        Texture.init(ctx=self.ctx, program=self.programs["blitting"], vao=self.vaos["blitting"])
        Canvas.init(ctx=self.ctx, program=self.programs["blitting"], vao=self.vaos["blitting"])
        Transform.init(
            ctx=self.ctx, 
            programs={
                "scale": self.programs["main"]
            }, 
            vaos={
                "scale": self.vaos["main"]
            }
        )

    def load_programs(self):
        self.programs["blitting"]: mgl.Program = self.ctx.program(vertex_shader=self.shaders["blitting"]["vert"], fragment_shader=self.shaders["main"]["frag"])

    def load_vaos(self):
        self.vaos["blitting"]: mgl.VertexArray = self.ctx.vertex_array(self.programs["blitting"], [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])

    def create(self):
        self.sprite_1: Texture = Texture.load(path=r"images\0TextureWall.png")
        self.canvas_1: Canvas  = Canvas.load(size=self.screen.get_size())

        self.sprite_2: Texture = Transform.scale(surface=self.sprite_1, size=(self.sprite_1.size[0]//2, self.sprite_1.size[1]//2))

        pos: tuple = (self.canvas_1.size[0]//2-self.sprite_2.size[0]//2, self.canvas_1.size[1]//2-self.sprite_2.size[1]//2)
        self.canvas_1.fill(colour=(49,95,176))
        self.canvas_1.blit(source=self.sprite_2, pos=pos)
        
    def update(self):
        pygame.display.set_caption(title=f"Custom Graphics API | FPS: {round(self.clock.get_fps())}")
        print(pygame.mouse.get_pos())

    def draw(self):

        self.ctx.screen.use()

        self.canvas_1.use()
        self.programs["main"]["sourceTexture"] = 0
        self.vaos["main"].render(mode=mgl.TRIANGLE_STRIP)
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