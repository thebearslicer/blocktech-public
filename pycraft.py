from inspect import currentframe
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from opensimplex import *
from ursina.shaders import lit_with_shadows_shader

app = Ursina()
app.title = "PyCraft"

grass_texture = load_texture("assets/textures/roax_grass.png")
stone_texture = load_texture("assets/textures/roax_stone.png")
dirt_texture = load_texture("assets/textures/roax_dirt.png")
wood_texture = load_texture("assets/textures/roax_wood.png")
leaves_texture = load_texture("assets/textures/roax_leaves.png")
stone_brick_texture = load_texture("assets/textures/roax_stone_bricks.png")
format_texture = load_texture("assets/format.png")

block_to_place = 1

def update():
    global block_to_place
    if held_keys['1']: block_to_place = 1
    if held_keys['2']: block_to_place = 2
    if held_keys['3']: block_to_place = 3
    if held_keys['4']: block_to_place = 4
    if held_keys['5']: block_to_place = 5
    if held_keys['6']: block_to_place = 6
    if held_keys['7']: block_to_place = 7
    if held_keys['8']: block_to_place = 8
    if held_keys['9']: block_to_place = 9

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
            color=color.color(0, 0, random.uniform(0.9, 1)),
            # shader=lit_with_shadows_shader
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)

            if key == 'right mouse down':
                if block_to_place == 1:
                    self.place_block(grass_texture)
                if block_to_place == 2:
                    self.place_block(dirt_texture)
                if block_to_place == 3:
                    self.place_block(stone_texture)
                if block_to_place == 4:
                    self.place_block(wood_texture)
                if block_to_place == 5:
                    self.place_block(leaves_texture)
                if block_to_place == 6:
                    self.place_block(stone_brick_texture)
                    
    def place_block(self, texture):
        vox = Voxel(pos=(self.position + mouse.normal), given_texture=texture)

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

def generate_tree(x, y, z):
    trunk_bottom = Voxel(pos=(1 + x, 0 + y, z + 1), given_texture=wood_texture)
    trunk_second = Voxel(pos=(1 + x, 1 + y, z + 1), given_texture=wood_texture)
    trunk_third  = Voxel(pos=(1 + x, 2 + y, z + 1), given_texture=wood_texture)
    trunk_forth  = Voxel(pos=(1 + x, 3 + y, z + 1), given_texture=wood_texture)
    top_leaf     = Voxel(pos=(1 + x, 4 + y, z + 1), given_texture=leaves_texture)
    left_leaf    = Voxel(pos=(0 + x, 3 + y, z + 1), given_texture=leaves_texture)
    right_leaf   = Voxel(pos=(2 + x, 3 + y, z + 1), given_texture=leaves_texture)
    behind_leaf  = Voxel(pos=(1 + x, 3 + y, z + 2), given_texture=leaves_texture)
    forward_leaf = Voxel(pos=(1 + x, 3 + y, z + 0), given_texture=leaves_texture)
 

generate_chunk(create_heightmap(16, 16), grass_texture, grass_texture,  False)
generate_tree(random.randint(1, 14), 1, random.randint(1, 14))


player = FirstPersonController()

app.run()
