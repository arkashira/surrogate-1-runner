from security_scan import SecurityScanner

class DashboardIntegration:
    def __init__(self):
        self.security_scanner = SecurityScanner()

    def integrate_security_scan(self):
        scan_results = self.security_scanner.run_security_scan()
        self._display_scan_results(scan_results)

    def _display_scan_results(self, scan_results):
        print("Security Scan Results:")
        print("EC2 Instances:")
        for instance in scan_results['EC2Instances']:
            print(f"Instance ID: {instance['InstanceId']}")
            print("Vulnerabilities:")
            for vulnerability in instance['Vulnerabilities']:
                print(f"- {vulnerability}")
            print()

        print("S3 Buckets:")
        for bucket in scan_results['S3Buckets']:
            print(f"Bucket Name: {bucket['BucketName']}")
            print("Vulnerabilities:")
            for vulnerability in bucket['Vulnerabilities']:
                print(f"- {vulnerability}")
            print()