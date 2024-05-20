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
        },
        "flip": {
            "frag": None,
            "vert": r"shaders\flip.vert"
        },
        "uvs_1": {
            "frag": r"shaders\uvs_1.frag",
            "vert": None
        },
        "uvs_2": {
            "frag": r"shaders\uvs_2.frag",
            "vert": None
        }
    }

    def __init__(self):
        self.screen: pygame.Surface    = None
        self.clock:  pygame.time.Clock = None
        self.fps:    int               = None
        self.time:   float             = None

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
        self.screen = pygame.display.set_mode((540, 540), pygame.DOUBLEBUF | pygame.OPENGL)
        pygame.display.set_caption(title="Custom Graphics API | FPS: 0")
        self.clock  = pygame.time.Clock()
        self.fps    = 120
        self.time   = 0.0

    def load_moderngl(self):
        """
        Load the moderngl variables for rendering
        """

        self.ctx:              mgl.Context     = mgl.create_context()
        self.buffers["main"]:  mgl.Buffer      = self.ctx.buffer(np.array([-1.0, -1.0, 0.0, 0.0, 1.0, -1.0, 1.0, 0.0,-1.0,  1.0, 0.0, 1.0, 1.0,  1.0, 1.0, 1.0], dtype='f4'))
        self.programs["main"]: mgl.Program     = self.ctx.program(vertex_shader=self.shaders["main"]["vert"], fragment_shader=self.shaders["main"]["frag"]) 
        self.vaos["main"]:     mgl.VertexArray = self.ctx.vertex_array(self.programs["main"], [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        self.ctx.enable(mgl.BLEND)
        self.ctx.wireframe = False

    def load_graphics(self):
        Texture.init(ctx=self.ctx, program=self.programs["blitting"], vao=self.vaos["blitting"])
        Canvas.init(ctx=self.ctx, program=self.programs["blitting"], vao=self.vaos["blitting"])
        Transform.init(
            ctx=self.ctx, 
            programs={
                "scale": self.programs["main"],
                "flip":  self.programs["flip"]
            }, 
            vaos={
                "scale": self.vaos["main"],
                "flip":  self.vaos["flip"]
            }
        )

    def load_programs(self):
        self.programs["blitting"]:   mgl.Program = self.ctx.program(vertex_shader=self.shaders["blitting"]["vert"], fragment_shader=self.shaders["main"]["frag"])
        self.programs["flip"]:       mgl.Program = self.ctx.program(vertex_shader=self.shaders["flip"]["vert"],     fragment_shader=self.shaders["main"]["frag"])
        self.programs["uvs_1"]:      mgl.Program = self.ctx.program(vertex_shader=self.shaders["main"]["vert"],     fragment_shader=self.shaders["uvs_1"]["frag"])
        self.programs["uvs_2"]:      mgl.Program = self.ctx.program(vertex_shader=self.shaders["main"]["vert"],     fragment_shader=self.shaders["uvs_2"]["frag"])

    def load_vaos(self):
        self.vaos["blitting"]: mgl.VertexArray = self.ctx.vertex_array(self.programs["blitting"], [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        self.vaos["flip"]:     mgl.VertexArray = self.ctx.vertex_array(self.programs["flip"],     [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        self.vaos["uvs_1"]:    mgl.VertexArray = self.ctx.vertex_array(self.programs["uvs_1"],    [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        self.vaos["uvs_2"]:    mgl.VertexArray = self.ctx.vertex_array(self.programs["uvs_2"],    [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])

    def create(self):
        self.sprite_1: Texture = Texture.load(path=r"images\0TextureSomething.png")
        self.canvas_1: Canvas  = Canvas.load(size=self.screen.get_size())

        self.sprite_1: Texture = Transform.scale(source=self.sprite_1, size=(self.sprite_1.size[0]*12,self.sprite_1.size[1]*12))
        self.canvas_1.blit(source=self.sprite_1, pos=(-128,0), area=(0,0,64,64))

    def update(self):
        pygame.display.set_caption(title=f"Custom Graphics API | FPS: {round(self.clock.get_fps())}")
        # print(pygame.mouse.get_pos())
        self.time += 1.0
        self.sprite_1.shader(program=self.programs["uvs_1"], vao=self.vaos["uvs_1"], uniforms={"time": self.time})


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
        self.ctx.release()
        for key in self.programs:
            self.programs[key].release()
        for key in self.vaos:
            self.programs[key].release()
        for key in self.buffers:
            self.programs[key].release()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
            # print(pygame.mouse.get_pos())

if __name__ == "__main__":
    Main: Main = Main()
    Main.run()