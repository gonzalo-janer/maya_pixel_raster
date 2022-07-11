# This script rasterizes a grey scale image into voxels with varying scale,
# corresponding to the color value.
from turtle import color
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
    voxel_scale_ls = [voxel_scale] * 3
    return voxel_scale_ls

def get_color_scale(voxel_scale_ls, rgb_value_ls):
    color_scale_ls = []
    for val in voxel_scale_ls:
        color_scale_ls.append((1 - val) * rgb_value_ls[0])
    return color_scale_ls
        
def main(x_resolution = None):
    img_plane = pm.selected()[0]
    file_node = get_file_texture(img_plane)
    if x_resolution == None:
        resolution = file_node.outSize.get()
        x_res = int(resolution[0])
        y_res = int(resolution[1])
    print(resolution)
    #TODO if x_resolution is different
    parent_group = pm.group(name = 'raster_parent_group', empty = True)
    voxel_scale_ls = get_voxel_scale(img_plane, x_res)
    print(voxel_scale_ls)

    for y in range(y_res):
        y += 0.5
        v_value = 1 / y_res * y
        for x in range(x_res):
            x += 0.5
            u_value = 1 / x_res * x
            world_position = pm.pointOnSurface(img_plane, u = u_value, v = v_value)
            rgb_value_ls = pm.colorAtPoint(file_node, output = 'RGB', u = u_value, v = v_value)
            # invert color value
            rgb_value_ls = [1 - val for val in rgb_value_ls]
            color_scale_ls = get_color_scale(voxel_scale_ls, rgb_value_ls)
            voxel_group = pm.group(name = 'voxel_group', empty = True)
            voxel = pm.polyCube()[0]
            pm.parent(voxel, voxel_group)
            voxel_group.translate.set(world_position)
            voxel_group.scale.set(voxel_scale_ls)
            voxel.scale.set(rgb_value_ls)
            pm.parent(voxel_group, parent_group)

if __name__ == '__main__':
    main()
