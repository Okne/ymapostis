
"""
-----------------------------------------------------------------------------
This source file is part of OSTIS (Open Semantic Technology for Intelligent Systems)
For the latest info, see http://www.ostis.net

Copyright (c) 2010 OSTIS

OSTIS is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OSTIS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with OSTIS.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
"""


'''
Created on 22.05.2012

@author: Andrei Krauchanka
'''

from suit.cf import BaseModeLogic
import suit.core.exceptions as exceptions
import suit.core.kernel as core
import suit.core.objects as objects
import ogre.renderer.OGRE as ogre
import suit.core.render.engine as render_engine
import yandexmaps_environment as env

count = 0

class YandexMapsViewer(BaseModeLogic):
    """Logic realization for image viewer 
    """
    def __init__(self):        
        '''
        Constructor
        '''
        BaseModeLogic.__init__(self)
        
        # texture object 
        self.texture = None
        self.file_addr = None
        self.imageName = None
        self.sceneNodeRect = render_engine.SceneManager.createSceneNode()
        
        self.rect = None
        self._createRect()
        
    def __del__(self):
        self.sceneNode.detachObject(self.rect)
        BaseModeLogic.__del__(self)
        
    def delete(self):
        """Deletion message
        """
        BaseModeLogic.delete(self)
        
        if self.sceneNodeRect is not None:
            render_engine.SceneManager.destroySceneNode(self.sceneNodeRect)
        
        if self.material is not None:   self._destroyMaterial()
        if self.texture is not None:    self._destroyTexture()
        if self.file_addr is not None: self.file_addr = None
        
        self._destroyRect()
        
    def _onContentUpdate(self):
        
        import suit.core.keynodes as keynodes
        sheet = self._getSheet()
        
        #translate sheet data
        
        sheet.content_type = objects.ObjectSheet.CT_String
        sheet.content_data = str("") # make translation into gwf
        sheet.content_format = keynodes.ui.format_ymapsml
        
    def _setSheet(self, _sheet):
        BaseModeLogic._setSheet(self, _sheet)
        
        _sheet.eventRootChanged = self._onRoot
        _sheet.eventContentUpdate = self._onContentUpdate
        
        # trying to get data for showing
        import suit.core.sc_utils as sc_utils
        session = core.Kernel.session()
        _addr = _sheet._getScAddr()   
        _fmt = sc_utils.getContentFormat(session, _addr)     
  
        assert _fmt is not None
        
        _cont = session.get_content_const(_addr)
        assert _cont is not None
        
        _cont_data = _cont.convertToCont()
        self.file_addr = _cont_data
        
        _type = session.get_idtf(_fmt).lower()
        global count
        count += 1
        
#        import os, pm.pm
#        self.imageName = os.path.join(env.res_tmp_dir, "%s.jpg" % str(_addr.this))
#        pm.pm.saveContentToFile(self.imageName + "%d.jpg" % count, _cont)

        
#        file(self.imageName + "_", "wb").write(_cont.get_data(_cont_data.d.size))
        
        """data = _cont.get_data(_cont_data.d.size)
        stream = ogre.MemoryDataStream("%s" % str(self), _cont_data.d.size, False)
        stream.setData(data)
#     
        try:
            img = ogre.Image()
            img.load(stream, ogre.Image.getFileExtFromMagic(stream))
            self._createTexture(img)
            self._createMaterial()
            self._resizeRect()
        except:
            import sys, traceback
            print "Error:", sys.exc_info()[0]
            traceback.print_exc(file=sys.stdout)
            
#        
#        
#        _image = self._createImageFromData(pm.pm.castChar_p(_cont_data.d.ptr), _cont_data.d.size, _type)
#        print _image"""
                
    def _onRoot(self, _isRoot):
        """Notification on sheet root state changing
        """
        if _isRoot:
            render_engine.SceneNode.addChild(self._getSheet().sceneNodeChilds, self.sceneNodeRect)
            render_engine.SceneManager.setBackMaterial("Back/Spaces")
            
            # get data from sheet node content
            
            # trying to get data for showing
            import suit.core.sc_utils as sc_utils
            session = core.Kernel.session()
            _addr = self._getSheet()._getScAddr()   
            _fmt = sc_utils.getContentFormat(session, _addr)     
  
            assert _fmt is not None
        
            _cont = session.get_content_const(_addr)
            assert _cont is not None
        
            _cont_data = _cont.convertToCont()
            self.file_addr = str(_cont_data.d.ptr)

            file_addr = self.file_addr.decode('cp1251')        
            
            dataToPaste = {'title': "Test", 'api_key': env.api_key, 'file_address': file_addr}
            
            #get template
            template = self._fileToStr()
            #put data into placeholders
            webPageText = template.format(**dataToPaste)
            #show to user in default browser
            self._browseLocal(webPageText)
        else:
            render_engine.SceneNode.removeChild(self._getSheet().sceneNodeChilds, self.sceneNodeRect)
            render_engine.SceneManager.setDefaultBackMaterial() 
        
    def _createRect(self):
        """ Creates rectangle surface for root mode
        """
        # FIXME: make thread safe
        self.rect = ogre.Rectangle2D(True)
        self.rect.setCorners(-0.7, 0.7, 0.7, -0.7)
        self.rect.setRenderQueueGroup(ogre.RENDER_QUEUE_8)
        self.rect.setBoundingBox(ogre.AxisAlignedBox(ogre.Vector3(-100000.0, -100000.0, -100000.0), ogre.Vector3(100000.0, 100000.0, 100000.0)))
        self.sceneNodeRect.attachObject(self.rect)
        
    def _resizeRect(self):
        """Calculate rectangle size base on texture size
        """
        tw = self.texture.getSrcWidth()
        th = self.texture.getSrcHeight()
        aspect = tw / th
        
        width = render_engine.Window.width
        height = render_engine.Window.height
        
        w = tw
        h = th
        
        if aspect >= 1.0 and tw >= width:
            w = width
            h = width / aspect
        elif aspect < 1.0 and th >= height:
            h = height
            w = h * aspect
                  
        # calculate corners
        rel_w = float(w) / float(width)
        rel_h = float(h) / float(height)
         
        self.rect.setCorners(-rel_w, rel_h, rel_w, -rel_h)
        
    
    def _destroyRect(self):
        """ Destroys rectangle surface for root mode
        """
        self.rect = None
        # FIXME: scene node removing
    
    def getMaterialName(self):
        """Returns material name
        """
        return "%s_material" % str(self)
    
    def _createMaterial(self):
        """Creates material for image viewing
        """
        self.material = ogre.MaterialManager.getSingleton().create(self.getMaterialName(), env.resource_group)
        mpass = self.material.getTechnique(0).getPass(0)
        mpass.setLightingEnabled(False) 
        #mpass.setDiffuse(0.0, 1.0, 0.0, 1.0)
        #mpass.setSceneBlending(Ogre.SBT_TRANSPARENT_ALPHA)
        mpass.setDepthWriteEnabled(True)
        tus = mpass.createTextureUnitState(self.getTextureName())
#        tus.setTextureName(self.getTextureName())
        
        self._getSheet()._setMaterialShowName(self.getMaterialName())
        self.rect.setMaterial(self.getMaterialName())
        
    def _destroyMaterial(self):
        """Destroys material
        """
        ogre.MaterialManager.getSingleton().remove(self.material)
    
    def getTextureName(self):
        """Returns name for texture
        """
        return "image/viewer_" + str(self)
    
    def _createTexture(self, _image):
        """Creates texture object
        
        @param _image:    image object to create texture
        @type _image: ogre.Image 
        """
        self.texture = ogre.TextureManager.getSingleton().loadImage(self.getTextureName(), env.resource_group, _image)
    
    def _destroyTexture(self):
        """Destroys old texture
        """
        ogre.TextureManager.getSingleton().remove(self.texture)
        
    def _recreateTexture(self, _image):
        """Recreates texture for new image
        @param _image: image to create texture 
        @type _image: ogre.Image 
        """
        if self.texture is not None:    self._destroyTexture()
        self._createTexture(_image)

    def _browseLocal(self, webpageText):
        """Start your webbrowser on a local file containing the text."""
        self._strToFile(webpageText)
        import webbrowser
        webbrowser.open(env.mapFileName)
        
    def _fileToStr(self):
        """Return a string containing the contents of the named file."""
        fin = open(env.templateName); 
        contents = fin.read();  
        fin.close() 
        return unicode(contents, 'utf-8')
    
    def _strToFile(self, text):  
        """Write a file with the given name and the given text."""
        output = open(env.mapFileName,"w")
        output.write(text.encode('utf-8'))
        output.close()