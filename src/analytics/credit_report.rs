use std::collections::HashMap;
use std::fs::File;
use std::io::{BufWriter, Write};
use chrono::{DateTime, Utc, NaiveDate};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreditReport {
    pub entries: Vec<MonthlyUsage>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MonthlyUsage {
    pub month: String,
    pub total_consumed: u64,
    pub remaining: u64,
}

impl CreditReport {
    /// Create a new empty credit report
    pub fn new() -> Self {
        CreditReport { entries: vec![] }
    }

    /// Generate a credit report from raw data
    /// In production, this would query a database instead of using simulated data
    pub fn generate_report(start_date: Option<NaiveDate>, end_date: Option<NaiveDate>) -> Self {
        // Simulated data source - would be replaced with actual DB query
        let raw_data = vec![
            ("2024-01-15".parse().unwrap(), 150, 850),
            ("2024-01-20".parse().unwrap(), 200, 800),
            ("2024-02-05".parse().unwrap(), 300, 700),
            ("2024-02-10".parse().unwrap(), 250, 650),
            ("2024-03-01".parse().unwrap(), 400, 600),
        ];

        let mut monthly_map: HashMap<String, (u64, u64)> = HashMap::new();

        for (date, consumed, remaining) in raw_data {
            // Filter by date range if provided
            if let (Some(start), Some(end)) = (&start_date, &end_date) {
                if date < *start || date > *end {
                    continue;
                }
            }

            let month_key = format!("{:04}-{:02}", date.year(), date.month());
            
            let entry = monthly_map.entry(month_key).or_insert((0, 0));
            entry.0 += consumed;
            entry.1 += remaining;
        }

        let entries: Vec<MonthlyUsage> = monthly_map
            .into_iter()
            .map(|(month, (total, remaining))| MonthlyUsage {
                month,
                total_consumed: total,
                remaining,
            })
            .collect();

        CreditReport { entries }
    }

    /// Generate a formatted report string
    pub fn generate_report_string(&self) -> String {
        let mut report = String::new();
        report.push_str("Credit Usage Report\n");
        report.push_str("==================\n");
        report.push_str("Month, Total Consumed, Remaining\n");
        report.push_str("--------------------------------\n");
        
        for entry in &self.entries {
            report.push_str(&format!(
                "{}, {}, {}\n",
                entry.month, 
                entry.total_consumed, 
                entry.remaining
            ));
        }
        report
    }

    /// Save report to CSV file
    pub fn save_to_csv(&self, filename: &str) -> std::io::Result<()> {
        let file = File::create(filename)?;
        let mut writer = BufWriter::new(file);
        
        // Write header
        writer.write_all("month,total_consumed,remaining\n".as_bytes())?;
        
        // Write data rows
        for entry in &self.entries {
            writer.write_all(
                &format!("{},{},{}\n", entry.month, entry.total_consumed, entry.remaining).as_bytes()
            )?;
        }
        
        Ok(())
    }

    /// Get total consumed across all months
    pub fn total_consumed(&self) -> u64 {
        self.entries.iter().map(|e| e.total_consumed).sum()
    }

    /// Get total remaining across all months
    pub fn total_remaining(&self) -> u64 {
        self.entries.iter().map(|e| e.remaining).sum()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_report_generation() {
        let report = CreditReport::generate_report(None, None);
        assert_eq!(report.entries.len(), 3);
        assert_eq!(report.entries[0].total_consumed, 350); // Jan: 150 + 200
        assert_eq!(report.entries[1].total_consumed, 550); // Feb: 300 + 250
        assert_eq!(report.entries[2].total_consumed, 400); // Mar: 400
    }

    #[test]
    fn test_report_generation_with_dates() {
        let start = "2024-01-01".parse().unwrap();
        let end = "2024-01-31".parse().unwrap();
        let report = CreditReport::generate_report(Some(start), Some(end));
        assert_eq!(report.entries.len(), 1); // Only January data
        assert_eq!(report.entries[0].month, "2024-01");
    }

    #[test]
    fn test_csv_generation() {
        let report = CreditReport::generate_report(None, None);
        let csv_content = report.generate_report_string();
        assert!(csv_content.contains("Credit Usage Report"));
        assert!(csv_content.contains("Month, Total Consumed, Remaining"));
    }

    #[test]
    fn test_total_calculations() {
        let report = CreditReport::generate_report(None, None);
        assert_eq!(report.total_consumed(), 1300); // 350 + 550 + 400
        assert_eq!(report.total_remaining(), 2100); // 850 + 800 + 700 + 650 + 600
    }
}