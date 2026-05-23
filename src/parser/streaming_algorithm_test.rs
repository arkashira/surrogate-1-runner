#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use std::fs::File;

    #[test]
    fn test_streaming_parser() {
        let mut file = File::create("test.txt").unwrap();
        file.write_all(b"Hello\nWorld\nThis\nIs\nA\nTest").unwrap();
        let mut parser = StreamingParser::new("test.txt");
        let result = parser.parse();
        assert_eq!(result, vec!["Hello", "World", "This", "Is", "A", "Test"]);
    }

    #[test]
    fn test_streaming_parser_large_file() {
        let mut file = File::create("large_test.txt").unwrap();
        for _ in 0..10000 {
            file.write_all(b"Hello\nWorld\nThis\nIs\nA\nTest").unwrap();
        }
        let mut parser = StreamingParser::new("large_test.txt");
        let result = parser.parse();
        assert_eq!(result.len(), 60000);
    }
}