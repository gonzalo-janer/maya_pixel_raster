# This script rasterizes a grey scale image into voxels with varying scale,
# corresponding to the color value.
import pymel.core as pm

# RETURNS file texture object, for the shader of the selected object.
# TAKES a PyNode of a geo or NURBS
def get_file_texture(img_plane):
    geo = img_plane.getShape()
    shading_group = geo.outputs(type = 'shadingEngine')
    shading_group_info = shading_group[0].connections(type = 'materialInfo')
    file_node = shading_group_info[0].connections(type = 'file')[0]
    return file_node

# RETURNS list of floats for the scale of each voxel,
# so that the voxels fully cover the image plane without overlapping.
# TAKES image plane PyNode and x_resolution INT
def get_voxel_scale(img_plane, x_res):
    coord_start = pm.pointOnSurface(img_plane, u = 0, v = 0)
    coord_end = pm.pointOnSurface(img_plane, u = 1, v = 0)
    for i in range(3):
        if coord_start[i] != coord_end[i]:
            length = coord_end[i] - coord_start[i]
            length = abs(length)
            break
    voxel_scale = length / x_res
    voxel_scale = [voxel_scale] * 3
    return voxel_scale

def main(x_resolution = None):
    img_plane = pm.selected()[0]
    file_node = get_file_texture(img_plane)
    if x_resolution == None:
        resolution = file_node.outSize.get()
        x_res = int(resolution[0])
        y_res = int(resolution[1])
    #TODO if x_resolution is different
    parent_group = pm.group(name = 'parent_group', empty = True)
    voxel_scale = get_voxel_scale(img_plane, x_res)
    print(voxel_scale)

    for y in range(y_res):
        y += 0.5
        v_value = 1 / y_res * y
        for x in range(x_res):
            x += 0.5
            u_value = 1 / x_res * x
            world_position = pm.pointOnSurface(img_plane, u = u_value, v = v_value)
            cube = pm.polyCube()[0]
            cube.translate.set(world_position)
            cube.scale.set(voxel_scale)
            pm.parent(cube, parent_group)

if __name__ == '__main__':
    main()