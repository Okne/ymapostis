# -*- coding: utf-8 -*-

# импорт базового модуля операции
from components.questions import operation
from suit.core.keynodes import ui

import sc_core.pm as sc
import suit.core.kernel as core
import suit.core.sc_utils as sc_utils
import sc_core.constants as sc_constants

import suit.core.environment as system_env
 
# получение текущей сессии
session = core.Kernel.session()
# открытие сегментов для сессии
session.open_segment(u"/etc/operations")
session.open_segment(u"/etc/questions")

# открываем сегмент пользовательского интерфейса
ui_segment = session.open_segment(system_env.URI_ui_core)
 
# поиск узла в базе знаний
sc_main_question = session.find_el_full_uri(u"/etc/questions/показать карту")
sc_operation_node = session.find_el_full_uri(u"/etc/operations/операция отображения карты")
sc_test_node = session.find_el_full_uri(u"/seb/test/test_geo_data")
sc_test_res_1 = session.find_el_full_uri(u"/seb/test/test_res_1")

arg_set_node = ui.arg_set
ymapsml_fmt_node = ui.format_ymapsml
 
# класс операции поиска всех выходящих дуг
class Op_show_map(operation.Operation):
 
    # функция инициализации
    def __init__(self):
        print "init: Show map operation"
        pass
 
    # функция проверки условия запуска
    @classmethod
    def checking(self, question):
        print "checking: Show map operation"
        # проверка входит ли вопрос в множество вопросов "поиск выходящих дуг"
        res = sc_utils.checkIncToSets(session,question,[sc_main_question],sc.SC_A_CONST|sc.SC_POS)
        if res is not None:
            return True
        else:
            return False
 
    # функция поиска ответа на вопрос
    def running(self, question):
        print "runing: Show map operation"
        
        res = []
        """targets = session.search3_f_a_a(question, sc.SC_A_CONST|sc.SC_POS, sc.SC_CONST|sc.SC_NODE)        
        # перебираем найденые элементы
        for target in targets:
            els = session.search3_f_a_a(target[2], sc.SC_A_CONST|sc.SC_POS, sc.SC_EMPTY)
            if els is not None:
                for el in els:
                    res.append(el[2])"""
                    
        #return test cont
        cont = sc_utils.searchOneShot(session.search3_f_a_a(sc_test_res_1, sc.SC_A_CONST|sc.SC_POS, sc.SC_CONST|sc.SC_NODE))[2]
        
        search_res_list = session.search3_f_a_a(cont, sc.SC_A_CONST|sc.SC_POS, sc.SC_CONST)
        if search_res_list is not None:
            for search_res in search_res_list:
                res.append(search_res[2])
        
                    
        #add sheet with type YMAPSML to display answer to
        
        """output_window = session.create_el(ui_segment, sc.SC_N_CONST)
        session.gen3_f_a_f(ui_segment, ymapsml_fmt_node, output_window, sc.SC_A_CONST)
        
        core.addOutputWindow(output_window)"""
        
        
        """input_param_set = None
        
        #get set of input parameters
        els = session.search3_f_a_f(question, sc.SC_A_CONST|sc.SC_POS, arg_set_node)
        result = sc_utils.searchOneShot(els)[2]
        
        assert result is not None
        input_param_set = result[2]
        
        res = []
        #search for output element from input_param and add all object in such set to result
        els = session.search3_f_a_a(input_param_set, sc.SC_A_CONST|sc.SC_POS, sc.SC_N_CONST)
        if els is not None:
            for el in els:
                elem_id = sc_utils.getLocalizedIdentifier(session, el[2])
                res.append(el[2])
                print "param id = %s" % (elem_id[0])"""
        
        """it = session.create_iterator(session.sc_constraint_new(sc_constants.CONSTR_5_a_a_f_a_a,
                                                           sc.SC_POS,
                                                           sc.SC_A_CONST | sc.SC_POS,
                                                           question,
                                                           sc.SC_A_CONST | sc.SC_POS,
                                                           sc.SC_POS), True)
        print "attributes for input arcs"
        while not it.is_over():
            elem_id = sc_utils.getLocalizedIdentifier(session, it.value(0))
            attr_id = sc_utils.getLocalizedIdentifier(session, it.value(4))
            print "elem id = %s  with attr id = %s" % (elem_id[0], attr_id[0])
            it.next()"""
        
        #show all input elements id's
        #print "input elements id's"
        #re = sc_utils.strInputIdtf(session, question)
        #print re
        
        # создаем множество для ответа
        #res = []
        # получаем элементы текущего вопроса
        """it = session.create_iterator(session.sc_constraint_new(sc_constants.CONSTR_3_f_a_a,
                                                           question,
                                                           sc.SC_A_CONST | sc.SC_POS,
                                                           sc.SC_CONST
                                                           ), True)
        print "ids of all question's elements"
        while not it.is_over():
            id = sc_utils.getLocalizedIdentifier(session, it.value(2))
            print "id = %s" % id[0]
            it.next()
        
        #test only"""
        #res.append(question)
        return res
 
    # метод возвращающий узел данной операции
    @classmethod
    #@staticmethod
    def getOperationNode(self):
        return sc_operation_node