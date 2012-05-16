
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
import suit.core.keynodes as sc_keys
#import scg_alphabet
#import scg_objects
import suit.core.exceptions as exceptions

#get current session
session = core.Kernel.session()

#get all translated questions nodes
sc_show_map_question_set = session.find_el_full_uri(u"/etc/questions/показать карту")
    
class ScToYMapsMLTranslator(Translator):
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
        #look for question node
        els = session.search11_f_a_a_a_a_a_f_a_f_a_f(_input, 
                                            sc.SC_A_CONST|sc.SC_POS, sc.SC_N_CONST,
                                            sc.SC_A_CONST|sc.SC_POS, sc.SC_N_CONST,
                                            sc.SC_A_CONST|sc.SC_POS, sc_keys.n_2,
                                            sc.SC_A_CONST|sc.SC_POS, sc_keys.n_1,
                                            sc.SC_A_CONST|sc.SC_POS, sc_keys.info.stype_sheaf)
        el = sc_utils.searchOneShot(els)
        assert el is not None
        
        #get question node
        question_node = el[4]
        
        #check if answer on question can be translated
        if sc_utils.checkIncToSets(session, question_node, [sc_show_map_question_set], sc.SC_POS | sc.SC_CONST):
            print "Show map question, translating answer"
            #parse sc-construction
            fin = open(env.testScript)
            test_data = fin.read()
            fin.close()
            #set returned script to _output node content
            session.set_content_str(_output, test_data)
            
                
        errors = []
        print "sc2yandexmaps finish translation"
        
        return errors
       
            