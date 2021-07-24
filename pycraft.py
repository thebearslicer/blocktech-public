from inspect import currentframe
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from opensimplex import *

# from PIL import Image
# from ursina.shaders import lit_with_shadows_shader

app = Ursina()

grass_texture = load_texture("assets/textures/roax_grass.png")
format_texture = load_texture("assets/format.png")

block_to_place = 1

def update():
    global block_to_place
    if held_keys['1']: block_to_place = 1
    if held_keys['2']: block_to_place = 2

    # ect
    
class Voxel(Button):
    def __init__(self, pos=(0, 0, 0), given_texture='white_cube'):
        super().__init__(
            parent=scene,
            position=pos,
            model='assets/block.obj',
            origin_y=0.5,
            texture=given_texture,
            scale=0.5,
            color=color.color(0, 0, random.uniform(0.9, 1))
            # shader=lit_with_shadows_shader
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)

            if key == 'right mouse down':
                if block_to_place == 1:
                    grass_voxel = Voxel(pos=(self.position + mouse.normal), given_texture=grass_texture)


heightmap = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def create_random_heightmap(input_map):  # make sure input map is all zeros
    for i in range(len(input_map)):
        for j in range(len(input_map[i])):
            input_map[i][j] = random.randint(0, 5)

    return input_map  # literally random yup


def create_heightmap(size_z, size_x):
    heightmap = [[0 for i in range(size_z)] for j in range(size_x)]  # ??? makes same thing as heightmap above

    tmp = OpenSimplex(random.randint(10000, 99999))

    multiplier = 0.001
    for z in range(len(heightmap)):
        for x in range(len(heightmap[z])):
            # iterates over all positions in heightmap
            heightmap[z][x] = (tmp.noise2d(z*multiplier, x*multiplier) + 1) **2
            heightmap[z][x] = int(heightmap[z][x])

    return heightmap


def generate_chunk(input_heightmap, top_texture, bottom_texture, fill, z_offset=0, x_offset=0):
    for z in range(len(input_heightmap)):  # iterate over all lists in input_heightmap
        for x in range(len(input_heightmap[z])):  # iterate over current sublist
            grass_generate = Voxel(pos=(x + x_offset, input_heightmap[x][z], z + z_offset), given_texture=top_texture)  # create top layer
            if fill:
                if input_heightmap[x][z] <= 0: continue  # check if top layer is at y<=0, if so, continue
                while input_heightmap[x][z] >= -1:  # check if top layer is not at y=0
                    below = Voxel(pos=(x + x_offset, input_heightmap[x][z] - 1, z + z_offset),
                                  given_texture=bottom_texture)  # this loop makes sure there aren't any weird gaps in generation
                    input_heightmap[x][z] -= 1


# pivot = Entity()
# AmbientLight(parent=pivot, y=3, x=8, z=8, shadows=True, texture=load_texture("assets/dirt.png"))

generate_chunk(create_heightmap(16, 16), grass_texture, grass_texture,  False)
generate_chunk(create_heightmap(16, 16), grass_texture, grass_texture,  False, 16, 0)
generate_chunk(create_heightmap(16, 16), grass_texture, grass_texture,  False, 0, 16)
generate_chunk(create_heightmap(16, 16), grass_texture, grass_texture,  False, 16, 16)

player = FirstPersonController()

app.run()
