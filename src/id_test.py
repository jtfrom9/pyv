# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import GrammarTestCase, TestCase2
import grammar
import action


@TestCase2(grammar.simple_identifier)
def test169(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.escaped_identifier)
def test170(self):
    pass


@TestCase2(grammar.identifier)
def test171(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.arrayed_identifier)
def test172(self):
    print(self.check_pass("hoge[10:5]").asXML())
    print(self.check_pass("hoge_[1:0]").asXML())
#    print(self.check_pass("hoge[HOGE:Foo(0)]").asXML())
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.block_identifier)
def test173(self):
    pass


@TestCase2(grammar.escaped_arrayed_identifier)
def test174(self):
    pass


@TestCase2(grammar.event_identifier)
def test175(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.function_identifier)
def test176(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.module_identifier)
def test177(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.module_instance_identifier)
def test178(self):
    print(self.check_pass("hoge").asXML())
    print(self.check_pass("hoge[2:3]").asXML())

@TestCase2(grammar.net_identifier)
def test179(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.port_identifier)
def test180(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.real_identifier)
def test181(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.simple_arrayed_identifier)
def test182(self):
    print(self.check_pass("hoge[10:5]").asXML())


@TestCase2(grammar.task_identifier)
def test183(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.variable_identifier)
def test184(self):
    print(self.check_pass("hoge").asXML())


@TestCase2(grammar.hierarchical_identifier)
def test185(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1]").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())
    print(self.check_pass("hoge[5].foo").asXML())
    print(self.check_pass("hoge[5].foo.bar").asXML())
    print(self.check_pass("hoge[5].foo.bar.A[10]").asXML())

@TestCase2(grammar.escaped_hierarchical_identifier)
def test186(self):
    pass


@TestCase2(grammar.simple_hierarchical_identifier)
def test187(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())


@TestCase2(grammar.hierarchical_task_identifier)
def test188(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())


@TestCase2(grammar.hierarchical_block_identifier)
def test189(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())


@TestCase2(grammar.hierarchical_event_identifier)
def test190(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())


@TestCase2(grammar.hierarchical_net_identifier)
def test191(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())


@TestCase2(grammar.hierarchical_variable_identifier)
def test192(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())

@TestCase2(grammar.hierarchical_function_identifier)
def test193(self):
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].a").asXML())
    print(self.check_pass("hoge[5].foo[1].bar").asXML())
    print(self.check_pass("hoge[5].foo[1].bar[10]").asXML())

@TestCase2(grammar.system_task_identifier)
def test194(self):
    print(self.check_pass("$foo").asXML())
    print(self.check_pass("$display").asXML())
    print(self.check_pass("$test$valuearg").asXML())

@TestCase2(grammar.simple_hierarchical_branch)
def test195(self):
    def _print(result):
        print(result.asXML())
        
    print(self.check_pass("hoge[5]").asXML())
    print(self.check_pass("hoge[5].foo[1]").asXML())
    print(self.check_pass("hoge[5].foo").asXML())
    print(self.check_pass("hoge[5].foo.bar").asXML())
    print(self.check_pass("hoge[5].foo.bar.A[10]").asXML())


@TestCase2(grammar.escaped_hierarchical_branch)
def test196(self):
    pass
    

if __name__=='__main__':
    unittest.main()

