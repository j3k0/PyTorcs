#!BPY

"""
Name: '_W_T_F (.wtf)...'
Blender: 248
Group: 'Export'
Tooltip: 'Save an OpenRacing Track File'
"""

__author__ = "Campbell Barton, Jiri Hnidek, Jean-Christophe Hoelt"
__url__ = ['http://wiki.blender.org/index.php/Scripts/Manual/Export/opentrackformat', 'www.blender.org', 'blenderartists.org']
__version__ = "1.3"

__bpydoc__ = """\
This script is an exporter to openracing file format.

Usage:

Select the objects you wish to export and run this script from "File->Export" menu.
Selecting the default options from the popup box will be good in most cases.
All objects that can be represented as a mesh (mesh, curve, metaball, surface, text3d)
will be exported as mesh data.
"""

# --------------------------------------------------------------------------
# WTF Export v1.1 by Campbell Barton (AKA Ideasman)
# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

import Blender
from Blender import Mesh, Scene, Window, sys, Image, Draw
import BPyMesh
import BPyObject
import BPySys
import BPyMessages

# Returns a tuple - path,extension.
# 'hello.obj' >  ('hello', '.obj')
def splitExt(path):
    dotidx = path.rfind('.')
    if dotidx == -1:
        return path, ''
    else:
        return path[:dotidx], path[dotidx:] 

def fixName(name):
    if name == None:
        return 'None'
    else:
        return name.replace(' ', '_').replace('.', '_')

# A Dict of Materials
# (material.name, image.name):matname_imagename # matname_imagename has gaps removed.
MTL_DICT = {} 

def write_library_materials(file):
    file.write('\n<library_materials>\n')
    # Write material/image combinations we have used.
    for key, (mtl_mat_name, mat, img) in MTL_DICT.iteritems():
        
        # Get the Blender data for the material and the image.
        # Having an image named None will make a bug, dont do it :)
        
        file.write('\t<material id="%s">\n' % mtl_mat_name) # Define a new material: matname_imgname
        
        if mat:
            # Hardness, convert blenders 1-511 to MTL's 
            file.write('\t\t<hardness>%.6f</hardness>\n' % ((mat.getHardness()-1) * 1.9607843137254901))
            file.write('\t\t<rgbCol>%.6f %.6f %.6f</rgbCol>\n' % tuple(mat.rgbCol)) # Diffuse
            file.write('\t\t<specCol>%.6f %.6f %.6f</specCol>\n' % tuple(mat.specCol)) # Specular
            file.write('\t\t<IOR>%.6f</IOR>\n' % mat.IOR) # Refraction index
            file.write('\t\t<alpha>%.6f</alpha>\n' % mat.alpha) # Alpha (obj uses 'd' for dissolve)
        else:
            #write a dummy material here?
            file.write('\t\t<alpha>1</alpha>\n') # No alpha
        
        # Write images!
        if img:  # We have an image on the face!
            imgname = img.filename.split('\\')[-1].split('/')[-1]
            file.write('\t\t<diffuse_map>%s</diffuse_map>\n' % imgname) # Diffuse mapping image
        
        elif not mat: # No face image. if we have a material search for MTex image.
            for mtex in mat.getTextures():
                if mtex and mtex.tex.type == Blender.Texture.Types.IMAGE:
                    try:
                        imgname = mtex.tex.image.filename.split('\\')[-1].split('/')[-1]
                        file.write('\t\t<diffuse_map>%s</diffuse_map>\n' % imgname) # Diffuse mapping image
                        break
                    except:
                        # Texture has no image though its an image type, best ignore.
                        pass
        
        file.write('\t</material>\n')
    file.write('</library_materials>\n\n')

# Store groups
def write_library_groups(file):
    file.write('\n<library_groups>\n')
    for grp in Blender.Group.Get():
        file.write('\t<%s>\n' % grp.name)
        for ob in grp.objects:
            obnamestring = fixName(ob.name)
            file.write('\t\t<object url="#%s" />\n' % obnamestring)
        file.write('\t</%s>\n' % grp.name)
    file.write('</library_groups>\n\n')

def copy_file(source, dest):
    file = open(source, 'rb')
    data = file.read()
    file.close()
    
    file = open(dest, 'wb')
    file.write(data)
    file.close()


def copy_images(dest_dir):
    if dest_dir[-1] != sys.sep:
        dest_dir += sys.sep
    
    # Get unique image names
    uniqueImages = {}
    for matname, mat, image in MTL_DICT.itervalues(): # Only use image name
        # Get Texface images
        if image:
            uniqueImages[image] = image # Should use sets here. wait until Python 2.4 is default.
        
        # Get MTex images
        if mat:
            for mtex in mat.getTextures():
                if mtex and mtex.tex.type == Blender.Texture.Types.IMAGE:
                    image_tex = mtex.tex.image
                    if image_tex:
                        try:
                            uniqueImages[image_tex] = image_tex
                        except:
                            pass
    
    # Now copy images
    copyCount = 0
    
    for bImage in uniqueImages.itervalues():
        image_path = sys.expandpath(bImage.filename)
        if sys.exists(image_path):
            # Make a name for the target path.
            dest_image_path = dest_dir + image_path.split('\\')[-1].split('/')[-1]
            if not sys.exists(dest_image_path): # Image isnt alredy there
                print '\tCopying "%s" > "%s"' % (image_path, dest_image_path)
                copy_file(image_path, dest_image_path)
                copyCount+=1
    print '\tCopied %d images' % copyCount

def write(filename, objects,\
EXPORT_NORMALS_HQ=False,\
EXPORT_MTL=True,  EXPORT_COPY_IMAGES=False,\
EXPORT_APPLY_MODIFIERS=True, EXPORT_BLEN_OBS=True,\
EXPORT_GROUP_BY_OB=False):
    '''
    Basic write function. The context and options must be alredy set
    This can be accessed externaly
    eg.
    write( 'c:\\test\\foobar.obj', Blender.Object.GetSelected() ) # Using default options.
    '''
    
    def veckey3d(v):
        return round(v.x, 6), round(v.y, 6), round(v.z, 6)
        
    def veckey2d(v):
        return round(v.x, 6), round(v.y, 6)
    
    print 'WTF Export path: "%s"' % filename
    temp_mesh_name = '~tmp-mesh'

    time1 = sys.time()
    scn = Scene.GetCurrent()

    file = open(filename, "w")
    file.write('<?xml version="1.0"?>\n')
    file.write('<OPEN_TRACK>\n')

    # Write Header
    # file.write('\n<!--\n'
    #            + '  Blender3D v%s WTF File: %s\n' % (Blender.Get('version'), Blender.Get('filename').split('/')[-1].split('\\')[-1] )
    #            + '  www.blender3d.org\n'
    #            + '-->\n\n')

    # Get the container mesh. - used for applying modifiers and non mesh objects.
    containerMesh = meshName = tempMesh = None
    for meshName in Blender.NMesh.GetNames():
        if meshName.startswith(temp_mesh_name):
            tempMesh = Mesh.Get(meshName)
            if not tempMesh.users:
                containerMesh = tempMesh
    if not containerMesh:
        containerMesh = Mesh.New(temp_mesh_name)
    
    del meshName
    del tempMesh
    
    # Initialize totals, these are updated each object
    totverts = totuvco = totno = 0
    
    face_vert_index = 0
    
    globalNormals = {}
    
    file.write('\n<library_objects>\n')
    # Get all meshs
    for ob_main in objects:
        obnamestring = fixName(ob_main.name)
        file.write('\t<object id="%s">\n' % obnamestring) # Write Object name

        for ob, ob_mat in BPyObject.getDerivedObjects(ob_main):
            # Will work for non meshes now! :)
            # getMeshFromObject(ob, container_mesh=None, apply_modifiers=True, vgroups=True, scn=None)
            me = BPyMesh.getMeshFromObject(ob, containerMesh, EXPORT_APPLY_MODIFIERS, False, scn)
            if not me:
                file.write('\t\t<loc>%.6f %.6f %.6f</loc>\n' % tuple(ob_main.loc)) # Write Object name
                file.write('\t\t<rot>%.6f %.6f %.6f</rot>\n' % tuple(ob_main.rot)) # Write Object name
                continue
            
            faceuv = me.faceUV
            
            # We have a valid mesh
            if me.faces:
                # Add a dummy object to it.
                has_quads = False
                for f in me.faces:
                    if len(f) == 4:
                        has_quads = True
                        break
                
                if has_quads:
                    oldmode = Mesh.Mode()
                    Mesh.Mode(Mesh.SelectModes['FACE'])
                    
                    me.sel = True
                    tempob = scn.objects.new(me)
                    me.quadToTriangle(0) # more=0 shortest length
                    oldmode = Mesh.Mode(oldmode)
                    scn.objects.unlink(tempob)
                    
                    Mesh.Mode(oldmode)
            
            # Make our own list so it can be sorted to reduce context switching
            faces = [ f for f in me.faces ]
            edges = me.edges
            
            if not (len(faces)+len(edges)+len(me.verts)): # Make sure there is somthing to write
                continue # dont bother with this mesh.
            
            me.transform(ob_mat)
            
            # High Quality Normals
            if faces:
                if EXPORT_NORMALS_HQ:
                    BPyMesh.meshCalcNormals(me)
                else:
                    # transforming normals is incorrect
                    # when the matrix is scaled,
                    # better to recalculate them
                    me.calcNormals()
            
            # # Crash Blender
            #materials = me.getMaterials(1) # 1 == will return None in the list.
            materials = me.materials
            
            materialNames = []
            materialItems = materials[:]
            if materials:
                for mat in materials:
                    if mat: # !=None
                        materialNames.append(mat.name)
                    else:
                        materialNames.append(None)
                # Cant use LC because some materials are None.
                # materialNames = map(lambda mat: mat.name, materials) # Bug Blender, dosent account for null materials, still broken.  
            
            # Possible there null materials, will mess up indicies
            # but at least it will export, wait until Blender gets fixed.
            materialNames.extend((16-len(materialNames)) * [None])
            materialItems.extend((16-len(materialItems)) * [None])
            
            # Sort by Material, then images
            # so we dont over context switch in the obj file.
            if faceuv:
                try:    faces.sort(key = lambda a: (a.mat, a.image, a.smooth))
                except: faces.sort(lambda a,b: cmp((a.mat, a.image, a.smooth), (b.mat, b.image, b.smooth)))
            elif len(materials) > 1:
                try:    faces.sort(key = lambda a: (a.mat, a.smooth))
                except: faces.sort(lambda a,b: cmp((a.mat, a.smooth), (b.mat, b.smooth)))
            else:
                # no materials
                try:    faces.sort(key = lambda a: a.smooth)
                except: faces.sort(lambda a,b: cmp(a.smooth, b.smooth))
            
            # Set the default mat to no material and no image.
            contextMat = (0, 0) # Can never be this, so we will label a new material teh first chance we get.
            contextSmooth = None # Will either be true or false,  set bad to force initialization switch.
            
            if len(faces) > 0:
                file.write('\t\t<mesh>\n')
            else:
                file.write('\t\t<curve>\n')

            vertname = "%s-Vertices" % obnamestring
            vertarrayname = "%s-Array" % vertname
            normname = "%s-Normals" % obnamestring
            normarrayname = "%s-Array" % normname
            texname = "%s-TexCoord" % obnamestring
            texarrayname = "%s-Array" % texname
            
            # Vert
            file.write('\t\t\t<float_array count="%d" id="%s">' % (len(me.verts), vertarrayname))
            for v in me.verts:
                file.write(' %.6f %.6f %.6f' % tuple(v.co))
            file.write('</float_array>\n')
            file.write('\t\t\t<vertices id="%s" source="#%s" />\n' % (vertname, vertarrayname))
            
            # UV
            if faceuv:
                file.write('\t\t\t<float_array id="%s">' % texarrayname)
                uv_face_mapping = [[0,0,0,0] for f in faces] # a bit of a waste for tri's :/
                
                uv_dict = {} # could use a set() here
                for f_index, f in enumerate(faces):
                    
                    for uv_index, uv in enumerate(f.uv):
                        uvkey = veckey2d(uv)
                        try:
                            uv_face_mapping[f_index][uv_index] = uv_dict[uvkey]
                        except:
                            uv_face_mapping[f_index][uv_index] = uv_dict[uvkey] = len(uv_dict)
                            file.write(' %.6f %.6f' % tuple(uv))
                
                uv_unique_count = len(uv_dict)
                del uv, uvkey, uv_dict, f_index, uv_index
                # Only need uv_unique_count and uv_face_mapping
                file.write('</float_array>\n')
                file.write('\t\t\t<texcoords id="%s" source="#%s" />\n' % (texname, texarrayname))
            
            # NORMAL, Smooth/Non smoothed.
            if len(faces) > 0:
                file.write('\t\t\t<float_array id="%s">' % normarrayname)
                for f in faces:
                    if f.smooth:
                        for v in f:
                            noKey = veckey3d(v.no)
                            if not globalNormals.has_key( noKey ):
                                globalNormals[noKey] = totno
                                totno +=1
                                file.write(' %.6f %.6f %.6f' % noKey)
                    else:
                        # Hard, 1 normal from the face.
                        noKey = veckey3d(f.no)
                        if not globalNormals.has_key( noKey ):
                            globalNormals[noKey] = totno
                            totno +=1
                            file.write(' %.6f %.6f %.6f' % noKey)
                file.write('</float_array>\n')
                file.write('\t\t\t<normals id="%s" source="#%s" />\n' % (normname, normarrayname))
            
            if not faceuv:
                f_image = None
            in_triangles = False
            
            for f_index, f in enumerate(faces):
                f_v= f.v
                f_smooth= f.smooth
                f_mat = min(f.mat, len(materialNames)-1)
                if faceuv:
                    f_image = f.image
                    f_uv= f.uv
                
                # MAKE KEY
                if faceuv and f_image: # Object is always true.
                    key = materialNames[f_mat],  f_image.name
                else:
                    key = materialNames[f_mat],  None # No image, use None instead.
                
                # CHECK FOR CONTEXT SWITCH
                if key == contextMat:
                    pass # Context alredy switched, dont do anythoing
                else:
                    if key[0] == None and key[1] == None:
                        # Write a null material, since we know the context has changed.
                        if in_triangles:
                            file.write('</p>\n')
                            file.write('\t\t\t</triangles>\n')
                        file.write('\t\t\t<triangles id="%s_%s">\n' % (fixName(ob.name), fixName(ob.getData(1))))
                        in_triangles = True
                    else:
                        mat_data= MTL_DICT.get(key)
                        if not mat_data:
                            # First add to global dict so we can export to mtl
                            # Then write mtl
                            
                            # Make a new names from the mat and image name,
                            # converting any spaces to underscores with fixName.
                            
                            # If none image dont bother adding it to the name
                            if key[1] == None:
                                mat_data = MTL_DICT[key] = ('%s'%fixName(key[0])), materialItems[f_mat], f_image
                            else:
                                mat_data = MTL_DICT[key] = ('%s_%s' % (fixName(key[0]), fixName(key[1]))), materialItems[f_mat], f_image
                        if in_triangles:
                            file.write('</p>\n')
                            file.write('\t\t\t</triangles>\n')
                        file.write('\t\t\t<triangles id="%s_%s_%s" material="#%s">\n' %
                                   (fixName(ob.name), fixName(ob.getData(1)), mat_data[0], mat_data[0]) )
                        in_triangles = True

                    file.write('\t\t\t\t<input offset="0" semantic="VERTEX" source="#%s" />\n' % vertname)
                    file.write('\t\t\t\t<input offset="1" semantic="NORMAL" source="#%s" />\n' % normname)
                    if faceuv:
                        file.write('\t\t\t\t<input offset="2" semantic="TEXCOORD" source="#%s" />\n' % texname)
                    file.write('\t\t\t\t<p>')
                    
                contextMat = key
                if f_smooth != contextSmooth:
                    if f_smooth: # on now off
                        # file.write('s 1\n')
                        contextSmooth = f_smooth
                    else: # was off now on
                        # file.write('s off\n')
                        contextSmooth = f_smooth
                
                if faceuv:
                    if f_smooth: # Smoothed, use vertex normals
                        for vi, v in enumerate(f_v):
                            file.write( ' %d %d %d' % (\
                                v.index+totverts,\
                                totuvco + uv_face_mapping[f_index][vi],\
                                globalNormals[ veckey3d(v.no) ])) # vert, uv, normal
                        
                    else: # No smoothing, face normals
                        no = globalNormals[ veckey3d(f.no) ]
                        for vi, v in enumerate(f_v):
                            file.write( ' %d %d %d' % (\
                                v.index+totverts,\
                                totuvco + uv_face_mapping[f_index][vi],\
                                no)) # vert, uv, normal
                    
                    face_vert_index += len(f_v)
                
                else: # No UV's
                    if f_smooth: # Smoothed, use vertex normals
                        for v in f_v:
                            file.write( ' %d %d' % (\
                                v.index+totverts,\
                                globalNormals[ veckey3d(v.no) ]))
                    else: # No smoothing, face normals
                        no = globalNormals[ veckey3d(f.no) ]
                        for v in f_v:
                            file.write( ' %d %d' % (\
                                v.index+totverts,\
                                no))
            if in_triangles:
                file.write('</p>\n')
                file.write('\t\t\t</triangles>\n')
            
            # Write edges.
            LOOSE = Mesh.EdgeFlags.LOOSE
            has_edge = False
            for ed in edges:
                if ed.flag & LOOSE:
                    has_edge = True
            if has_edge:
                file.write('\t\t\t<edges>\n')
                file.write('\t\t\t\t<input offset="0" semantic="VERTEX" source="#%s" />\n' % vertname)
                file.write('\t\t\t\t<p>')
                for ed in edges:
                    if ed.flag & LOOSE:
                        file.write(' %d %d' % (ed.v1.index+totverts, ed.v2.index+totverts))
                file.write('</p>\n')
                file.write('\t\t\t</edges>\n')
                
            # Make the indicies global rather then per mesh
            # totverts += len(me.verts)
            # if faceuv:
            #     totuvco += uv_unique_count
            me.verts= None
            if len(faces) > 0:
                file.write('\t\t</mesh>\n')
            else:
                file.write('\t\t</curve>\n')
        file.write('\t</object>\n')
    file.write('</library_objects>\n\n')
    
    # Now we have all our materials, save them
    if EXPORT_MTL:
        write_library_materials(file)

    # Save the groups
    write_library_groups(file)

    file.write('</OPEN_TRACK>\n')
    file.close()

    if EXPORT_COPY_IMAGES:
        dest_dir = filename
        # Remove chars until we are just the path.
        while dest_dir and dest_dir[-1] not in '\\/':
            dest_dir = dest_dir[:-1]
        if dest_dir:
            copy_images(dest_dir)
        else:
            print '\tError: "%s" could not be used as a base for an image path.' % filename
    
    print "WTF Export time: %.2f" % (sys.time() - time1)
    
    

def write_ui(filename):
    
    if not filename.lower().endswith('.wtf'):
        filename += '.wtf'
    
    if not BPyMessages.Warning_SaveOver(filename):
        return
    
    global EXPORT_APPLY_MODIFIERS, \
        EXPORT_NORMALS_HQ, \
        EXPORT_MTL, EXPORT_SEL_ONLY, EXPORT_ALL_SCENES,\
        EXPORT_ANIMATION, EXPORT_COPY_IMAGES, EXPORT_BLEN_OBS,\
        EXPORT_GROUP_BY_OB

    EXPORT_APPLY_MODIFIERS = True
    EXPORT_NORMALS_HQ = True
    EXPORT_MTL = True
    EXPORT_SEL_ONLY = False
    EXPORT_ALL_SCENES = False
    EXPORT_ANIMATION = False
    EXPORT_COPY_IMAGES = False
    EXPORT_BLEN_OBS = True
    EXPORT_GROUP_BY_OB = True
    
    
    
    base_name, ext = splitExt(filename)
    context_name = [base_name, '', '', ext] # basename, scene_name, framenumber, extension
    
    # Use the options to export the data using write()
    # def write(filename, objects, EXPORT_MTL=True, EXPORT_COPY_IMAGES=False, EXPORT_APPLY_MODIFIERS=True):
    orig_scene = Scene.GetCurrent()
    if EXPORT_ALL_SCENES:
        export_scenes = Scene.Get()
    else:
        export_scenes = [orig_scene]
    
    # Export all scenes.
    for scn in export_scenes:
        scn.makeCurrent() # If alredy current, this is not slow.
        context = scn.getRenderingContext()
        orig_frame = Blender.Get('curframe')
        
        if EXPORT_ALL_SCENES: # Add scene name into the context_name
            context_name[1] = '_%s' % BPySys.cleanName(scn.name) # WARNING, its possible that this could cause a collision. we could fix if were feeling parranoied.
        
        # Export an animation?
        if EXPORT_ANIMATION:
            scene_frames = xrange(context.startFrame(), context.endFrame()+1) # up to and including the end frame.
        else:
            scene_frames = [orig_frame] # Dont export an animation.
        
        # Loop through all frames in the scene and export.
        for frame in scene_frames:
            if EXPORT_ANIMATION: # Add frame to the filename.
                context_name[2] = '_%.6d' % frame
            
            Blender.Set('curframe', frame)
            if EXPORT_SEL_ONLY:
                export_objects = scn.objects.context
            else:   
                export_objects = scn.objects
            
            full_path= ''.join(context_name)
            
            # erm... bit of a problem here, this can overwrite files when exporting frames. not too bad.
            # EXPORT THE FILE.
            write(full_path, export_objects,\
            EXPORT_NORMALS_HQ, EXPORT_MTL,\
            EXPORT_COPY_IMAGES, EXPORT_APPLY_MODIFIERS,\
            EXPORT_BLEN_OBS,\
            EXPORT_GROUP_BY_OB)
        
        Blender.Set('curframe', orig_frame)
    
    # Restore old active scene.
    orig_scene.makeCurrent()
    Window.WaitCursor(0)


if __name__ == '__main__':
    Window.FileSelector(write_ui, 'Export OpenRacing WTF', sys.makename(ext='.wtf'))
