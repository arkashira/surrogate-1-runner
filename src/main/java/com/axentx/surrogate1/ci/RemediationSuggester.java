package com.axentx.surrogate1.ci;

import com.axentx.surrogate1.utils.Suggestion;
import com.axentx.surrogate1.utils.SuggestionFactory;
import com.axentx.surrogate1.utils.SuggestionStore;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.kohsuke.github.GHIssue;
import org.kohsuke.github.GHRepository;

import java.io.IOException;
import java.util.List;

public class RemediationSuggester {
    private static final Logger logger = LoggerFactory.getLogger(RemediationSuggester.class);
    private final SuggestionStore suggestionStore;
    private final SuggestionFactory suggestionFactory;

    public RemediationSuggester(SuggestionStore suggestionStore, SuggestionFactory suggestionFactory) {
        this.suggestionStore = suggestionStore;
        this.suggestionFactory = suggestionFactory;
    }

    public void suggestRemediations(GHRepository repo, List<GHIssue> issues) throws IOException {
        for (GHIssue issue : issues) {
            if (issue.hasLabel("security")) {
                String fixSteps = suggestionFactory.createFixSteps(issue.getTitle(), issue.getBody());
                Suggestion suggestion = new Suggestion(issue.getNumber(), fixSteps);
                suggestionStore.storeSuggestion(repo, suggestion);
                logger.info("Stored remediation suggestion for issue #{}", issue.getNumber());
            }
        }
    }
}