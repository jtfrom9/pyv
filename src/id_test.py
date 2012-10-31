# -*- coding: utf-8 -*-
import sys
import unittest

from test_common import TestCase, run_tests
import grammar

def _id_print(result):
    print(result.asXML())
    idAst = result[0]
    print("shortName={0}".format(idAst.shortName()))
    print("longName={0}".format(idAst.longName()))
    if idAst.hasIndex(): print("Index={0}".format(idAst.index))
    if idAst.hasRange(): print("Range={0}".format(idAst.range))
    if idAst.isHierachical():
        for index,id in enumerate(idAst.ids):
            print("  name[{0}] short={1}, long={2}".format(index,id.shortName(),id.longName()))

@testOf(grammar.simple_identifier)
def test169(self):
    _id_print(self.check_pass("hoge"))


@testOf(grammar.escaped_identifier)
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


@testOf(grammar.block_identifier)
def test173(self):
    pass


@testOf(grammar.escaped_arrayed_identifier)
def test174(self):
    pass


@testOf(grammar.module_instance_identifier)
def test178(self):
    _id_print(self.check_pass("hoge"))
    _id_print(self.check_pass("hoge[2:3]"))

@testOf(grammar._range)
def test182r(self):
    self.check_pass("[10:5]")

@testOf(grammar.simple_arrayed_identifier)
def test182(self):
    _id_print(self.check_pass("hoge[10:5]"))

@testOf(grammar.hierarchical_identifier)
def test185(self):
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
    

@testOf(grammar.escaped_hierarchical_identifier)
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


@testOf(grammar.escaped_hierarchical_branch)
def test196(self):
    pass
    

if __name__=='__main__':
    run_tests()

