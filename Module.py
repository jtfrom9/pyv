
class ParameterList:
    def __init__(self,param_list):
        self.__params = param_list

    def params(self):
        for p in self.__params:
            yield p

class Module:
    def __init__(self,name,param):
        self.__name = name
        self.__param = param

    def name(self):
        return self.__name

    def param(self):
        return self.__param

