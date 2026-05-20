import ast
import typing as t

from surrogates.analysis.base import LintRule, FunctionInfo, Severity

class UnrestrictedPublicFunctionRule(LintRule):
    """Check for public functions without access control checks."""

    def __init__(self, config: t.Dict):
        super().__init__("unrestricted-public-function", "MEDIUM")
        self.whitelist = config.get("whitelist", [])

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Skip builtins and methods
        if node.name.startswith("__") or node.name.startswith("lambda"):
            return

        # Check if function is marked as public/external
        is_public = False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "public":
                is_public = True
                break

        if not is_public:
            return

        # Check if function is pure (no side effects)
        is_pure = True
        for stmt in node.body:
            if isinstance(stmt, ast.Call):
                # If it calls any non-whitelisted functions or accesses external state
                if not self._is_whitelisted(stmt.func):
                    is_pure = False
                    break
            elif isinstance(stmt, ast.Break) or isinstance(stmt, ast.Continue):
                is_pure = False
                break

        # Check for access control checks
        has_access_check = False
        for stmt in node.body:
            if isinstance(stmt, ast.Expr):
                expr = stmt.value
                if isinstance(expr, ast.Call):
                    if isinstance(expr.func, ast.Name) and expr.func.id in ("require", "assert"):
                        # Check if argument references access control variable
                        if isinstance(expr.args[0], ast.Name) and expr.args[0].id in ("auth", "user", "role"):
                            has_access_check = True
                            break

        # Report if function is public and doesn't have access checks
        if is_public and not has_access_check and not is_pure:
            self.report(
                node,
                message="Public function lacks access control checks",
                severity=Severity.MEDIUM,
                details={
                    "function": node.name,
                    "is_pure": is_pure,
                    "has_access_check": has_access_check
                }
            )

    def _is_whitelisted(self, node: ast.AST) -> bool:
        """Check if function is in the whitelist."""
        if isinstance(node, ast.Name):
            return node.id in self.whitelist
        elif isinstance(node, ast.Attribute):
            return node.attr in self.whitelist
        return False