
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
Created on 06.10.2009

@author: Andrei Krauchanka
'''

"""sc -> yandex.maps translator component
"""
from suit.core.objects import Translator
import suit.core.objects as objects
import suit.core.kernel as core
import yandexmaps_environment as env
import sc_core.pm as sc
import sc_core.constants as sc_constants
import suit.core.keynodes as keynodes
import suit.core.sc_utils as sc_utils
#import scg_alphabet
#import scg_objects
import suit.core.exceptions as exceptions
    
class TranslatorSc2Ym(Translator):
    """Class that implements translation from SC-code directly to yandex.maps
    """    
    def __init__(self):
        Translator.__init__(self)
        
    def __del__(self):
        Translator.__del__(self)
        
    def translate_impl(self, _input, _output):
        """Translator implementation
        @param _input:    input data set
        @type _input:    sc_global_addr
        @param _output:    output window (must be created)
        @type _output:    sc_global_addr
        
        @return: list of errors each element of list is a tuple(object, error)
        @rtype: list
        """
        errors = []
        
        return errors
       
            