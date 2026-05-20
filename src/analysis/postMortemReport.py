import markdown
from analysis.patternDetector import PatternDetector

class PostMortemReport:
    def __init__(self, data):
        self.data = data

    def generate_report(self):
        pattern_detector = PatternDetector(self.data)
        patterns = pattern_detector.detect_patterns()
        suggestions = pattern_detector.generate_remediation_suggestions(patterns)

        report = "# Post-Mortem Report\n\n"
        report += "## Timeline of Correlated Events\n\n"
        report += self._generate_timeline()

        report += "\n## Patterns in Model Decisions Leading to Alerts\n\n"
        for i, pattern in enumerate(patterns):
            report += f"### Pattern {i+1}\n\n"
            report += self._generate_pattern_section(pattern)

        report += "\n## Remediation Suggestions\n\n"
        for i, suggestion in enumerate(suggestions):
            report += f"### Suggestion {i+1}\n\n"
            report += self._generate_suggestion_section(suggestion)

        return markdown.markdown(report)

    def _generate_timeline(self):
        # Generate timeline of correlated events
        timeline = ""
        for event in self.data:
            timeline += f"* {event}\n"

        return timeline

    def _generate_pattern_section(self, pattern):
        section = ""
        for feature, (mean, std) in pattern.items():
            section += f"* {feature}: mean={mean}, std={std}\n"

        return section

    def _generate_suggestion_section(self, suggestion):
        section = ""
        for feature, suggestion_text in suggestion.items():
            section += f"* {feature}: {suggestion_text}\n"

        return section