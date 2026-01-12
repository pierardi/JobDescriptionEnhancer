# WORK Methodology Guide

## What is WORK?

WORK is a framework for clearly articulating what a role actually requires:

- **W**ork Output - What will this person build/deliver?
- **O**utcome/Role - What are the key responsibilities?
- **R**equired Knowledge - What knowledge areas are critical?
- **K**ey Competencies - What competencies are essential?

By filling out the WORK form, you guide Claude to create much better, more targeted job descriptions and interview questions.

---

## Why Fill Out WORK?

**Without WORK inputs:**
```
Basic JD: "We need a software engineer"
Claude thinks: "Hmm, what kind of engineer? What do they do?"
Result: Generic enhancement based on assumptions
```

**With WORK inputs:**
```
Basic JD: "We need a software engineer"
WORK inputs: "Build real-time trading systems... handle 10k transactions/sec... Kafka, PostgreSQL... system design"
Claude thinks: "Ah! High-performance, distributed systems specialist"
Result: Precise, competency-focused enhancement
```

---

## How to Fill Out Each WORK Field

### 1. Work Output (What will they build/deliver?)

**Purpose:** Specify the actual systems, features, or products they'll create

**Examples:**

```
❌ Too vague:
"Build software systems"

✅ Good:
"Design and build microservices that process 10,000 banking transactions 
per second with real-time fraud detection and high availability"

❌ Too vague:
"Frontend development"

✅ Good:
"Build responsive, accessible React dashboards that handle real-time 
data updates with complex state management for 100k+ concurrent users"

❌ Too vague:
"Infrastructure work"

✅ Good:
"Design and maintain Kubernetes clusters that auto-scale across 
multiple cloud regions, handling petabyte-scale data workloads"
```

**Tips:**
- Be specific about scale (10k/sec, 100k users, petabytes)
- Include key non-functional requirements (real-time, high-availability, etc.)
- Mention critical features or characteristics
- 2-3 sentences is ideal

---

### 2. Work Role (What are the key responsibilities?)

**Purpose:** Describe what they actually do day-to-day and their scope of influence

**Examples:**

```
❌ Too generic:
"Develop features"

✅ Good:
"Lead backend microservices architecture, make critical design decisions, 
mentor junior engineers, own service reliability and performance, 
interface with product team on technical trade-offs"

❌ Too generic:
"Write code"

✅ Good:
"Architect distributed system solutions, conduct technical interviews, 
lead design reviews, own end-to-end feature delivery from database 
schema to API design to frontend integration"

❌ Too generic:
"Manage infrastructure"

✅ Good:
"Design infrastructure-as-code, manage disaster recovery procedures, 
lead on-call rotations, optimize system costs, mentor ops engineers, 
evaluate new tools and platforms"
```

**Tips:**
- Include leadership/mentorship aspects if relevant
- Specify decision-making authority
- Mention cross-team interactions
- Include ownership and accountability elements
- 2-3 sentences is ideal

---

### 3. Work Knowledge (What knowledge areas are critical?)

**Purpose:** List the specific technologies, concepts, and frameworks they MUST know

**Examples:**

```
❌ Too broad:
"Java, databases, APIs"

✅ Good:
"Spring Boot, Kafka/RabbitMQ, PostgreSQL (ACID, EXPLAIN ANALYZE), 
Redis caching, REST API design, Docker, distributed transaction patterns, 
load balancing strategies"

❌ Too broad:
"Frontend technologies"

✅ Good:
"React (hooks, context, performance optimization), Redux/state management, 
TypeScript, responsive design, accessibility (WCAG), testing frameworks 
(Jest, React Testing Library), performance profiling"

❌ Too broad:
"Cloud and DevOps"

✅ Good:
"Kubernetes (deployments, services, operators), Terraform/IaC, AWS 
(EC2, RDS, S3, Lambda), monitoring (Prometheus, DataDog), CI/CD 
(Jenkins/GitLab CI), security scanning, cost optimization"
```

**Tips:**
- List specific technologies, NOT generic categories
- Include deeper knowledge areas (e.g., "PostgreSQL" is better than "SQL")
- Mix foundational and specialized knowledge
- 10-15 technologies/concepts is good
- Comma-separated list is fine

---

### 4. Work Competencies (What competencies are essential?)

**Purpose:** Describe the professional abilities and soft skills they need

**Examples:**

```
❌ Too vague:
"Communication, problem solving"

✅ Good:
"System design at scale, deep troubleshooting of production issues, 
architectural decision-making, clear technical communication (docs, design docs, 
presentations), mentorship and knowledge sharing, balancing technical 
perfection with shipping velocity"

❌ Too vague:
"Collaboration, attention to detail"

✅ Good:
"Full-stack thinking (understanding tradeoffs across the stack), 
attention to UX details, ability to work with designers and product managers, 
mentoring junior designers, balancing accessibility with aesthetics, 
keeping up with design trends and tooling"

❌ Too vague:
"Leadership, planning"

✅ Good:
"Incident management and on-call leadership, capacity planning for 
scale, security mindset, cost optimization thinking, ability to take 
ownership of large projects, strategic technical roadmap development, 
cross-team alignment"
```

**Tips:**
- Mix hard skills (technical depth) with soft skills (communication)
- Include mindset/approach elements (e.g., "ownership", "pragmatic")
- Be specific about what "good communication" looks like in this role
- Think about what separates a good person from a great person in this role
- 5-7 competencies is good

---

## Real-World Example

### Scenario: Hiring a Senior Backend Engineer

**Basic JD:**
```
Senior Backend Engineer - We're looking for a senior backend engineer 
with experience in building scalable systems. You'll work with a team 
to develop APIs and services. Required: 7+ years experience, Java/Spring, SQL.
```

**WORK Form Filled Out:**

```
Work Output:
"Design and build microservices that handle 10,000+ banking transactions 
per second with zero-downtime deployments, real-time fraud detection, and 
99.99% uptime SLA. Architect systems that support scaling from 1 million 
to 100 million transactions per day."

Work Role:
"Lead backend architecture decisions and make strategic technology choices. 
Mentor a team of 3-5 junior/mid-level engineers. Own service reliability 
and performance. Collaborate with platform, data, and security teams on 
complex technical requirements. Conduct technical interviews for hiring."

Work Knowledge:
"Spring Boot, Java streams/concurrency, PostgreSQL (ACID properties, 
query optimization), Kafka message streaming, Redis caching, REST API 
design patterns, gRPC, Docker/Kubernetes, distributed transaction patterns 
(Saga), event sourcing, load testing and profiling, AWS (ECS, RDS, 
Lambda), monitoring and alerting"

Work Competencies:
"System design at scale (millions of requests/sec), deep production 
debugging and incident response, making architectural trade-offs 
(consistency vs availability), technical mentorship and code review, 
clear technical communication (design docs, presentations), pragmatic 
approach to technical debt, security mindset, understanding of regulatory 
requirements (financial services)"
```

**Result:**
Claude now creates an enhanced JD that specifically mentions:
- Banking transaction processing at scale
- Microservices architecture
- Specific technologies (Spring Boot, Kafka, PostgreSQL)
- Leadership and mentorship expectations
- Performance and reliability requirements

**And generates interview questions that directly test:**
- Can they design a high-volume transaction system?
- How do they handle distributed transactions?
- Do they understand Kafka as a message queue?
- Can they mentor other engineers?
- How do they approach production incidents?

---

## Tips for Writing Good WORK Inputs

### 1. Be Specific, Not Generic
```
❌ "Experience with cloud platforms"
✅ "Experience with AWS (EC2, RDS, S3, CloudFront, Lambda, IAM), 
   and proven ability to architect multi-region deployments"
```

### 2. Include Scale/Volume
```
❌ "Build systems"
✅ "Build systems that handle 100k concurrent users and 1 million 
   events per second"
```

### 3. Mention Real Constraints
```
❌ "Good performance"
✅ "Sub-100ms response times at p95 latency, optimized for 
   sub-100MB/s bandwidth usage"
```

### 4. Link to Business Value
```
❌ "Handle transactions"
✅ "Process payment transactions with zero-tolerance fraud detection 
   and regulatory compliance requirements"
```

### 5. Include Mindset/Approach
```
❌ "Attention to detail"
✅ "Obsessive attention to edge cases and error handling, 
   'fail safe' design philosophy"
```

---

## Common Mistakes

### ❌ Mistake 1: Writing the WORK section like a resume
```
"Led team of 5 engineers, shipped features, improved performance by 20%"
→ This describes what you want to hear about interviews
→ Not what the role itself demands
```

### ❌ Mistake 2: Being too vague
```
"Full-stack engineer with good communication"
→ Every job posting says this
→ Won't help Claude create targeted enhancements
```

### ❌ Mistake 3: Confusing nice-to-have with essential
```
"Knowledge of Rust, Go, and Python"
→ If they only NEED Rust and could learn the rest,
→ Don't list Go and Python as required knowledge
```

### ❌ Mistake 4: Copy-pasting from job boards
```
"10+ years experience, strategic thinking, passionate about clean code"
→ These are generic
→ Focus on what THIS role specifically needs
```

---

## How to Gather WORK Information

### From Hiring Manager
1. "What will this person build that we're currently not building?"
2. "What are the hardest technical problems this person will solve?"
3. "What should they know very deeply vs just understand?"
4. "What will separate a good engineer from a great engineer in this role?"
5. "What decisions will they make independently?"

### From Team
1. Ask the team they'll be joining what they wish they had in a new team member
2. Ask about the toughest technical challenges the team faces
3. Ask about growth areas they'd love support in

### From Past Success
1. What characteristics did your most successful hires in this role have?
2. What do your best engineers in similar roles know?
3. What technical depth is most valued?

---

## Using WORK with the API

### Workflow 1: JD Enhancement Only
```bash
POST /api/interview/jd/enhance
{
  "req_id": "REQ-12345",
  "basic_title": "Senior Backend Engineer",
  "basic_description": "...",
  "work_output": "...",
  "work_role": "...",
  "work_knowledge": "...",
  "work_competencies": "..."
}
```

### Workflow 2: Complete (Enhancement + Interview)
```bash
POST /api/interview/workflow/full
{
  "req_id": "REQ-12345",
  "basic_title": "Senior Backend Engineer",
  "basic_description": "...",
  "work_output": "...",
  "work_role": "...",
  "work_knowledge": "...",
  "work_competencies": "...",
  "interview_name": "..."
}
```

---

## Testing Your WORK Inputs

### Good Sign ✅
- The enhanced JD reads like it's specifically for this role
- The interview questions directly test the WORK requirements
- Someone reading it immediately understands what the person will do

### Bad Sign ❌
- The enhanced JD could apply to 10 different roles
- The interview questions seem generic
- You read it and think "that could be any engineer"

---

## Next Steps

1. **Start with one role** - Don't try to perfect all roles at once
2. **Fill out WORK from scratch** - Don't copy from old job postings
3. **Ask your team** - Get their input on what's essential
4. **Test the output** - See if the enhanced JD matches your vision
5. **Refine** - Adjust WORK inputs if the enhancement isn't quite right

---

Remember: **The effort you put into the WORK form directly impacts the quality of the enhanced JD and interview questions.** Better WORK inputs = better hiring.
