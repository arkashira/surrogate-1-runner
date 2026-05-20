document.addEventListener('DOMContentLoaded', function() {
    const guideContent = `
        <h1>Content Marketing Guide</h1>
        <section>
            <h2>Introduction</h2>
            <p>Welcome to the Content Marketing Guide for micro-SaaS founders. This guide will help you effectively reach and engage your target audience through content marketing.</p>
        </section>
        <section>
            <h2>Getting Started</h2>
            <ol>
                <li><strong>Define Your Target Audience</strong>: Understand who your ideal customers are and what they need.</li>
                <li><strong>Set Clear Goals</strong>: Determine what you want to achieve with your content marketing efforts.</li>
            </ol>
        </section>
        <section>
            <h2>Content Creation</h2>
            <h3>Blog Posts</h3>
            <ul>
                <li><strong>Tips</strong>: Write about industry trends, how-to guides, and case studies.</li>
                <li><strong>Examples</strong>:
                    <ul>
                        <li>"10 Tips for Effective Content Marketing"</li>
                        <li>"Case Study: How Company X Increased Traffic by 200%"</li>
                    </ul>
                </li>
            </ul>
            <h3>Social Media</h3>
            <ul>
                <li><strong>Platforms</strong>: Focus on platforms where your audience is most active.</li>
                <li><strong>Examples</strong>:
                    <ul>
                        <li>Twitter: Share quick tips and industry news.</li>
                        <li>LinkedIn: Post long-form articles and thought leadership pieces.</li>
                    </ul>
                </li>
            </ul>
            <h3>Email Marketing</h3>
            <ul>
                <li><strong>Newsletters</strong>: Send regular newsletters with valuable content.</li>
                <li><strong>Examples</strong>:
                    <ul>
                        <li>Monthly digest of industry news.</li>
                        <li>Exclusive content for subscribers.</li>
                    </ul>
                </li>
            </ul>
        </section>
        <section>
            <h2>Integration with Onboarding Process</h2>
            <ol>
                <li><strong>Welcome Email</strong>: Include a link to your content marketing guide.</li>
                <li><strong>Onboarding Checklist</strong>: Add a step to review the content marketing guide.</li>
                <li><strong>Resource Center</strong>: Create a dedicated section in your app for content marketing resources.</li>
            </ol>
        </section>
        <section>
            <h2>Case Studies</h2>
            <ul>
                <li><strong>Example 1</strong>: How Company A increased engagement by 150% through consistent blogging.</li>
                <li><strong>Example 2</strong>: How Company B used social media to build a loyal community.</li>
            </ul>
        </section>
        <section>
            <h2>Conclusion</h2>
            <p>Content marketing is a powerful tool for reaching and engaging your target audience. By following this guide, you can create a comprehensive content marketing strategy that drives results.</p>
        </section>
    `;

    document.getElementById('content-marketing-guide').innerHTML = guideContent;
});