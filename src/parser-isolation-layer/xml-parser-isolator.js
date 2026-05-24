const detectXmlParser = require('./xml-parser-detector');

async function isolateXmlParser() {
  try {
    const isParserRunning = await detectXmlParser();
    if (isParserRunning) {
      console.error('XML parser is already running. Isolation failed.');
      process.exit(1);
    }
    // Proceed with XML parsing logic here
    console.log('XML parser is isolated and ready to run.');
  } catch (error) {
    console.error('Failed to detect XML parser:', error);
    process.exit(1);
  }
}

isolateXmlParser();