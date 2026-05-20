pub fn display_routing_duration(duration: u64) {
    println!("Routing duration: {} ms", duration);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_display_routing_duration() {
        display_routing_duration(25);
    }
}