
const fs = require('fs');
const path = require('path');
const marked = require('marked');

function renderMarkdown(markdownContent) {
  return marked(markdownContent);
}

function writeDocs(docs, outputDir) {
  // Ensure output directory exists
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  docs.forEach((doc) => {
    const filePath = path.join(outputDir, `${path.basename(doc.filename, '.md')}.html`);
    fs.writeFileSync(filePath, doc.html);
  });
}

async function generateDocs(inputDir = './docs', outputDir = '/opt/axentx/surrogate-1/docs/workflows/') {
  // Check if input directory exists
  if (!fs.existsSync(inputDir)) {
    console.log(`Input directory ${inputDir} does not exist. Creating it.`);
    fs.mkdirSync(inputDir, { recursive: true });
    return;
  }
  
  const markdownFiles = fs.readdirSync(inputDir).filter(f => f.endsWith('.md'));
  const docs = [];

  for (const markdownFile of markdownFiles) {
    const markdownContent = fs.readFileSync(path.join(inputDir, markdownFile), 'utf8');
    const htmlContent = renderMarkdown(markdownContent);
    docs.push({ filename: markdownFile, html: htmlContent });  // Fixed syntax from Candidate 2
  }

  writeDocs(docs, outputDir);
  console.log(`Generated ${docs.length} documentation files to ${outputDir}`);
}

// Run if executed directly
if (require.main === module) {
  generateDocs();
}

module.exports = { generateDocs, renderMarkdown };