# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2, _id_print
import grammar
import action

@TestCase2(grammar.simple_identifier)
def test169(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.escaped_identifier)
def test170(self):
    pass


@TestCase2(grammar.identifier)
def test171(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.arrayed_identifier)
def test172(self):
    _id_print(self.check_pass("hoge[10:5]"))
    _id_print(self.check_pass("hoge_[1:0]"))
#    _id_print(self.check_pass("hoge[HOGE:Foo(0)]"))
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.block_identifier)
def test173(self):
    pass


@TestCase2(grammar.escaped_arrayed_identifier)
def test174(self):
    pass


@TestCase2(grammar.event_identifier)
def test175(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.function_identifier)
def test176(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.module_identifier)
def test177(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.module_instance_identifier)
def test178(self):
    _id_print(self.check_pass("hoge"))
    _id_print(self.check_pass("hoge[2:3]"))

@TestCase2(grammar.net_identifier)
def test179(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.port_identifier)
def test180(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.real_identifier)
def test181(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.simple_arrayed_identifier)
def test182(self):
    _id_print(self.check_pass("hoge[10:5]"))


@TestCase2(grammar.task_identifier)
def test183(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.variable_identifier)
def test184(self):
    _id_print(self.check_pass("hoge"))


@TestCase2(grammar.hierarchical_identifier)
def test185(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1]"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))
    _id_print(self.check_pass("hoge[5].foo"))
    _id_print(self.check_pass("hoge[5].foo.bar"))
    _id_print(self.check_pass("hoge[5].foo.bar.A[10]"))

@TestCase2(grammar.escaped_hierarchical_identifier)
def test186(self):
    pass


@TestCase2(grammar.simple_hierarchical_identifier)
def test187(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))


@TestCase2(grammar.hierarchical_task_identifier)
def test188(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))


@TestCase2(grammar.hierarchical_block_identifier)
def test189(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))


@TestCase2(grammar.hierarchical_event_identifier)
def test190(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))


@TestCase2(grammar.hierarchical_net_identifier)
def test191(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))


@TestCase2(grammar.hierarchical_variable_identifier)
def test192(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))

@TestCase2(grammar.hierarchical_function_identifier)
def test193(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))

@TestCase2(grammar.system_task_identifier)
def test194(self):
    _id_print(self.check_pass("$foo"))
    _id_print(self.check_pass("$display"))
    _id_print(self.check_pass("$test$valuearg"))

@TestCase2(grammar.simple_hierarchical_branch)
def test195(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].foo[1]"))
    _id_print(self.check_pass("hoge[5].foo"))
    _id_print(self.check_pass("hoge[5].foo.bar"))
    _id_print(self.check_pass("hoge[5].foo.bar.A[10]"))


@TestCase2(grammar.escaped_hierarchical_branch)
def test196(self):
    pass
    

if __name__=='__main__':
    unittest.main()

