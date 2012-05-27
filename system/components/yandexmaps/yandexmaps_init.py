
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
Created on 03.02.2010

@author: Andrei Krauchanka
'''
import suit.core.kernel as core

import yandexmaps_viewer
import sc2yandexmaps
import yandexmaps_environment as env

def initialize():
    kernel = core.Kernel.getSingleton()
    
    from suit.core.objects import Factory
    import suit.core.keynodes as keynodes
    
    global view_factory
    global translsc2yandmap_factory
    
    view_factory = Factory(viewer_creator)
    translsc2yandmap_factory = Factory(sc2yandmap_creator)
    kernel.registerViewerFactory(view_factory, [keynodes.ui.format_ymapsml])
    kernel.registerTranslatorFactory(translsc2yandmap_factory, [keynodes.ui.format_sc], [keynodes.ui.format_ymapsml])

def shutdown():
    global view_factory
    global translsc2yandmap_factory
    kernel = core.Kernel.getSingleton()
    kernel.unregisterViewerFactory(view_factory)
    kernel.unregisterTranslatorFactory(translsc2yandmap_factory)    


def _resourceLocations():
    """Returns list of resource locations
    
    @return: list of tuples that represents resource storage type, location and group (storage_type, location, group)
    @rtype: list 
    """
    res = []
    for _path in env.resource_dirs:
        res.append( (_path, "FileSystem", env.resource_group) )
        
    return res 

def viewer_creator():
    return yandexmaps_viewer.YandexMapsViewer()

def sc2yandmap_creator():
    return sc2yandexmaps.ScToYMapsMLTranslator()