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
Created on 29.01.2010

@author: Denis Koronchik
'''

from LayoutGroup import LayoutGroupDepth
import ogre.renderer.OGRE as ogre
import math, random
import suit.core.render.engine as render_engine
from suit.core.objects import Object
import suit.core.objects as objects

class LayoutGroupForceSimple(LayoutGroupDepth):
    
    def __init__(self,
                 _step_max = 0.00005,
                 _step_min = 0.0015, 
                 _max_rep_length = 30.0,
                 _max_force = 0.3,
                 _repulsion = 24,
                 _rigidity = 16,
                 _length = 5.5,
                 _gravity = 0.05,
                 _windowBorder = -7.0):
        
        LayoutGroupDepth.__init__(self)
        
        # map of forces
        self.step_max = _step_max
        self.step = self.step_max
        self.prevMaxF = 0.0
        self.minMaxF = 0.000015
        self.maxf = 0.0
        self.step_min = _step_min
        self.lengthOld = 0
        
        self.max_rep_length = _max_rep_length
        self.max_force = _max_force
        
        
        self.repulsion = _repulsion
        self.rigidity = _rigidity
        self.length = _length
        self.gravity = _gravity
        self.dr = 0.1
        self.kstep = 0.95
        self.df = 0.0001
        
        self.radius = 1
        self.angle = 0.0
        
        self.needModeUpdate = True
        
    def __del__(self):
        LayoutGroupDepth.__del__(self)

    def _addObjectToGroup(self, _object):
        """Append object to layout group
        """
        res = LayoutGroupDepth._addObjectToGroup(self, _object)
#        self.step = self.step_max
        self.need_layout = True
        
#        if render_engine.viewMode is render_engine.Mode_Isometric:
#            _object.setPosition(ogre.Vector3(math.cos(self.angle), math.sin(self.angle), 0.0) * self.radius)
#        else:
#            _object.setPosition(ogre.Vector3(math.cos(self.angle), math.sin(self.angle), math.sin(self.angle) + math.cos(self.angle)) * self.radius)
        #self.radius += 1.0 / 36.0
        #self.angle += 0.17
        
        # calculate object position as an geometrical center of connected to it objects
        pos = None
        count = 0
        objs = _object.getLinkedObjects(Object.LS_IN)
        for obj in objs:
            if obj.getBegin() in self.objects:
                if pos is None:
                    pos = obj.getPosition()
                    count += 1
                else:
                    pos += obj.getPosition()
                    count += 1
                
            
        objs = _object.getLinkedObjects(Object.LS_OUT)
        for obj in objs:
            if obj.getBegin() in self.objects:
                if pos is None:
                    pos = obj.getPosition()
                    count += 1
                else:
                    pos += obj.getPosition()
                    count += 1
                    
        if pos is not None:
            pos = pos / float(count)
        else:
            pos = ogre.Vector3(0, 0, 0)
            
        if render_engine.viewMode is render_engine.Mode_Isometric:
            pos = pos + ogre.Vector3(math.cos(len(self.nodes) * (math.pi**2)), math.sin(len(self.nodes)* (math.pi**2)), 0.0) * 2
        else:
            pos = pos + ogre.Vector3(2 * math.cos(len(objs)), 2 * math.sin(len(objs)), math.cos(len(objs)) + math.sin(len(objs)))
        _object.setPosition(pos)
   
        return res
        
    def _removeObjectFromGroup(self, _object):
        """Removes object from layout group
        """
        res = LayoutGroupDepth._removeObjectFromGroup(self, _object)
#        self.step = self.step_max
        self.need_layout = True
        
        return res
        
    def _removeAllObjectsFromGroup(self):
        """Removes all objects from layout group
        """
        res = LayoutGroupDepth._removeAllObjectsFromGroup(self)
#        self.step = self.step_max
        self.need_layout = True
        
        return res
    
    def _mode_changed_impl(self):
        """Sets flag to update Z axis positions 
        """
        self.needModeUpdate = True
        
        LayoutGroupDepth._mode_changed_impl(self)
    
    def _apply(self):
        """Applies force directed layout to group
        """
        LayoutGroupDepth._apply(self)
        
        ln = len(self.objects)
        if ln == 0: return
        if not self.lengthOld == ln: 
            self.step = self.step_max / len(self.objects)
            self.prevMaxF = 0.0
            self.prevStep = self.step
            
        self.lengthOld = ln
             
#        import math
#        items_count = len(self.nodes)
#        
#        if items_count != 0:
#            da = 2 * math.pi / items_count
#            angle = 0
#            radius = 5
#            for obj in self.nodes:
#                # set new position
#                x = radius * math.cos(angle) - obj.scale.x / 2
#                y = radius * math.sin(angle) - obj.scale.y / 2
#                z = 0
#                obj.setPosition(ogre.Vector3(x, y, z))
#                angle += da
#
        
                
        
        n_obj = []
        n_obj.extend(self.nodes)
        n_obj.extend(self.sheets)
        n = len(n_obj)
        
        #if n == 0:
        #    self.needModeUpdate = False 
        #    return
        
        forces = [ogre.Vector3(0, 0, 0)] * n
        obj_f = {}
        self.maxf = 0.0
        
#        self.step = self.step * 0.99
        
        o_pos = []
        # updating on mode
        if self.needModeUpdate:
            angle = 0.0
            radius = 1.0
            
            for obj in n_obj:
                pos = obj.getPosition()
                if render_engine.viewMode is render_engine.Mode_Isometric:
                    o_pos.append(ogre.Vector3(pos.x, pos.y, 0.0))
                else:
                    o_pos.append(ogre.Vector3(pos.x, pos.y, math.cos(angle) * radius))
                    angle += 0.25
                    radius += 0.1
                    
            self.needModeUpdate = False
        else:
            for obj in n_obj:
                o_pos.append(obj.getPosition())
                   
        # calculating repulsion forces
        for idx in xrange(n):
            obj_f[n_obj[idx]] = idx
            
            p1 = o_pos[idx]
            
            l = p1.length()
            
            #if l > 3:
            # mode sheet objects bottom
            f = None
#            if isinstance(n_obj[idx], objects.ObjectSheet):
#                f = ogre.Vector3(p1.x / 5.0, p1.y - self.windowBorder, 0)
#            else:
#                f = (p1) * self.gravity * (l - 3.0)
            inv_mass1 = 0.6
            if isinstance(n_obj[idx], objects.ObjectSheet):
                inv_mass1 = 1.6
                
            #f = (p1) * self.gravity * (l - 3.0)
            #forces[idx] = forces[idx] - f
            
            for jdx in xrange(idx + 1, n):
                p2 = o_pos[jdx]
                p = (p1 - p2)
                l = p.length()
#                p.normalise()
                              
                if l > self.max_rep_length: continue    # don't calculate repulsion if distance between objects is to
                
                #if l > 0.5:
                if l < 0.5: l += 0.25
                f = p * self.repulsion / l / l / l
                #else:
                #    f = ogre.Vector3(math.cos(0.17 * idx) * self.length * 7, math.sin(0.17 * (idx + 1)) * self.length * 7, 0) 
                
                inv_mass2 = 0.6
                if isinstance(n_obj[jdx], objects.ObjectSheet):
                    inv_mass2 = 1.6
                
                # append forces to nodes
#                if idx != 0:
                forces[idx] = forces[idx] + f * inv_mass1
                forces[jdx] = forces[jdx] - f * inv_mass2
                
                               
        # calculating springs
        for line in self.lines:
            
            ob = line.getBegin()
            oe = line.getEnd()
            if ob is None or oe is None:    continue
            
            p1 = ob.getPosition()
            p2 = oe.getPosition()
            
            p = (p2 - p1)
            l = p.length()
            
            if l > 0:
                l = l - self.length
                #p.normalise()
#                f = p*(self.rigidity * (l - self.length) / l)
                #cnt = self.getLinkedCount(ob) + self.getLinkedCount(oe)
                #f = p*(self.rigidity * (l - self.getLineLength(cnt)) / l)
                f = p * self.rigidity * l#math.log(l)
                
#                if (f.length() > 10):
#                    f = p * self.rigidity / l
            else:
                f = ogre.Vector3(1, 1, 0)
                
            if obj_f.has_key(ob) and not isinstance(ob, objects.ObjectLine):
                idx = obj_f[ob]
                forces[idx] = forces[idx] + f
            if obj_f.has_key(oe) and not isinstance(oe, objects.ObjectLine):
                idx = obj_f[oe]
                forces[idx] = forces[idx] - f

        
        # apply forces to objects
#        df = forces[0]
        maxf = 0.0
        for idx in xrange(n):
            f = forces[idx]
            # getting maximum force
            maxf = max([maxf, f.length()])          
        
#        if maxf >= self.max_force:
#            self.step = self.step_max
#        else:
        
        v = self.dr / (maxf + 0.01)
        if (maxf - self.prevMaxF) > self.df:
            self.step = min([self.kstep * self.step, v])
        else:
            self.step = max([v, self.step])
            
        self.prevMaxF = maxf
            
        #newStep = max([self.step * 0.98, min([self.step * 1.02, self.dr / (maxf + 0.01)])])#self.step * 0.97
    
        for idx in xrange(n):
            f = forces[idx]
            offset = f * self.step
            self.maxf = max([self.maxf, offset.length()])
            pos = o_pos[idx] + f * self.step
            if render_engine.viewMode is render_engine.Mode_Isometric:
                pos = pos * ogre.Vector3(1, 1, 0)
            n_obj[idx].setPosition(pos)  
    
        print self.maxf
#        self.prevStep = self.step
        #self.need_layout = self.step > self.step_min
        self.need_layout = self.minMaxF < self.maxf#self.step > self.step_min

    def getLineLength(self, cnt):
        """Calculates length for a line depending on output/input arcs count
        """
        return max([self.length, cnt / 3.0])
    
    def getLinkedCount(self, obj):
        return len(obj.linkedObjects[Object.LS_OUT]) + len(obj.linkedObjects[Object.LS_IN])