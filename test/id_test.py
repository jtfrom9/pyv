# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import (
    testOf, testOfSkipped,
    run_tests, debug, grammar, _id_print )

@testOf(grammar.simple_identifier)
def test169(self):
    #_id_print(self.check_pass("hoge"))
    #debug(grammar.simple_identifier)
    self.check_pass("hoge")


@testOfSkipped(grammar.escaped_identifier)
def test170(self):
    pass


@testOf(grammar.identifier)
def test171(self):
    _id_print(self.check_pass("hoge"))


@testOf(grammar.arrayed_identifier)
def test172(self):
    _id_print(self.check_pass("hoge[10:5]"))
    _id_print(self.check_pass("hoge_[1:0]"))
#    _id_print(self.check_pass("hoge[HOGE:Foo(0)]"))
    _id_print(self.check_pass("hoge"))


@testOfSkipped(grammar.block_identifier)
def test173(self):
    pass


@testOfSkipped(grammar.escaped_arrayed_identifier)
def test174(self):
    pass


@testOf(grammar.module_instance_identifier)
def test178(self):
    _id_print(self.check_pass("hoge"))
    _id_print(self.check_pass("hoge[2:3]"))

@testOf(grammar.range_)
def test182r(self):
    self.check_pass("[10:5]")

@testOf(grammar.simple_arrayed_identifier)
def test182(self):
    _id_print(self.check_pass("hoge[10:5]"))

@testOf(grammar.hierarchical_identifier)
def test185(self):
    # debug(grammar.hierarchical_identifier)
    # debug(grammar.simple_hierarchical_identifier)
    # debug(grammar.simple_hierarchical_branch)
    _id_print(self.check_pass("x.abc[0]"))
    _id_print(self.check_pass("x.abc[1]"))
    _id_print(self.check_pass("hoge[5].foo[1]"))
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1]"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))
    _id_print(self.check_pass("hoge[5].foo"))
    _id_print(self.check_pass("hoge[5].foo.bar"))
    _id_print(self.check_pass("hoge[5].foo.bar.A[10]"))
    _id_print(self.check_pass("foo.bar.hoge[5].A[1]"))
    self.check_fail("-X")


@testOfSkipped(grammar.escaped_hierarchical_identifier)
def test186(self):
    pass


@testOf(grammar.simple_hierarchical_identifier)
def test187(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].a"))
    _id_print(self.check_pass("hoge[5].foo[1].bar"))
    _id_print(self.check_pass("hoge[5].foo[1].bar[10]"))

@testOf(grammar.system_task_identifier)
def test194(self):
    _id_print(self.check_pass("$foo"))
    _id_print(self.check_pass("$display"))
    _id_print(self.check_pass("$test$valuearg"))

@testOf(grammar.simple_hierarchical_branch)
def test195(self):
    _id_print(self.check_pass("hoge[5]"))
    _id_print(self.check_pass("hoge[5].foo[1]"))
    _id_print(self.check_pass("hoge[5].foo"))
    _id_print(self.check_pass("hoge[5].foo.bar"))
    _id_print(self.check_pass("hoge[5].foo.bar.A[10]"))


@testOfSkipped(grammar.escaped_hierarchical_branch)
def test196(self):
    pass
    

if __name__=='__main__':
    run_tests()

