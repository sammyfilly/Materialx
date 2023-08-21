#!/usr/bin/env python
'''
MaterialX glTF bi-directional conversion example
'''

import sys, os, io, argparse
import MaterialX as mx
import MaterialX.PyMaterialXglTF as mx_gltf

def main():
    parser = argparse.ArgumentParser(description="MaterialX glTF converter")
    parser.add_argument(dest="inputFilename", help="Filename of the input document (glTF or MaterialX).")
    opts = parser.parse_args()

    inputFilename = opts.inputFilename
    if not os.path.isfile(inputFilename):
        print('Input file not found: ' + inputFilename)
        return

    inputFilePath = mx.FilePath(inputFilename)
    
    toGLTF = inputFilePath.getExtension() == 'mtlx'
    toMaterialX = inputFilePath.getExtension() == 'gltf'

    if not toGLTF and not toMaterialX:
        print('Input file must be glTF or MaterialX')
        return

    handler = mx_gltf.GltfMaterialHandler()
    if not handler:
        print('Failed to create GltfMaterialHandler')
        return
    
    utils = mx_gltf.GltfMaterialUtil()
    if not utils:
        print('Failed to create GltfMaterialUtil')
        return

    log = []
        
    # Convert from Materialx to GLTF
    if toGLTF:
        doc = mx.createDocument()
        mx.readFromXmlFile(doc, inputFilePath)
        outputFilePath = inputFilePath
        outputFilePath.addExtension('gltf')
        print('Converting MaterialX file:%s to glTF file: %s' % 
              (inputFilePath.asString(), outputFilePath.asString()))
        converted = utils.mtlx2glTF(handler, outputFilePath, doc, log)
        print("Converted: " + converted)

    # Convert from GLTF to MaterialX
    elif toMaterialX:
        stdlib = mx.createDocument()
        searchPath = mx.getDefaultDataSearchPath()
        libraryFolders = []
        libraryFolders.extend(mx.getDefaultDataLibraryFolders())
        try:
            mx.loadLibraries(libraryFolders, searchPath, stdlib)
        except err:
            print('Failed to load standard libraries: "', err, '"')
            sys.exit(-1)

        outputFilePath = inputFilePath
        createAssignments = True
        fullDefinition = False
        print('Converting glTF file:%s to MaterialX file: %s' % 
              (inputFilePath.asString(), outputFilePath.asString()))
        outputFilePath.addExtension('mtlx')
        doc = utils.glTF2Mtlx(inputFilePath, stdlib, createAssignments, fullDefinition, log)
        print("Converted: " + str(doc != None))

    if log:
        print("Log" + '\n'.join(log))


if __name__ == '__main__':
    main()
