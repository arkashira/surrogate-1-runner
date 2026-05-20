from surrogate_1.rules.base import BaseRule, Detection

class MyCustomRule(BaseRule):
    name = "My Custom Rule"
    description = "Detects usage of deprecated API X."
    severity = "high"

    def run(self, context):
        findings = []
        for file_path, content in context.files.items():
            if "deprecated_api_x" in content:
                findings.append(
                    Detection(
                        rule_name=self.name,
                        message="Deprecated API X used.",
                        severity=self.severity,
                        location=file_path,
                        metadata={"line": content.index("deprecated_api_x") + 1}
                    )
                )
        return findings