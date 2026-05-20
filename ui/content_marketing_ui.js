document.addEventListener('DOMContentLoaded', function() {
    const guideContent = document.getElementById('content-marketing-guide');
    const examplesSection = document.getElementById('examples-section');
    const caseStudiesSection = document.getElementById('case-studies-section');

    // Comprehensive and easy-to-follow content marketing guide
    guideContent.innerHTML = `
        <h1>Content Marketing Guide</h1>
        <p>Content marketing is a strategic approach focused on creating and distributing valuable, relevant, and consistent content to attract and retain a clearly defined audience.</p>
        <h2>Strategies</h2>
        <ol>
            <li>Define your target audience</li>
            <li>Create valuable content</li>
            <li>Promote your content through various channels</li>
            <li>Analyze and optimize your content performance</li>
        </ol>
    `;

    // Examples and case studies
    examplesSection.innerHTML = `
        <h2>Examples</h2>
        <ul>
            <li>Blog posts that educate your audience about industry trends.</li>
            <li>Infographics that simplify complex information.</li>
        </ul>
    `;
    
    caseStudiesSection.innerHTML = `
        <h2>Case Studies</h2>
        <ul>
            <li>Company X increased their website traffic by 50% using content marketing strategies.</li>
            <li>Company Y improved customer engagement by 30% through regular blog updates.</li>
            <li>Company A increased engagement by 200% through blogs.</li>
            <li>Company B's success with social media campaigns.</li>
        </ul>
    `;
});