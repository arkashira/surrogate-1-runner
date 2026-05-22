const ambiguousTerms = ['some', 'many', 'various', 'several', 'few'];

function detectAmbiguity(specSections) {
  const warnings = [];
  
  specSections.forEach((section, index) => {
    const matches = ambiguousTerms.filter(term => section.toLowerCase().includes(term));
    if (matches.length > 0) {
      const warning = {
        sectionIndex: index,
        ambiguousTerms: matches,
        suggestedRephrasing: suggestRephrasing(section, matches)
      };
      warnings.push(warning);
    }
  });

  return warnings;
}

function suggestRephrasing(section, matches) {
  let rephrasedSection = section;
  matches.forEach(match => {
    rephrasedSection = rephrasedSection.replace(match, `a specific number of`);
  });
  return rephrasedSection;
}

module.exports = {
  detectAmbiguity
};