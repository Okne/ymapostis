
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
Created on 13.10.2009

@author: Denis Koronchik
'''
import thread
import pm
import ctypes

class MThreadSession:
    
    """Multithreaded session object
    """
    
    def __init__(self, session):
        self.__session = session
        self.lock = thread.allocate_lock()
        print "Starting multithreaded session"

    def __del__(self):
        pass
    
    def __getattr__(self, name):
        if name == 'error':
            self.lock.acquire()
            res = self.__session.error
            self.lock.release()
            return res
        
        raise AttributeError("There are no attribute '%s'" % name)
        
    def _stat(self, _uri):
        """Check if uri points to segment
        @param _uri: uri for check
        @type _uir: str
        
        @return: if uri points to segment, then returns RV_THEN, else
        RV_ELSE   
        """
        res = False
        self.lock.acquire()
        try:
            if self.__session._stat(_uri.encode("cp1251")) == pm.RV_THEN:
                res = True
        finally:
            self.lock.release()
        return res
        
        
#    def appendObjs2Set(self, _seg, _set, _el_list):
#        """Appends list of element to specified set
#        @param _seg:    segment where links will be created
#        @type _seg:    sc_segment
#        @param _set:    set to append elements
#        @type _set:    sc_global_addr
#        @param _el_list:    list of elements that would be added to set
#        @type _el_list:    list (sc_global_addr)
#        """
#        self.lock.acquire()
#        try:
#            for el in _el_list:
#                a = self.__session.create_el(_seg, pm.SC_ARC)
#                self.__session.set_beg(a, _set)
#                self.__session.set_end(a, el)
#        except:
#            pass
#            
#        self.lock.release()
#            
    def appendObj2Sets(self, _seg, _obj, _set_list):
        """Appends object to specified sets
        @param _seg:    segment where links will be created
        @type _seg:    sc_segment
        @param _obj:    object that will be added to sets
        @type _obj:    sc_global_addr
        @param _set_list:    list of sets
        @type _set_list:    list
        """
        self.lock.acquire()
        try:
            for _set in _set_list:
                a = self.__session.create_el(_seg, pm.SC_A_CONST)
                self.__session.set_beg(_set)
                self.__session.set_end(_obj)
        except:
            pass        
        self.lock.release()
        
    def attach_wait(self, _wait, _type, _params, _len):
        """Attaches event to elements
        @param _wait: Wait object
        @type _wait: sc_event_multi
        @param _type: Event type
        @type _type: sc_wait_type
        @param _params: 
        @type _param: sc_param
        @param _len: Parameters length
        @type _len: int
        
        @return: operation result (sc_retval)   
        """
        self.lock.acquire()
        res = _wait.attach_to(self.__session, _type, _params, _len)
        self.lock.release()
        return res

    def change_type(self, _el, _type):
        """Changes element type
        @param _el:    element to change type
        @type _el:    sc_global_addr
        @param _type:    new specified type
        @type _type:    sc_type
        
        @return: operation result
        @rtype: sc_retval
        """
        self.lock.acquire()
        res = self.__session.change_type(_el, _type)
        self.lock.release()
        return res
    
    def create_el(self, _seg, _type):
        """Creates new element
        @param _seg: segment to create element in
        @type _seg: sc_segment
        @param _type: element type
        @type _type: sc_type
        
        @return: If element created, then returns it sc_global_addr, else - None    
        """
        res = None
        self.lock.acquire()
        res = self.__session.create_el(_seg, _type)
        self.lock.release()
        return res
    
    def create_el_full_uri(self, _uri, _type):
        """Creates sc-element by full uri
        @param _uri: element uri (paht)
        @type _uri: str
        @param _type: element type  
        @type _type: sc_type 
        
        @return: tuple (<bool>, <sc_global_addr>). First element of tuple is true, when 
        element created, else it will be false
        """
        str = _uri.encode("cp1251")
        segm = None
        name = None
        
        h_s = None
        h_el = None
        ind = 0
        ind = str.rfind('/')
        if ind != -1:
            name = str[ind + 1:len(str)]
            segm = str[0:ind]
            created = False
            
            self.lock.acquire()
            h_s = pm.create_segment_full_path(self.__session, segm)
            h_el = self.__session.find_by_idtf(name, h_s)
            if h_el == None:
                h_el = self.__session.create_el(h_s, _type)
                self.__session.set_idtf(h_el, name)
                created = True
                
            self.lock.release()    
            
            return (created, h_el)
        else:
            raise RuntimeError("Invalid uri '%s'" % _uri)

    
    def create_el_idtf(self, _segment, _type, _idtf):
        """Creates new element with identificator
        @param _segment: segment to create element in
        @type _segment: sc_segment
        @param _type: element type
        @type _type: sc_type 
        @param _idtf: element identificator
        @type _idtf: str     
        
        @return: tuple (<created>, <sc_global_addr>) 
        """
        res = (None, None)
        self.lock.acquire()
        try:
            el = self.__session.find_by_idtf(_idtf.encode("cp1251"), _segment)
        finally:
            self.lock.release()
        
        if el is not None:
            return False, el
        
        # creating element
        self.lock.acquire()
        try:
            el = self.__session.create_el(_segment, _type)
            self.__session.set_idtf(el, _idtf.encode("cp1251"))
        finally:
            self.lock.release()
        
        return True, el
        
    def create_iterator(self, _constr, _sink):
        """Creates iterator for a constraint
        @param _constr: constraint to create iterator
        @type _constr: sc_iterator
        @param _sink: flag to automatic iterator deletion
        @type _sink: bool
        
        @return: iterator object         
        """
        self.lock.acquire()
        res = self.__session.create_iterator(_constr, _sink)
        self.lock.release()
        return res       
        
    def create_segment_full_uri(self, _uri):
        """Creates segment by full path
        @param _uri: segment path
        @type _uri: str
        
        @return created segment 
        """
        self.lock.acquire()
        try:
            res = pm.create_segment_full_path(self.__session, _uri.encode("cp1251"))
        finally:
            self.lock.release()
        return res
    
    def find_el_full_uri(self, _uri):
        """Finds element by full uri
        @param _uri: full element uri
        @type _uri: str
        
        @return: sc_global_addr of founded element  
        """
        # getting semgment name
        n = _uri.rfind("/")
        if n == -1: raise RuntimeError("Invalid uri '%s'" % _uri)
        segUri = _uri[:n]
        # finding segment
        seg = self.find_segment(segUri)
        if seg is None: raise RuntimeError("Can't find segment '%s'" % segUri)
        idtf = _uri[n + 1:]
        return self.find_el_idtf(idtf, seg)
        
    
    def find_el_idtf(self, _idtf, _seg):
        """Finds element by identificator
        @param _idtf: element identificator
        @type _idtf: str
        @param _seg: segment to search element in
        @type _seg: sc_segment
        
        @return: If element founded, then returns it sc_global_addr, else - None     
        """
        self.lock.acquire()
        try:
            res = self.__session.find_by_idtf(_idtf.encode("cp1251"), _seg)
        finally:
            self.lock.release()
        return res
    
    def find_keynode_idtf(self, _idtf, _seg):
        """Finds keynode by identificator
        @param _idtf: keynode identificator
        @type _idtf: str
        @param _seg: segment to search
        @type _seg: sc_segment  
        
        @return: if keynode founded, then returns it sc_global_addr, else raise RuntimeError  
        """
        res = self.find_el_idtf(_idtf, _seg)
        if res is None:
            raise RuntimeError("Can't find keynode '%s'" % _idtf)
        return res
    
    def find_keynode_full_uri(self, _uri):
        """Finds keynode by full uri
        @param _uri: keynode uri
        @type _uri: str
        
        @return: if keynode founded, then returns it sc_global_addr, else raise RuntimeError  
        """
        res = self.find_el_full_uri(_uri)
        if res is None:
            raise RuntimeError("Can't find keynode '%s'" % _uri)
        return res
    
    def find_segment(self, _uri):
        """Finds segment by uri
        @param _uri: segment uri (path)
        @type _uri: str
        
        @return: Founded segment if it founded, else - None
        """
        self.lock.acquire()
        try:
            res = self.__session.find_segment(_uri.encode("cp1251"))
        finally:
            self.lock.release()        
        return res
    
    def gen3_f_a_f(self, _seg, _el1, _el3, _type):
        """Generates construction for 3 elements.
        1---2---3
        
        @param _seg: segment to create construction in
        @type _seg: sc_segment
        @param _el1: first element
        @type _el1: sc_global_addr
        @param _el3: third element
        @type _el3: sc_global_addr
        @param _type: type of generating element
        @type _type: sc_type
        
        @return: list of elements [el1, el2, el3]. Returns None if constructions wasn't created
        """
        assert (_el1 is not None) and (_el3 is not None)
        el2 = self.create_el(_seg, _type)
        if el2 is None: 
            return None
        
        if self.set_beg(el2, _el1) != pm.RV_OK:
            self.erase_el(el2)
            return None
        
        if self.set_end(el2, _el3) != pm.RV_OK:
            self.erase_el(el2)
            return None
        
        return [_el1, el2, _el3]
    
    def get_beg(self, _arc):
        """Returns begin element of arc
        @param _arc: arc element
        @type _arc: sc_global_addr
        
        @return: begin of arc  
        """
        self.lock.acquire()
        res = self.__session.get_beg(_arc)
        self.lock.release()
        return res
    
    def get_content(self, _el):
        """Gets content data for an element
        @param _el: element to get content
        @type _el: sc_global_addr  
        @return: Content object
        """
        self.lock.acquire()
        res = self.__session.get_content(_el)
        self.lock.release()
        
        return res
    
    def get_content_const(self, _el):
        """Gets content data for an element
        @param _el: element to get content
        @type _el: sc_global_addr  
        @return: Content object
        """
        self.lock.acquire()
        res = self.__session.get_content_const(_el)
        self.lock.release()
        
        return res
    
    def get_content_int(self, _el):
        """Gets value of int type content
        @param _el:    sc-address of element to get content
        @type _el:    sc_global_addr
        
        @return: if content have integer data, then return it, else
        return None          
        """
        cont = self.get_content(_el)
        
        if cont is None:
            return None
        
        self.lock.acquire()
        if cont.type() != pm.TCINT:
            self.lock.release()
            return None
        
        # getting data from content
        cont_data = cont.convertToCont()
        res = int(cont_data.i)
        
        self.lock.release()
        return res
    
    def get_content_real(self, _el):
        """Gets value of real type content
        @param _el: sc-address of element to get content
        @type _el: sc_global_addr
        
        @return: if content have real data, then return it, else
        return None         
        """
        cont = self.get_content(_el)
        
        if cont is None:
            return None
        
        self.lock.acquire()
        if cont.type() != pm.TCREAL:
            self.lock.release()
            return None 
        
        # getting data from content
        cont_data = cont.convertToCont()
        res = float(cont_data.r)
                
        self.lock.release()        
        return res
    
    def get_content_str(self, _el):
        """Gets value of string type content
        @param _el: sc-address of element to get content
        @type _el: sc_global_addr
        
        @return: if content have string data, then return it, else
        return None         
        """
        
        cont = self.get_content(_el)
        
        if cont is None:
            return None
        
        self.lock.acquire()
        if cont.type() != pm.TCSTRING:
            self.lock.release()
            return None 
        
        # getting data from content
        cont_data = cont.convertToCont()
        res = str(cont_data.d.ptr)
                
        self.lock.release()        
        return res
        
    def get_end(self, _arc):
        """Returns end element of arc
        @param _arc: arc element
        @type _arc: sc_global_addr
        
        @return: end of arc
        """
        self.lock.acquire()
        try:
            res = self.__session.get_end(_arc)
        finally:
            self.lock.release()
        return res
    
    def get_idtf(self, _el):
        """Returns element identificator
        @param _el: element to get identificator
        @type _el: sc_global_addr
        
        @return: element identificator
        """
        self.lock.acquire()
        try:
            res = self.__session.get_idtf(_el)
        finally:
            self.lock.release()
        return res
    
    def get_type(self, _el):
        """Gets element type
        @param _el: element to get type
        @type _el: sc_global_addr
        
        @return: element type (sc_type)
        """
        self.lock.acquire()
        try:
            res = self.__session.get_type(_el)
        finally:
            self.lock.release()
        return res
        
    
    def erase_el(self, _el):
        """Delete element from session
        @param _el: elemtn to delete
        @type _el: sc_global_addr  
        
        @return: operation result (sc_retval)
        """
        self.lock.acquire()
        try:
            res = self.__session.erase_el(_el)
        finally:
            self.lock.release()
        return res
    
    def mkdir_full_uri(self, _uri):
        """Creates directory by full uri
        @param _uri: directory uri
        @type _uri: str
        
        @return: operation result (bool)
        """
        self.lock.acquire()
        res = True
        try:
            l = len(_uri)
            ind = 1
            while ind != -1:
                ind = _uri.find('/', ind + 1, l)
                if ind == -1:
                    self.__session.mkdir(_uri.encode("cp1251"))
                    break 
                s = _uri[0:ind]
                self.__session.mkdir(s)
                
        except (RuntimeError, TypeError, NameError):
           res = False 
        self.lock.release()
        return res
    
    def open_segment(self, _uri):
        """Opens segment with specified path (uri)
        @param _uri: segment path
        @type _uri: str  
        """
        self.lock.acquire()
        try:
            res = self.__session.open_segment(_uri.encode("cp1251"))
        finally:
            self.lock.release()
        return res
    
    def sc_constraint_new(self, constr_uid, *arguments):
        """Creates constraint
        @param constr_uid: constarint uid
        @param arguments: constraint arguments   
        """
        constr = None
        info = None
        self.lock.acquire()
        info = pm.sc_constraint_get_info(constr_uid)
        self.lock.release()
        if not info :
            return None
        
        self.lock.acquire()
        constr = pm.sc_constraint_new_by_info(info)
        self.lock.release()
        if not constr :
            return None
        i = 0
        self.lock.acquire()
        params = pm.sc_paramArray_frompointer(constr.params)
        inp_spec = pm.sc_param_specArray_frompointer(info.input_spec)
        self.lock.release()
        
        for arg in arguments:
            p = pm.sc_param()
            if arg == None : raise RuntimeError("Parameters must be an objects")
            if inp_spec[i] == pm.SC_PD_TYPE:  
                p.type = arg
            elif inp_spec[i] == pm.SC_PD_ADDR or info.input_spec[i] == pm.SC_PD_ADDR_0:
                p.addr = arg 
            elif inp_spec[i] == pm.SC_PD_INT:
                p.i = arg
            else:
                self.lock.acquire()
                pm.sc_constraint_free(constr)
                self.lock.release()
            params[i] = p             
            i += 1

        return constr
    
    def search_one_shot(self, _constr, _sink, _len):
        """Searches elements by constraint and return first founded
        @param _const: constraint to search
        @type _constr: sc_constraint
        @param _sink: flag to auto remove constraint
        @type _sink: bool
        @param _len: length if result buffer (number of element in result)
        @type _len: int
        
        @return: if constructions was founded, then returns list of elements, else returns None
        @attention: if was founded more then one result constructions, then throws RuntimeError         
        """
        iter = self.create_iterator(_constr, _sink)
        res = None
        if not iter.is_over():
            res = []
            for i in xrange(_len):
                res.append(iter.value(i))
                
        # check number of results
        n = 0
        while not iter.is_over():
            n += 1
            iter.next()
            
        if n > 1:   raise RuntimeError("There are '%d' search results" % (n))
            
        return res
    
    def set_beg(self, _arc, _el):
        """Sets begin element for arc
        @param _arc: arc element
        @type _arc: sc_global_addr
        @param _el: begin element
        @type _el: sc_global_addr
        
        @return: operation result (sc_retval)    
        """
        self.lock.acquire()
        res = self.__session.set_beg(_arc, _el)
        self.lock.release()
        return res
    
    def set_content_int(self, _el, _data):
        """Sets int value content to element
        @param _el:    element to set content into
        @type _el:    sc_global_addr
        @param _data:    content data
        @type _data:    str
        """
        self.lock.acquire()
        cont = pm.Content.integer(_data)
        res = self.__session.set_content(_el, cont)
        self.lock.release()
        return res

    def set_content_real(self, _el, _data):
        """Sets real value content to element
        @param _el:    element to set content into
        @type _el:    sc_global_addr
        @param _data:    content data
        @type _data:    str
        """
        self.lock.acquire()
        cont = pm.Content.real(_data)
        res = self.__session.set_content(_el, cont)
        self.lock.release()
        return res

    
    def set_content_str(self, _el, _data):
        """Sets string content to element
        @param _el:    elment to set content into
        @type _el:    sc_global_addr
        @param _data:    content data
        @type _data:    str
        """
        self.lock.acquire()
        cont = pm.Content.string(_data)
        res = self.__session.set_content(_el, cont)
        self.lock.release()
        return res
    
    def set_end(self, _arc, _el):
        """Sets end element for arc
        @param _arc: arc element
        @type _arc: sc_global_addr
        @param _el: end element
        @type _el: sc_global_addr
        
        @return: operation result (sc_retval)
        """
        self.lock.acquire()
        res = self.__session.set_end(_arc, _el)
        self.lock.release()
        return res
    
    def set_idtf(self, _el, _idtf):
        """Sets new identificator for element 
        
        @param _el:    sc-element for adentificator setting
        @type _el:    sc_global_addr
        @param _idtf:    new text identificator
        @type _idtf:    str
        
        @return: if identificator changed, then return True, else - False
        @rtype: bool
        """
        if not self.find_el_idtf(_idtf, _el.seg):
            self.lock.acquire()
            try:
                rv = self.__session.set_idtf(_el, _idtf.encode("cp1251"))
            finally:
                self.lock.release()
                return False
            return rv == pm.RV_THEN
    
    def unlink(self, seg_uri):
        """Unlink segment
        @param seg_uri: segment uri to unlink
        @type seg_uri: str 
        
        @return: operation result (sc_retval)
        """
        self.lock.acquire()
        try:
            res = self.__session.unlink(seg_uri.encode("cp1251"))
        finally:
            self.lock.release()
        return res