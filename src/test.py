# -*- coding: utf-8 -*-
import sys
import re
import unittest

import module_test
import operator_test
import primary_test 
#import statement_test
import value_test

this = sys.modules[__name__]

def mods():
    for p in dir(this):
        #print(p)
        match = re.search(r'_test$', p)
        if match:
            yield getattr(this,p)

# for m in mods():
#     print(m)

s = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(m) for m in mods()])
unittest.TextTestRunner(verbosity=2).run(s)



