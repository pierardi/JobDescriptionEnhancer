"""
Test Client for Interview Generation API

This script provides a simple way to test the API endpoints without curl or Postman.
Run this after starting the Flask app to validate everything is working.

Usage:
    python test_client.py [environment]

    environment: development (default), testing, production
"""

import requests
import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
ADMIN_USER_ID = 'test-admin-user-123'
ADMIN_ROLE = 'admin'

# Headers
ADMIN_HEADERS = {
    'X-User-ID': ADMIN_USER_ID,
    'X-User-Role': ADMIN_ROLE,
    'Content-Type': 'application/json'
}

USER_HEADERS = {
    'X-User-ID': 'test-user-456',
    'X-User-Role': 'user',
    'Content-Type': 'application/json'
}


class APITestClient:
    """Simple API test client for endpoint testing."""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def print_response(self, method, url, status_code, response):
        """Pretty print API response."""
        print(f"\n{'='*80}")
        print(f"REQUEST: {method} {url}")
        print(f"STATUS: {status_code}")
        print(f"RESPONSE:")
        try:
            if response:
                print(json.dumps(response, indent=2))
            else:
                print("(empty response)")
        except:
            print(response)
        print(f"{'='*80}\n")
    
    def health_check(self):
        """Test health endpoint."""
        print("\n[TEST 1] Health Check")
        try:
            response = requests.get(f"{self.base_url}/health")
            self.print_response('GET', f"{self.base_url}/health", response.status_code, response.json())
            return response.status_code == 200
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    def enhance_jd(self, req_id, title, description, work_output=None, work_role=None, work_knowledge=None, work_competencies=None):
        """Test JD enhancement endpoint with optional WORK inputs."""
        print(f"\n[TEST 2] Enhance Job Description (req_id: {req_id})")
        
        payload = {
            'req_id': req_id,
            'basic_title': title,
            'basic_description': description,
            'basic_department': 'Engineering',
            'basic_level': 'Senior'
        }
        
        # Add WORK inputs if provided
        if work_output:
            payload['work_output'] = work_output
        if work_role:
            payload['work_role'] = work_role
        if work_knowledge:
            payload['work_knowledge'] = work_knowledge
        if work_competencies:
            payload['work_competencies'] = work_competencies
        
        try:
            response = requests.post(
                f"{self.base_url}/api/interview/jd/enhance",
                json=payload,
                headers=ADMIN_HEADERS
            )
            self.print_response(
                'POST',
                f"{self.base_url}/api/interview/jd/enhance",
                response.status_code,
                response.json()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def get_jd(self, req_id):
        """Test get JD endpoint."""
        print(f"\n[TEST 3] Get Job Description (req_id: {req_id})")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/interview/jd/{req_id}",
                headers=USER_HEADERS
            )
            self.print_response(
                'GET',
                f"{self.base_url}/api/interview/jd/{req_id}",
                response.status_code,
                response.json()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def generate_interview(self, req_id, jd_id):
        """Test interview generation endpoint."""
        print(f"\n[TEST 4] Generate Interview (req_id: {req_id}, jd_id: {jd_id})")
        
        payload = {
            'req_id': req_id,
            'job_description_id': jd_id,
            'interview_name': f'Test Interview - {req_id}'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/interview/generate",
                json=payload,
                headers=ADMIN_HEADERS
            )
            self.print_response(
                'POST',
                f"{self.base_url}/api/interview/generate",
                response.status_code,
                response.json()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def get_interview(self, interview_id):
        """Test get interview endpoint."""
        print(f"\n[TEST 5] Get Interview (interview_id: {interview_id})")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/interview/{interview_id}",
                headers=USER_HEADERS
            )
            self.print_response(
                'GET',
                f"{self.base_url}/api/interview/{interview_id}",
                response.status_code,
                response.json()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def get_interviews_by_req(self, req_id):
        """Test get interviews by requisition."""
        print(f"\n[TEST 6] Get Interviews by Requisition (req_id: {req_id})")
        
        try:
            response = requests.get(
                f"{self.base_url}/api/interview/req/{req_id}",
                headers=USER_HEADERS
            )
            self.print_response(
                'GET',
                f"{self.base_url}/api/interview/req/{req_id}",
                response.status_code,
                response.json()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None
    
    def complete_workflow(self, req_id):
        """Test complete workflow (enhance JD + generate interview)."""
        print(f"\n[TEST 7] Complete Workflow - JD Enhancement + Interview Generation (req_id: {req_id})")
        
        payload = {
            'req_id': req_id,
            'basic_title': 'Full Stack Software Engineer',
            'basic_description': """We are looking for a full stack engineer with experience in microservices, 
React, and cloud platforms. The ideal candidate will have 5+ years of experience building scalable systems.""",
            'basic_department': 'Engineering',
            'basic_level': 'Senior',
            'work_output': 'Design and build full-stack microservices handling 5k concurrent users',
            'work_role': 'Lead full-stack architecture, mentor juniors, own feature delivery',
            'work_knowledge': 'React, Node.js/Spring Boot, PostgreSQL, Docker, Kubernetes, AWS',
            'work_competencies': 'Full-stack design, problem solving, communication, ownership',
            'interview_name': f'Full Stack Engineer Interview - {req_id}'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/interview/workflow/full",
                json=payload,
                headers=ADMIN_HEADERS
            )
            self.print_response(
                'POST',
                f"{self.base_url}/api/interview/workflow/full",
                response.status_code,
                response.json()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"ERROR: {e}")
            return None


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("INTERVIEW GENERATION API - TEST CLIENT")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    
    client = APITestClient()
    
    # Test 1: Health check
    print("\n[STEP 1/7] Testing health endpoint...")
    if not client.health_check():
        print("FATAL: Server is not responding. Make sure Flask app is running.")
        print(f"Start the app with: python app.py")
        return False
    
    # Test 2: Enhance JD with WORK inputs
    print("\n[STEP 2/7] Testing JD enhancement with WORK methodology inputs...")
    req_id = "TEST-REQ-001"
    jd_response = client.enhance_jd(
        req_id=req_id,
        title="Senior Software Engineer",
        description="""We are looking for a senior engineer with 7+ years of experience. 
The role involves designing microservices, leading architectural decisions, and mentoring junior engineers.""",
        work_output="Design and build microservices that process 10,000 transactions per second",
        work_role="Lead backend architecture, mentor junior engineers, own service reliability",
        work_knowledge="Kafka/RabbitMQ, PostgreSQL, Spring Boot, distributed systems, load balancing",
        work_competencies="System design, problem solving, communication, technical depth"
    )
    
    if not jd_response or not jd_response.get('success'):
        print("ERROR: JD enhancement failed")
        return False
    
    jd_id = jd_response['job_description_id']
    
    # Test 3: Get JD
    print("\n[STEP 3/7] Testing get JD...")
    get_jd_response = client.get_jd(req_id)
    if not get_jd_response or not get_jd_response.get('success'):
        print("ERROR: Get JD failed")
        return False
    
    # Test 4: Generate Interview
    print("\n[STEP 4/7] Testing interview generation...")
    interview_response = client.generate_interview(req_id, jd_id)
    
    if not interview_response or not interview_response.get('success'):
        print("ERROR: Interview generation failed")
        return False
    
    interview_id = interview_response['interview_id']
    
    # Test 5: Get Interview
    print("\n[STEP 5/7] Testing get interview...")
    get_interview_response = client.get_interview(interview_id)
    if not get_interview_response or not get_interview_response.get('success'):
        print("ERROR: Get interview failed")
        return False
    
    # Test 6: Get Interviews by Req
    print("\n[STEP 6/7] Testing get interviews by requisition...")
    interviews_response = client.get_interviews_by_req(req_id)
    if not interviews_response or not interviews_response.get('success'):
        print("ERROR: Get interviews by req failed")
        return False
    
    # Test 7: Complete Workflow
    print("\n[STEP 7/7] Testing complete workflow...")
    workflow_response = client.complete_workflow("TEST-WORKFLOW-001")
    if not workflow_response or not workflow_response.get('success'):
        print("ERROR: Complete workflow failed")
        return False
    
    # Summary
    print("\n" + "="*80)
    print("✓ ALL TESTS PASSED!")
    print("="*80)
    print("\nEndpoints are working correctly:")
    print("  ✓ Health check")
    print("  ✓ JD enhancement")
    print("  ✓ Get JD")
    print("  ✓ Interview generation")
    print("  ✓ Get interview")
    print("  ✓ Get interviews by requisition")
    print("  ✓ Complete workflow")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Check the database to verify data was created:")
    print("   mysql> SELECT * FROM job_descriptions;")
    print("   mysql> SELECT * FROM interviews;")
    print("   mysql> SELECT * FROM interview_questions;")
    print("\n2. Check generation logs:")
    print("   mysql> SELECT * FROM generation_logs;")
    print("\n3. Review the README.md for full API documentation")
    print("\n4. Integrate into your Flask application")
    print("\n5. Update authentication to use your auth system")
    
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
