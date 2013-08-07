# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import (
    testOf, testOfSkipped,
    run_tests, debug, grammar, print_result_as_id )

@testOf(grammar.simple_identifier)
def test169(self):
    #print_result_as_id(self.try_parse_pass("hoge"))
    #debug(grammar.simple_identifier)
    self.try_parse_pass("hoge")


@testOfSkipped(grammar.escaped_identifier)
def test170(self):
    pass


@testOf(grammar.identifier)
def test171(self):
    print_result_as_id(self.try_parse_pass("hoge"))


@testOf(grammar.arrayed_identifier)
def test172(self):
    print_result_as_id(self.try_parse_pass("hoge[10:5]"))
    print_result_as_id(self.try_parse_pass("hoge_[1:0]"))
#    print_result_as_id(self.try_parse_pass("hoge[HOGE:Foo(0)]"))
    print_result_as_id(self.try_parse_pass("hoge"))


@testOfSkipped(grammar.block_identifier)
def test173(self):
    pass


@testOfSkipped(grammar.escaped_arrayed_identifier)
def test174(self):
    pass


@testOf(grammar.module_instance_identifier)
def test178(self):
    print_result_as_id(self.try_parse_pass("hoge"))
    print_result_as_id(self.try_parse_pass("hoge[2:3]"))

@testOf(grammar.range_)
def test182r(self):
    self.try_parse_pass("[10:5]")

@testOf(grammar.simple_arrayed_identifier)
def test182(self):
    print_result_as_id(self.try_parse_pass("hoge[10:5]"))

@testOf(grammar.hierarchical_identifier)
def test185(self):
    # debug(grammar.hierarchical_identifier)
    # debug(grammar.simple_hierarchical_identifier)
    # debug(grammar.simple_hierarchical_branch)
    print_result_as_id(self.try_parse_pass("x.abc[0]"))
    print_result_as_id(self.try_parse_pass("x.abc[1]"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo[1]"))
    print_result_as_id(self.try_parse_pass("hoge[5]"))
    print_result_as_id(self.try_parse_pass("hoge[5].a"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo[1]"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo[1].bar"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo[1].bar[10]"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo.bar"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo.bar.A[10]"))
    print_result_as_id(self.try_parse_pass("foo.bar.hoge[5].A[1]"))
    self.try_parse_fail("-X")


@testOfSkipped(grammar.escaped_hierarchical_identifier)
def test186(self):
    pass


@testOf(grammar.simple_hierarchical_identifier)
def test187(self):
    print_result_as_id(self.try_parse_pass("hoge[5]"))
    print_result_as_id(self.try_parse_pass("hoge[5].a"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo[1].bar"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo[1].bar[10]"))

@testOf(grammar.system_task_identifier)
def test194(self):
    print_result_as_id(self.try_parse_pass("$foo"))
    print_result_as_id(self.try_parse_pass("$display"))
    print_result_as_id(self.try_parse_pass("$test$valuearg"))

@testOf(grammar.simple_hierarchical_branch)
def test195(self):
    print_result_as_id(self.try_parse_pass("hoge[5]"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo[1]"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo.bar"))
    print_result_as_id(self.try_parse_pass("hoge[5].foo.bar.A[10]"))


@testOfSkipped(grammar.escaped_hierarchical_branch)
def test196(self):
    pass
    

if __name__=='__main__':
    run_tests()

