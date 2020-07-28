import os
import sys

import bpy
import mathutils
import numpy as np

dir = os.path.dirname(bpy.data.filepath)
if not dir:
    dir = os.path.dirname(__file__)
if dir not in sys.path:
    sys.path.append(dir)

exoplanets = __import__('exoplanets').system


def clean_slate():
    '''
    Simple function to clean up the scene,
    it deletes all objects and material from the scene
    '''
    for o in bpy.context.scene.objects:
        if o.type in ['MESH', 'EMPTY']:
            o.select_set(True)
        else:
            o.select_set(False)
    #
    bpy.ops.object.delete()
    #
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)


def add_sphere(rad, loc, Name):
    '''
    Adds a sphere to the scene
    -----------
    radius  : radius of the UV sphere
    (x,y,x) : position
    name    : name of the variable (note that this is not a string its the name by which you can
    later call the object)
    '''
    bpy.ops.mesh.primitive_uv_sphere_add(radius=rad, enter_editmode=False, location=loc)
    bpy.ops.object.shade_smooth()
    obj = bpy.data.objects['Sphere']
    obj.name = Name
    return obj


def adjust_node(node, inputs):
    '''
    Function to adjust the values of a given node based on the input dictionary
    '''
    for i in list(inputs.keys()):
        node.inputs[i].default_value = inputs[i]


def add_material_star(name, m_name, temp):
    '''
    adds a glowing star material to the object that is passed into the function
    ----------------
    name : name of the object (by default its UV Sphere, Cube etc..)
    m_name: the name you wish to give your material (a string)
    temp : Temperature of the star you are texturing
    ----------------
    '''
    mat = bpy.data.materials.new(m_name)
    mat.use_nodes = True
    name.data.materials.append(mat)
    mat.node_tree.nodes.remove(mat.node_tree.nodes['Principled BSDF'])
    # Store output node in a variable
    material_output = mat.node_tree.nodes.get('Material Output')
    # adding a mix shader
    mixer = mat.node_tree.nodes.new('ShaderNodeMixShader')
    mat.node_tree.links.new(material_output.inputs[0], mixer.outputs[0])
    # Create new node for emmision and set it's strength
    emission = mat.node_tree.nodes.new('ShaderNodeEmission')
    emission.inputs['Strength'].default_value = temp / 1000
    # emission.inputs[0].default_value=(0.9804,1,0.3246,1)
    # Blackbody radiation
    blackbody = mat.node_tree.nodes.new('ShaderNodeBlackbody')
    blackbody.inputs['Temperature'].default_value = temp
    # Link emission to output
    mat.node_tree.links.new(emission.inputs[0], blackbody.outputs[0])
    mat.node_tree.links.new(emission.outputs[0], mixer.inputs[1])
    # Create new node for emmision and set it's strength
    darker = 1000  # controls how dark you want some features to be
    emission2 = mat.node_tree.nodes.new('ShaderNodeEmission')
    emission2.inputs['Strength'].default_value = (temp / 3000) - 1
    # emission2.inputs[0].default_value=(0.9804,1,0.3246,1)
    # Blackbody radiation
    blackbody2 = mat.node_tree.nodes.new('ShaderNodeBlackbody')
    blackbody2.inputs['Temperature'].default_value = temp - darker
    # Link emission to output
    mat.node_tree.links.new(emission2.inputs[0], blackbody2.outputs[0])
    mat.node_tree.links.new(emission2.outputs[0], mixer.inputs[2])
    # adding a noise texture
    noise = mat.node_tree.nodes.new('ShaderNodeTexNoise')
    values = {2: 38, 3: 16, 4: 0, 5: 1.15}
    adjust_node(noise, values)
    #
    colra = mat.node_tree.nodes.new('ShaderNodeValToRGB')
    colra.color_ramp.elements[0].color = (0, 0, 0, 1)
    colra.color_ramp.elements[1].color = (1, 1, 1, 1)
    colra.color_ramp.elements[0].position = 0.32
    colra.color_ramp.elements[1].position = 0.65
    mat.node_tree.links.new(noise.outputs[0], colra.inputs[0])
    mat.node_tree.links.new(colra.outputs[0], mixer.inputs[0])


def update_camera(camera, focusPt=(0.0, 0.0, 0.0), distance=10.0):
    '''
    Focus the camera to a focus point and place the camera at a specific distance from that
    focus point. The camera stays in a direct line with the focus point.

    :param camera: the camera object
    :type camera: bpy.types.object
    :param focus_point: the point to focus on (default=``mathutils.Vector((0.0, 0.0, 0.0))``)
    :type focus_point: mathutils.Vector
    :param distance: the distance to keep to the focus point (default=``10.0``)
    :type distance: float
    '''
    focus_point = mathutils.Vector(focusPt)
    looking_direction = camera.location - focus_point
    rot_quat = looking_direction.to_track_quat('Z', 'Y')
    #
    camera.rotation_euler = rot_quat.to_euler()
    camera.location = camera.location * distance / camera.location.length


def cycles(render_file):
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 16
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(__file__), 'render', render_file + '_')
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.ops.render.render(animation=True, write_still=1)


def eevee(render_file):
    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
    bpy.context.scene.eevee.taa_render_samples = 16
    bpy.context.scene.eevee.use_bloom = True
    bpy.context.scene.eevee.use_gtao = True
    bpy.context.scene.eevee.use_motion_blur = True
    bpy.context.scene.view_settings.gamma = 0.85
    bpy.context.scene.render.filepath = os.path.join(os.path.dirname(__file__), 'render', render_file + '_')
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.ops.render.render(animation=True, write_still=1)


if __name__ == '__main__':
    argv = []
    if '--' in sys.argv:
        argv = sys.argv[sys.argv.index('--') + 1:]  # get all args after '--'

    if len(argv) > 1:
        params_file = argv[0]
        render_file = argv[1]
    else:
        print('Error : Parameters not proper!!!')
        print('Usage:')
        print('<blender_executable> --background --factory-startup --python <this_file> -- <params_file> <render_file>;')
        sys.exit(0)

    clean_slate()
    bpy.context.scene.render.fps = 15

    system = exoplanets(params_file, time_split=100, img_split=100, n=1.0)
    time_coord = system.coords()
    timespan = system.timespan

    star = add_sphere(1.0, (0, 0, 0), 'Star')
    star.modifiers.new('Subdivide', type='SUBSURF')
    mat = add_material_star(star, 'Starry', 5000)

    for planet in system.planets:
        mod = add_sphere(planet['planet_radius'], (0, 0, 0), 'Planet ' + str(planet['index']))
        mod.modifiers.new('Subdivide', type='SUBSURF')
        planet['model'] = mod

    start_locatn = (0, 0, 10)
    bpy.context.scene.frame_current = 0
    cam = bpy.data.objects['Camera']
    cam.location = start_locatn
    cam.data.angle = 60 * np.pi / 180

    dis = (2 * (3**0.5)) * max([planet['semi-major'] for planet in system.planets])
    update_camera(cam, focusPt=(0.0, 0.0, 0.0), distance=dis)

    light = bpy.context.scene.objects['Light']
    light.location = cam.location
    light.data.shadow_soft_size = 5
    light.data.energy = 20000

    # Make the background dark
    world = bpy.data.worlds['World']
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0, 0, 0, 1)
    bg.inputs[1].default_value = 5

    for i in range(len(timespan)):
        for planet in system.planets:
            planet['model'].location = time_coord[i][planet['index']]
            planet['model'].keyframe_insert(data_path='location', frame=i * 1)

    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = len(timespan) * 1

    # cycles(render_file)
    eevee(render_file)
