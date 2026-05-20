#!/usr/bin/env bash
# /opt/axentx/surrogate-1/cli/src/testConnectivity.sh
set -euo pipefail

# Function to validate YAML syntax
validate_yaml() {
    local yaml_file="$1"
    if ! command -v yamllint &> /dev/null; then
        echo "yamllint not found, skipping YAML validation"
        return 0
    fi
    
    if ! yamllint "$yaml_file"; then
        echo "❌ YAML validation failed for $yaml_file"
        return 1
    else
        echo "✅ YAML validation passed for $yaml_file"
        return 0
    fi
}

# Function to check service connectivity
check_connectivity() {
    local service_name="$1"
    local port="$2"
    
    # Try to connect to the service using curl
    if timeout 5 bash -c "curl -f -s --connect-timeout 5 http://$service_name:$port >/dev/null"; then
        echo "✅ Service $service_name is reachable on port $port"
        return 0
    else
        echo "❌ Service $service_name is not reachable on port $port"
        return 1
    fi
}

# Main execution logic
main() {
    echo "Starting connectivity tests..."
    
    # Validate all YAML files in the current directory
    for yaml_file in *.yaml *.yml; do
        if [[ -f "$yaml_file" ]]; then
            validate_yaml "$yaml_file" || exit 1
        fi
    done
    
    # Check connectivity for common services
    # Add more services as needed based on your deployment
    check_connectivity "kubernetes.default.svc" "443" || echo "Warning: Could not verify kubernetes API connectivity"
    check_connectivity "localhost" "8080" || echo "Warning: Could not verify localhost service"
    
    echo "Connectivity tests completed."
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi