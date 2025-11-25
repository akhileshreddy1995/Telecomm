#!/usr/bin/env python3
"""
IMS SMS Checker - Automated SMS over IMS Network Monitor
Monitors and validates SMS messages transmitted over IP Multimedia Subsystem
"""

import socket
import re
from datetime import datetime
from typing import Dict, List, Optional
import json

class IMSSMSChecker:
    def __init__(self, ims_server: str = "localhost", port: int = 5060):
        """
        Initialize IMS SMS Checker
        
        Args:
            ims_server: IMS server address
            port: SIP port (default 5060 for IMS)
        """
        self.ims_server = ims_server
        self.port = port
        self.messages: List[Dict] = []
        
    def parse_sip_message(self, data: str) -> Optional[Dict]:
        """Parse SIP message containing SMS data"""
        try:
            lines = data.split('\r\n')
            message_info = {
                'timestamp': datetime.now().isoformat(),
                'method': '',
                'from': '',
                'to': '',
                'content': '',
                'content_type': '',
                'status': 'unknown'
            }
            
            # Parse request line
            if lines:
                request_line = lines[0]
                if 'MESSAGE' in request_line:
                    message_info['method'] = 'MESSAGE'
                    message_info['status'] = 'valid'
            
            # Parse headers
            content_start = False
            content_lines = []
            
            for line in lines[1:]:
                if line.startswith('From:'):
                    message_info['from'] = line.split(':', 1)[1].strip()
                elif line.startswith('To:'):
                    message_info['to'] = line.split(':', 1)[1].strip()
                elif line.startswith('Content-Type:'):
                    message_info['content_type'] = line.split(':', 1)[1].strip()
                elif line == '':
                    content_start = True
                elif content_start:
                    content_lines.append(line)
            
            message_info['content'] = '\r\n'.join(content_lines)
            
            return message_info
            
        except Exception as e:
            return None
    
    def check_sms_format(self, message: Dict) -> Dict:
        """Validate SMS message format and content"""
        checks = {
            'has_sender': bool(message.get('from')),
            'has_recipient': bool(message.get('to')),
            'has_content': bool(message.get('content')),
            'is_sip_message': message.get('method') == 'MESSAGE',
            'content_type_valid': 'text/plain' in message.get('content_type', '').lower() or 
                                 'application/vnd.3gpp.sms' in message.get('content_type', '').lower()
        }
        
        checks['all_valid'] = all(checks.values())
        return checks
    
    def simulate_ims_sms_check(self) -> List[Dict]:
        """Simulate checking SMS messages over IMS"""
        # Simulated IMS SMS messages for demonstration
        sample_messages = [
            """MESSAGE sip:+1234567890@ims.network.com SIP/2.0
Via: SIP/2.0/UDP client.ims.network.com:5060
From: <sip:+0987654321@ims.network.com>
To: <sip:+1234567890@ims.network.com>
Call-ID: abc123def456@ims.network.com
CSeq: 1 MESSAGE
Content-Type: text/plain; charset=UTF-8
Content-Length: 23

Hello, this is a test!""",
            """MESSAGE sip:+1111111111@ims.network.com SIP/2.0
Via: SIP/2.0/UDP client.ims.network.com:5060
From: <sip:+2222222222@ims.network.com>
To: <sip:+1111111111@ims.network.com>
Call-ID: xyz789ghi012@ims.network.com
CSeq: 2 MESSAGE
Content-Type: application/vnd.3gpp.sms
Content-Length: 34

Meeting scheduled for 3 PM today"""
        ]
        
        results = []
        for i, msg_data in enumerate(sample_messages, 1):
            print(f"\n{'='*60}")
            print(f"Checking SMS Message #{i}")
            print(f"{'='*60}")
            
            parsed = self.parse_sip_message(msg_data)
            if parsed:
                validation = self.check_sms_format(parsed)
                parsed['validation'] = validation
                
                print(f"From: {parsed['from']}")
                print(f"To: {parsed['to']}")
                print(f"Content Type: {parsed['content_type']}")
                print(f"Message: {parsed['content']}")
                print(f"\nValidation Results:")
                print(f"  - Has Sender: {'✓' if validation['has_sender'] else '✗'}")
                print(f"  - Has Recipient: {'✓' if validation['has_recipient'] else '✗'}")
                print(f"  - Has Content: {'✓' if validation['has_content'] else '✗'}")
                print(f"  - Is SIP MESSAGE: {'✓' if validation['is_sip_message'] else '✗'}")
                print(f"  - Valid Content Type: {'✓' if validation['content_type_valid'] else '✗'}")
                print(f"  - Overall Status: {'PASS ✓' if validation['all_valid'] else 'FAIL ✗'}")
                
                results.append(parsed)
                self.messages.append(parsed)
        
        return results
    
    def generate_report(self) -> str:
        """Generate summary report of checked messages"""
        if not self.messages:
            return "No messages to report"
        
        total = len(self.messages)
        valid = sum(1 for m in self.messages if m['validation']['all_valid'])
        
        report = f"\n{'='*60}\n"
        report += f"IMS SMS CHECK SUMMARY REPORT\n"
        report += f"{'='*60}\n"
        report += f"Total Messages Checked: {total}\n"
        report += f"Valid Messages: {valid}\n"
        report += f"Invalid Messages: {total - valid}\n"
        report += f"Success Rate: {(valid/total*100):.1f}%\n"
        report += f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"{'='*60}\n"
        
        return report
    
    def export_to_json(self, filename: str = "ims_sms_check.json"):
        """Export results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.messages, f, indent=2)
        print(f"\n✓ Results exported to {filename}")


def main():
    """Main function to run IMS SMS checker"""
    print("IMS SMS Checker - Automated SMS Validation Tool")
    print("=" * 60)
    
    # Initialize checker
    checker = IMSSMSChecker(ims_server="ims.network.com", port=5060)
    
    # Run checks
    print("\nStarting automated SMS checks over IMS...\n")
    results = checker.simulate_ims_sms_check()
    
    # Generate report
    report = checker.generate_report()
    print(report)
    
    # Export results
    checker.export_to_json()
    
    print("\n✓ SMS check automation completed successfully!")


if __name__ == "__main__":
    main()