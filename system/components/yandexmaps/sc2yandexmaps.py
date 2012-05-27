
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

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import tempfile
from xml.dom.minidom import Document

#get current session
session = core.Kernel.session()

#get all translated questions nodes
sc_show_map_question_set = session.find_el_full_uri(u"/etc/questions/показать карту")
sc_coord_rel_node = session.find_el_full_uri(u"/seb/geodata/координаты*")

class SCParser:
    """
    Parser 
    """
    def __init__(self):
        self.parsed_data = {}
        self.data = None
        self.xml_doc = Document()
    
    def parse(self, input, question_node):
        #производим поиск всех связок отношения координаты* в ответе
        coord_sheafs = []
        res_list = session.search3_f_a_a(input, sc.SC_A_CONST|sc.SC_POS, sc.SC_CONST|sc.SC_NODE)
        if res_list is not None:
            for res in res_list:
                sheaf_node = res[2]
                is_coord_rel_sheaf = sc_utils.checkIncToSets(session, sheaf_node, [sc_coord_rel_node], sc.SC_A_CONST|sc.SC_POS)
                if is_coord_rel_sheaf:
                    coord_sheafs.append(sheaf_node)
        
        #элементы связки отношения и запоминаем название географического
        for sheaf in coord_sheafs:
            obj_node = sc_utils.searchOneShot(session.search5_f_a_a_a_f(sheaf, sc.SC_A_CONST|sc.SC_POS, sc.SC_CONST|sc.SC_NODE, sc.SC_A_CONST|sc.SC_POS, sc_keys.n_1))[2]
            obj_name = sc_utils.getLocalizedIdentifier(session, obj_node)[0]
            
            """obj_class_node = session.search3_a_a_f(sc.SC_CONST|sc.SC_ELMNCLASS, sc.SC_A_CONST|sc.SC_POS, obj_node)
            if obj_class_node is not None:
                for el_set in obj_class_node:
                    print sc_utils.getLocalizedIdentifier(session, el_set[0])[0]                    
            obj_class_name = sc_utils.getLocalizedIdentifier(session, obj_class_node)[0]"""
            
            obj_class_name = "geo_obj"
            
            coord_node = sc_utils.searchOneShot(session.search5_f_a_a_a_f(sheaf, sc.SC_A_CONST|sc.SC_POS, sc.SC_CONST|sc.SC_NODE, sc.SC_A_CONST|sc.SC_POS, sc_keys.n_2))[2]
            #получаем координаты из содержимого узла
            _cont = session.get_content_const(coord_node)
            _cont_data = _cont.convertToCont()
            coords_str = str(_cont_data.d.ptr)
            
            #сохраняем сведения об географическом объекте в карту
            self.parsed_data[obj_class_name + " " + obj_name] = coords_str     
            
    
    def toYmapsML(self):
        root = self.createRootElem()
        self.xml_doc.appendChild(root)
        
        geoObjCollect = self.createGeoObjectCollectionElem()
        root.appendChild(geoObjCollect)
        
        futureMems = self.createFutureMembersElem()
        geoObjCollect.appendChild(futureMems)
        
        for obj in self.parsed_data.keys():            
            geoObj = self.createGeoObjectElem()
            futureMems.appendChild(geoObj)
            
            name = self.createNameElem(obj.split(" ")[1])
            descr = self.createDescriptionElem(obj.split(" ")[0])
            geoObj.appendChild(name)
            geoObj.appendChild(descr)
            
            coord_str = self.parsed_data[obj]
            coord_list = coord_str.split(" ")
            
            #find out what kind of object need to show (point, line, polygon)
            obj_type = self._getObjectType(coord_list)
            
            if obj_type == "point":
                point = self.createPointElem()
                pos = self.createPosElem(coord_str)
                point.appendChild(pos)
                geoObj.appendChild(point)
                pass
            elif obj_type == "line":
                line = self.createLineStringElem()
                posList = self.createPosListElem(coord_str)
                line.appendChild(posList)
                geoObj.appendChild(line)
                pass
            elif obj_type == "polygon":
                polygon = self.createPolygonElem()
                exterior = self.createExteriorElem()
                ring = self.createLinearRingElem()
                posList = self.createPosListElem(coord_str)
                polygon.appendChild(exterior)
                exterior.appendChild(ring)
                ring.appendChild(posList)
                geoObj.appendChild(polygon)
                pass
            else:
                futureMems.removeChild(geoObj)
                print "error coordinate node content: ", coord_str
                pass 
        
        return self.xml_doc.toprettyxml("\t", "\n", "utf-8")
    
    def _getObjectType(self, coord_list):
        if len(coord_list) % 2 > 0:
            return "error"
        
        if len(coord_list) == 2:
            return "point"
        
        first_coord_pair = coord_list[:2]
        last_coord_pair = coord_list[-2:]
        
        if first_coord_pair == last_coord_pair:
            return "polygon"
        else:
            return "line"
        
    
    def createRootElem(self):
        root = self.xml_doc.createElement("ymaps:ymaps")
        root.setAttribute("xmlns:ymaps","http://maps.yandex.ru/ymaps/1.x")
        root.setAttribute("xmlns:repr","http://maps.yandex.ru/representation/1.x")
        root.setAttribute("xmlns:gml","http://www.opengis.net/gml")
        root.setAttribute("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
        root.setAttribute("xsi:schemaLocation","http://maps.yandex.ru/schemas/ymaps/1.x/ymaps.xsd")
        return root
    
    def createGeoObjectCollectionElem(self):
        return self.xml_doc.createElement("ymaps:GeoObjectCollection")
        
    def createFutureMembersElem(self):
        return self.xml_doc.createElement("gml:featureMembers")
       
    def createNameElem(self, name_str):
        n = self.xml_doc.createElement("gml:name")
        tn = self.xml_doc.createTextNode(name_str)
        n.appendChild(tn)
        return n
    
    def createDescriptionElem(self, descr_str):
        d = self.xml_doc.createElement("gml:description")
        tn = self.xml_doc.createTextNode(descr_str)
        d.appendChild(tn)
        return d
    
    def createGeoObjectElem(self):
        return self.xml_doc.createElement("ymaps:GeoObject")
    
    def createPointElem(self):
        return self.xml_doc.createElement("gml:Point")
    
    def createLineStringElem(self):
        return self.xml_doc.createElement("gml:LineString")
    
    def createLinearRingElem(self):
        return self.xml_doc.createElement("gml:LinearRing")
    
    def createPolygonElem(self):
        return self.xml_doc.createElement("gml:Polygon")
    
    def createExteriorElem(self):
        return self.xml_doc.createElement("gml:exterior")
    
    def createLinearRingElem(self):
        return self.xml_doc.createElement("gml:LinearRing")
    
    def createPosElem(self, coord_str):
        p = self.xml_doc.createElement("gml:pos")
        tn = self.xml_doc.createTextNode(coord_str)
        p.appendChild(tn)
        return p
    
    def createPosListElem(self, coords_str):
        pl = self.xml_doc.createElement("gml:posList")
        tn = self.xml_doc.createTextNode(coords_str)
        pl.appendChild(tn)
        return pl
        
    
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
            
            parser = SCParser()
            parser.parse(_input, question_node)            
            data = parser.toYmapsML()
            
            file_name = self._generate_filename()
            self._send_data_to_server(file_name, data)
            #set returned script to _output node content
            session.set_content_str(_output, env.server_address + file_name)            
                
        errors = []
        print "sc2yandexmaps finish translation"
        
        return errors
    
    def _generate_filename(self):
        return "ymapsml_data.xml"
    
    def _send_data_to_server(self, file_name, send_data):
        register_openers()
        # Start the multipart/form-data encoding of the file "DSC0001.jpg"
        # "geo_data" is the name of the parameter, which is normally set
        # via the "name" parameter of the HTML <input> tag.
        
        # headers contains the necessary Content-Type and Content-Length
        # datagen is a generator object that yields the encoded parameters
        tmp_file = tempfile.TemporaryFile()
        tmp_file.write(send_data)
        datagen, headers = multipart_encode({file_name: tmp_file})
        
        # Create the Request object
        request = urllib2.Request(env.server_address, datagen, headers)
        # Actually do the request, and get the response
        print urllib2.urlopen(request).read()
        tmp_file.close()
       
            