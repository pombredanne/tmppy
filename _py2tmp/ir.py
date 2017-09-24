#  Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Iterable, Union

class ExprType:
    def __str__(self) -> str: ... # pragma: no cover

    def __eq__(self, other) -> bool: ... # pragma: no cover

class BoolType(ExprType):
    def __str__(self):
        return 'bool'

    def __eq__(self, other):
        return isinstance(other, BoolType)

class TypeType(ExprType):
    def __str__(self):
        return 'Type'

    def __eq__(self, other):
        return isinstance(other, TypeType)

class FunctionType(ExprType):
    def __init__(self, argtypes: List[ExprType], returns: ExprType):
        self.argtypes = argtypes
        self.returns = returns

    def __str__(self):
        return "(%s) -> %s" % (
            ', '.join(str(arg)
                      for arg in self.argtypes),
            str(self.returns))

    def __eq__(self, other):
        return isinstance(other, FunctionType) and self.__dict__ == other.__dict__

class ListType(ExprType):
    def __init__(self, elem_type: ExprType):
        assert not isinstance(elem_type, FunctionType)
        self.elem_type = elem_type

    def __str__(self):
        return "List[%s]" % str(self.elem_type)

    def __eq__(self, other):
        return isinstance(other, ListType) and self.__dict__ == other.__dict__

class Expr:
    def __init__(self, type: ExprType):
        self.type = type

    # Note: it's the caller's responsibility to de-duplicate VarReference objects that reference the same symbol, if
    # desired.
    def get_free_variables(self) -> 'Iterable[VarReference]': ... # pragma: no cover

class FunctionArgDecl:
    def __init__(self, type: ExprType, name: str = ''):
        self.type = type
        self.name = name

class VarReference(Expr):
    def __init__(self, type: ExprType, name: str, is_global_function: bool):
        super().__init__(type=type)
        assert name
        self.name = name
        self.is_global_function = is_global_function

    def get_free_variables(self):
        if not self.is_global_function:
            yield self

class MatchCase:
    def __init__(self, type_patterns: List[str], matched_var_names: List[str], expr: Expr):
        self.type_patterns = type_patterns
        self.matched_var_names = matched_var_names
        self.expr = expr

    def is_main_definition(self):
        return set(self.type_patterns) == set(self.matched_var_names)

class MatchExpr(Expr):
    def __init__(self, matched_exprs: List[Expr], match_cases: List[MatchCase]):
        assert matched_exprs
        assert match_cases
        for match_case in match_cases:
            assert len(match_case.type_patterns) == len(matched_exprs)
            assert match_case.expr.type == match_cases[0].expr.type
        super().__init__(type=match_cases[0].expr.type)
        self.matched_exprs = matched_exprs
        self.match_cases = match_cases

        assert len([match_case
                    for match_case in match_cases
                    if match_case.is_main_definition()]) <= 1

    def get_free_variables(self):
        for expr in self.matched_exprs:
            for var in expr.get_free_variables():
                yield var
        for match_case in self.match_cases:
            local_vars = set(match_case.matched_var_names)
            for var in match_case.expr.get_free_variables():
                if var.name not in local_vars:
                    yield var

class BoolLiteral(Expr):
    def __init__(self, value: bool):
        super().__init__(BoolType())
        self.value = value

    def get_free_variables(self):
        if False:
            yield

class TypeLiteral(Expr):
    def __init__(self, cpp_type: str):
        super().__init__(type=TypeType())
        self.cpp_type = cpp_type

    def get_free_variables(self):
        if False:
            yield

class ListExpr(Expr):
    def __init__(self, elem_type: ExprType, elem_exprs: List[Expr]):
        assert not isinstance(elem_type, FunctionType)
        super().__init__(type=ListType(elem_type))
        self.elem_type = elem_type
        self.elem_exprs = elem_exprs

    def get_free_variables(self):
        for expr in self.elem_exprs:
            for var in expr.get_free_variables():
                yield var

class FunctionCall(Expr):
    def __init__(self, fun_expr: Expr, args: List[Expr]):
        assert isinstance(fun_expr.type, FunctionType)
        assert len(fun_expr.type.argtypes) == len(args)
        super().__init__(type=fun_expr.type.returns)
        self.fun_expr = fun_expr
        self.args = args

    def get_free_variables(self):
        for var in self.fun_expr.get_free_variables():
            yield var
        for expr in self.args:
            for var in expr.get_free_variables():
                yield var

class EqualityComparison(Expr):
    def __init__(self, lhs: Expr, rhs: Expr):
        super().__init__(type=BoolType())
        assert lhs.type == rhs.type
        assert not isinstance(lhs.type, FunctionType)
        self.lhs = lhs
        self.rhs = rhs

    def get_free_variables(self):
        for expr in (self.lhs, self.rhs):
            for var in expr.get_free_variables():
                yield var

class Assert:
    def __init__(self, expr: Expr, message: str):
        assert isinstance(expr.type, BoolType)
        self.expr = expr
        self.message = message

class Assignment:
    def __init__(self, lhs: VarReference, rhs: Expr):
        assert lhs.type == rhs.type
        self.lhs = lhs
        self.rhs = rhs

class FunctionDefn:
    def __init__(self, name: str, args: List[FunctionArgDecl], asserts_and_assignments: List[Union[Assert, Assignment]], expr: Expr):
        self.name = name
        self.args = args
        self.asserts_and_assignments = asserts_and_assignments
        self.expr = expr

class Module:
    def __init__(self, function_defns: List[FunctionDefn], assertions: List[Assert]):
        self.function_defns = function_defns
        self.assertions = assertions
