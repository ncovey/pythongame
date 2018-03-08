from shader import Shader

def OpenFileAsStringBuffer(filename):
    if (filename != ''):
        buffer = []
        try:    
            with open(filename, 'r') as f:
                for line in f:
                    buffer.append(line)
                f.close()
                return buffer
        except IOError as e:
            print 'Could not open file: {}'.format(filename)
            return []
    else:
        return []

# create our Phong Shader by Jerome GUINOT aka 'JeGX' - jegx [at] ozone3d [dot] net
# see http://www.ozone3d.net/tutorials/glsl_lighting_phong.php

def LoadShaderFromFile(vshader_filename = '', pshader_filename = '', gshader_filename = ''):
    
    if (vshader_filename == '' and
        pshader_filename == '' and
        gshader_filename == ''):
        return None
    
    vshader_buffer = OpenFileAsStringBuffer(vshader_filename)
    pshader_buffer = OpenFileAsStringBuffer(pshader_filename)
    gshader_buffer = OpenFileAsStringBuffer(gshader_filename)

    return Shader(vshader_buffer, pshader_buffer, gshader_buffer)

