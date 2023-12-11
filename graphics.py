import moderngl as mgl
import numpy as np
from PIL import Image

class Texture():
    ctx: mgl.Context     = None
    program: mgl.Program = None
    vao: mgl.VertexArray = None

    def __init__(self):
        self.loaded: bool  = False
        self.size:   tuple = None
        self.channels: int = None
        self.texture:     mgl.Texture = None
        self.framebuffer: mlg.Framebuffer = None
        

    def blit(self, source, pos:tuple=(0,0)):

        ctx, program, vao = Texture.get_components() 

        # Bind framebuffer and source texture
        self.framebuffer.use()
        source.texture.use(location=0)

        # Set uniforms
        program["sourceTexture"] = 0
        program["pos"]           = (pos[0] + source.size[0] / 2, pos[1] + source.size[1] / 2)
        program["textureSize"]   = self.size
        Program["sourceSize"]    = self.source.size

        # Render
        vao.render(mode=mgl.TRIANGLE_STRIP)

        # Unbind framebuffer
        ctx.screen.use()
        
    def use(self, location:int=0):
        self.texture.use(location=location)

    def __str__(self):
        return f"Texture Object {self.size[0]}x{self.size[1]} {self.channels}"

    @classmethod
    def init(cls, ctx:mgl.Context, program:mgl.Program, vao:mgl.VertexArray):
        cls.ctx = ctx
        cls.program = program
        cls.vao = vao
        
    @classmethod
    def get_components(cls) -> (mgl.Context, mgl.Program, mgl.VertexArray):
        return cls.ctx, cls.program, cls.vao

    @classmethod
    def load(self, path:str):
        ctx, program, vao = Texture.get_components() 

        image:   Image = Image.open(path)
        texture: Texture = Texture()
        
        texture.size:     tuple = image.size
        texture.channels: int   = len(image.getbands())
        texture.texture:  mgl.Texture = ctx.texture(size=texture.size, components=texture.channels, data=image.tobytes())
        texture.filter:   tuple       = (mgl.NEAREST, mgl.NEAREST)
        texture.framebuffer: mgl.Framebuffer = ctx.framebuffer(color_attachments=texture.texture)

        self.loaded = True

        return texture


class Canvas:
    ctx: mgl.Context     = None
    program: mgl.Program = None
    vao: mgl.VertexArray = None

    def __init__(self):
        
        pass

    @classmethod
    def init(cls, ctx:mgl.Context, program:mgl.Program, vao:mgl.VertexArray):
        cls.ctx = ctx
        cls.program = program
        cls.vao = vao