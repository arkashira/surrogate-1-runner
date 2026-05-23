use std::io::{Read, BufReader};
use std::fs::File;

pub struct StreamingParser {
    buffer: Vec<u8>,
    reader: BufReader<File>,
}

impl StreamingParser {
    pub fn new(file_path: &str) -> Self {
        let file = File::open(file_path).unwrap();
        let reader = BufReader::new(file);
        StreamingParser {
            buffer: Vec::new(),
            reader,
        }
    }

    pub fn parse(&mut self) -> Vec<String> {
        let mut result = Vec::new();
        loop {
            let mut chunk = [0; 4096];
            let bytes_read = self.reader.read(&mut chunk).unwrap();
            if bytes_read == 0 {
                break;
            }
            self.buffer.extend_from_slice(&chunk[..bytes_read]);
            let parsed = self.parse_buffer();
            result.extend(parsed);
        }
        result
    }

    fn parse_buffer(&mut self) -> Vec<String> {
        let mut result = Vec::new();
        let mut i = 0;
        while i < self.buffer.len() {
            if self.buffer[i] == b'\n' {
                let line = String::from_utf8_lossy(&self.buffer[..i]);
                result.push(line.to_string());
                self.buffer = self.buffer[i + 1..].to_vec();
                i = 0;
            } else {
                i += 1;
            }
        }
        result
    }
}