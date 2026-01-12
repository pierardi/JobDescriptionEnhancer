#!/usr/bin/env python3
"""
Quick Demo - TechScreen Interview Generator
Shows how the system works without requiring Claude API key (uses mock mode)
"""

import sys
import json
from datetime import datetime

print("=" * 80)
print("TechScreen Interview Generator - DEMO MODE")
print("=" * 80)
print()
print("This demo shows you what the system does WITHOUT calling the Claude API")
print("(No API key needed for this demo)")
print()

# Try to import the necessary modules
try:
    from flask import Flask
    from models import db, JobDescription, Interview, InterviewQuestion
    from jd_enhancement_service import JDEnhancementService
    from interview_generation_service import InterviewGenerationService
    from claude_client import MockClaudeClient
    from config import TestingConfig
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print()
    print("Please run setup first:")
    print("  ./setup.sh")
    print("  or")
    print("  source venv/bin/activate && pip install -r requirements.txt")
    sys.exit(1)

print()

# Create Flask app with testing config
print("Creating Flask app with in-memory database...")
app = Flask(__name__)
app.config.from_object(TestingConfig)
db.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ In-memory database created")
    print()
    
    # Create mock Claude client
    print("=" * 80)
    print("STEP 1: Enhance Job Description")
    print("=" * 80)
    print()
    
    mock_client = MockClaudeClient()
    jd_service = JDEnhancementService(mock_client)
    
    # Sample job description
    print("📝 Original Job Description:")
    print("-" * 80)
    basic_jd = """
Title: Senior Backend Engineer

We are looking for a senior backend engineer with 7+ years of experience 
building scalable systems. You'll work with microservices, databases, and 
cloud platforms to deliver high-quality solutions.
"""
    print(basic_jd)
    print()
    
    print("📝 WORK Methodology Inputs:")
    print("-" * 80)
    work_inputs = {
        "work_output": "Design and build microservices that handle 10,000+ transactions per second with 99.99% uptime",
        "work_role": "Lead backend architecture, mentor 3-5 junior engineers, own service reliability",
        "work_knowledge": "Spring Boot, Kafka, PostgreSQL, Redis, Docker, Kubernetes, distributed systems",
        "work_competencies": "System design at scale, production debugging, technical mentorship, architectural trade-offs"
    }
    
    for key, value in work_inputs.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    print()
    
    print("🤖 Calling JD Enhancement Service (with mock Claude)...")
    result = jd_service.enhance_jd(
        req_id='DEMO-001',
        basic_title='Senior Backend Engineer',
        basic_description=basic_jd.strip(),
        user_id='demo-user',
        **work_inputs
    )
    
    if result['success']:
        print("✅ JD Enhancement completed!")
        print()
        print("📊 Result:")
        print("-" * 80)
        print(f"  Job Description ID: {result['job_description_id']}")
        print(f"  Requisition ID: {result['req_id']}")
        print(f"  Tokens Used: {result['tokens_used']} (mock)")
        print()
        print("  Enhanced Description:")
        print(f"  {result['enhanced_jd']['description'][:200]}...")
    else:
        print(f"❌ Enhancement failed: {result.get('error')}")
        sys.exit(1)
    
    print()
    print()
    
    # Interview Generation
    print("=" * 80)
    print("STEP 2: Generate Interview Questions")
    print("=" * 80)
    print()
    
    # Create a better mock client for interview generation
    class DemoInterviewMockClient(MockClaudeClient):
        def parse_interview_response(self, response_text):
            """Return sample interview questions"""
            return [
                {
                    'question_number': i + 1,
                    'question_text': f"[Demo Question {i+1}] Design a high-throughput system to process financial transactions with real-time fraud detection. How would you architect this?",
                    'expected_answer': f'High-Performance System Design',
                    'criteria': [
                        {
                            'criterion': 'Microservices Architecture',
                            'description': 'Demonstrates understanding of how to separate concerns into distinct, independently scalable services.'
                        },
                        {
                            'criterion': 'Message Queue Integration',
                            'description': 'Shows knowledge of using Kafka or similar systems to buffer traffic and ensure reliability.'
                        },
                        {
                            'criterion': 'Database Strategy',
                            'description': 'Explains approach to balancing transactional consistency with high-speed reads.'
                        },
                        {
                            'criterion': 'Caching Strategy',
                            'description': 'Describes how to use Redis or similar for frequently accessed data.'
                        },
                        {
                            'criterion': 'Load Balancing',
                            'description': 'Explains strategies for distributing traffic across services.'
                        },
                        {
                            'criterion': 'Error Handling',
                            'description': 'Demonstrates thought about failure scenarios and recovery mechanisms.'
                        },
                        {
                            'criterion': 'Monitoring & Alerting',
                            'description': 'Shows awareness of observability requirements for production systems.'
                        },
                        {
                            'criterion': 'Scalability Planning',
                            'description': 'Explains how the system would scale from 1k to 100k transactions per second.'
                        }
                    ]
                }
                for i in range(5)
            ]
    
    interview_service = InterviewGenerationService(DemoInterviewMockClient())
    
    print("🤖 Calling Interview Generation Service (with mock Claude)...")
    interview_result = interview_service.generate_interview(
        req_id='DEMO-001',
        job_description_id=result['job_description_id'],
        user_id='demo-user',
        interview_name='Senior Backend Engineer Interview - Demo'
    )
    
    if interview_result['success']:
        print("✅ Interview Generation completed!")
        print()
        print("📊 Result:")
        print("-" * 80)
        print(f"  Interview ID: {interview_result['interview_id']}")
        print(f"  Total Questions: {len(interview_result['interview']['questions'])}")
        print(f"  Tokens Used: {interview_result['tokens_used']} (mock)")
        print()
        
        # Display first question in detail
        question = interview_result['interview']['questions'][0]
        print(f"  📋 Sample Question (Question 1):")
        print(f"     {question['question_text']}")
        print()
        print(f"     Evaluation Criteria ({len(question['criteria'])} total):")
        for i, criterion in enumerate(question['criteria'][:3], 1):
            print(f"       {i}. {criterion['criterion']}")
            print(f"          {criterion['description']}")
        print(f"       ... and {len(question['criteria']) - 3} more criteria")
    else:
        print(f"❌ Interview generation failed: {interview_result.get('error')}")
        sys.exit(1)
    
    print()
    print()
    
    # Show database contents
    print("=" * 80)
    print("STEP 3: Database Records Created")
    print("=" * 80)
    print()
    
    jd_count = JobDescription.query.count()
    interview_count = Interview.query.count()
    question_count = InterviewQuestion.query.count()
    
    print(f"📊 Database Statistics:")
    print(f"  • Job Descriptions: {jd_count}")
    print(f"  • Interviews: {interview_count}")
    print(f"  • Interview Questions: {question_count}")
    print()
    
    # Show sample data
    jd = JobDescription.query.first()
    if jd:
        print(f"📝 Job Description Record:")
        print(f"  • ID: {jd.id}")
        print(f"  • Req ID: {jd.req_id}")
        print(f"  • Title: {jd.basic_title}")
        print(f"  • Has WORK inputs: {bool(jd.work_output)}")
        print(f"  • Enhanced: {bool(jd.enhanced_description)}")
    
    print()
    
    interview = Interview.query.first()
    if interview:
        print(f"📋 Interview Record:")
        print(f"  • ID: {interview.id}")
        print(f"  • Name: {interview.interview_name}")
        print(f"  • Questions: {len(interview.questions)}")
        print(f"  • Status: {interview.status}")
    
    print()
    print()

print("=" * 80)
print("✅ DEMO COMPLETE!")
print("=" * 80)
print()
print("What you just saw:")
print()
print("1. ✅ Enhanced a job description using WORK methodology")
print("   - Used work_output, work_role, work_knowledge, work_competencies")
print("   - Claude would make it more specific and deliverable-focused")
print()
print("2. ✅ Generated a 5-question technical interview")
print("   - Each question has 8-10 evaluation criteria")
print("   - Questions test actual job requirements")
print()
print("3. ✅ Stored everything in a database")
print("   - Job descriptions with WORK inputs")
print("   - Interviews with questions and criteria")
print()
print("Next Steps:")
print()
print("1. To run with REAL Claude API:")
print("   • Get API key from: https://console.anthropic.com/")
print("   • Add to .env file: CLAUDE_API_KEY=your-key")
print("   • Run: python app.py")
print("   • Test: python test_client.py")
print()
print("2. To explore the code:")
print("   • Read: QUICK_START.md")
print("   • Review: README.md")
print("   • Understand WORK: WORK_METHODOLOGY_GUIDE.md")
print()
print("3. To integrate into your app:")
print("   • Follow: INTEGRATION_GUIDE_FOR_PETER.md")
print()
print("=" * 80)
