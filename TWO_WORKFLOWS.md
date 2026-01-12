# Two Workflows: Quick Reference Guide

## Overview

You now have TWO separate workflows:

1. **Workflow 1: JD Enhancement Only** - Enhance a job description using WORK methodology
2. **Workflow 2: Complete Workflow** - Enhance a JD AND generate an interview in one call

Choose based on what you need.

---

## Workflow 1: JD Enhancement Only

### When to Use
- You just want to enhance a job description
- You'll create the interview manually or separately
- You want to review and approve the enhanced JD before generating an interview
- You're building an internal job description that won't have interviews

### What Happens
```
Basic JD + WORK Inputs
        ↓
    [Claude]
        ↓
  Enhanced JD
        ↓
   Database
```

### Endpoint
```
POST /api/interview/jd/enhance
```

### Example Request
```json
{
  "req_id": "REQ-12345",
  "basic_title": "Senior Software Engineer",
  "basic_description": "We need a senior engineer...",
  "basic_department": "Engineering",
  "basic_level": "Senior",
  
  "work_output": "Design microservices processing 10k transactions/sec",
  "work_role": "Lead backend architect, mentor juniors",
  "work_knowledge": "Kafka, PostgreSQL, Spring Boot, distributed systems",
  "work_competencies": "System design, problem solving, technical depth"
}
```

### Response
```json
{
  "success": true,
  "job_description_id": 123,
  "enhanced_jd": {
    "title": "Senior Software Engineer",
    "description": "Enhanced description focused on deliverables..."
  },
  "work_inputs": { ... },
  "tokens_used": 1250
}
```

### Next Steps
- Review the enhanced JD
- Share with team
- Later: Use `job_description_id` to generate interview with Workflow 2 (Standalone Interview Generation)

---

## Workflow 2: Complete Workflow (Enhancement + Interview)

### When to Use
- You have a job description you want enhanced AND need an interview
- You want everything done in one call
- You're creating the full hiring package (enhanced JD + interview questions)
- You don't need to review/approve the JD separately

### What Happens
```
Basic JD + WORK Inputs
        ↓
   [Claude: Enhance]
        ↓
  Enhanced JD
        ↓
   [Claude: Generate]
        ↓
5-Question Interview
        ↓
    Database
```

### Endpoint
```
POST /api/interview/workflow/full
```

### Example Request
```json
{
  "req_id": "REQ-12345",
  "basic_title": "Senior Software Engineer",
  "basic_description": "We need a senior engineer...",
  "basic_department": "Engineering",
  "basic_level": "Senior",
  
  "work_output": "Design microservices processing 10k transactions/sec",
  "work_role": "Lead backend architect, mentor juniors",
  "work_knowledge": "Kafka, PostgreSQL, Spring Boot, distributed systems",
  "work_competencies": "System design, problem solving, technical depth",
  
  "interview_name": "Senior Engineer Interview - Q1 2025"
}
```

### Response
```json
{
  "success": true,
  "job_description_id": 123,
  "interview_id": 456,
  "interview": {
    "questions": [
      {
        "question_number": 1,
        "question_text": "Design a system to process...",
        "criteria": [...]
      },
      ...
    ]
  },
  "total_tokens_used": 3350
}
```

### Next Steps
- Review the generated interview
- Use with candidates
- Everything is stored in database

---

## Comparison Table

| Aspect | Workflow 1: JD Only | Workflow 2: Full |
|--------|-------------------|-----------------|
| **Purpose** | Enhance JD only | Enhance JD + Generate Interview |
| **Endpoint** | `/api/interview/jd/enhance` | `/api/interview/workflow/full` |
| **Time** | ~5-10 seconds | ~15-20 seconds |
| **Tokens Used** | ~1,200-1,500 | ~3,200-4,000 |
| **Output** | Enhanced JD | Enhanced JD + 5-question Interview |
| **Review Step** | Recommended | Optional |
| **Use When** | JD is the primary goal | Need both JD and interview |
| **API Calls** | 1 | 2 (sequential) |

---

## Real-World Scenarios

### Scenario 1: Building a Hiring Package

**Goal:** Create everything for a new job opening

**Best Choice:** Workflow 2 (Complete)

**Flow:**
```
1. User fills out WORK form
2. User provides basic JD
3. Click "Create Interview Package"
4. Get back: Enhanced JD + 5-question interview
5. Done!
```

---

### Scenario 2: Improving Existing Job Descriptions

**Goal:** Enhance a job description that will be posted internally

**Best Choice:** Workflow 1 (JD Enhancement)

**Flow:**
```
1. User fills out WORK form
2. User provides basic JD
3. Click "Enhance JD"
4. Review enhanced JD
5. Make edits if needed
6. Post to career page
7. Later: Generate interview if needed
```

---

### Scenario 3: Quick Interview Creation

**Goal:** You already have an enhanced JD, just need the interview

**Best Choice:** Standalone Interview Generation

**Endpoint:**
```
POST /api/interview/generate
{
  "req_id": "REQ-12345",
  "job_description_id": 123,
  "interview_name": "Senior Engineer Interview"
}
```

---

## WORK Methodology is the Same

Both workflows use the SAME WORK methodology:

- **work_output** - What will they build?
- **work_role** - What are their responsibilities?
- **work_knowledge** - What knowledge is critical?
- **work_competencies** - What competencies are essential?

**Key Point:** The more detailed your WORK inputs, the better the enhancement AND interview.

See **WORK_METHODOLOGY_GUIDE.md** for detailed guidance on filling out WORK fields.

---

## Quick Decision Tree

```
Do you need BOTH enhanced JD AND interview?
    ├─ YES → Use Workflow 2 (/api/interview/workflow/full)
    └─ NO
        ├─ Need enhanced JD only? → Use Workflow 1 (/api/interview/jd/enhance)
        └─ Have JD, need interview? → Use Standalone Interview Generation
```

---

## Error Handling

### If JD Enhancement Fails (Workflow 2)
```json
{
  "success": false,
  "error": "Claude API rate limit exceeded",
  "req_id": "REQ-12345"
}
```
→ Fix: Wait a few seconds and retry

### If Interview Generation Fails (Workflow 2)
```json
{
  "success": false,
  "error": "Claude API call failed",
  "job_description_id": 123,
  "message": "JD was enhanced successfully, but interview generation failed"
}
```
→ Fix: JD is saved. Retry interview generation later using Standalone Interview Generation.

---

## Tips for Success

### Workflow 1 (JD Enhancement)
1. ✅ Fill out WORK form completely
2. ✅ Provide detailed basic JD
3. ✅ Review enhanced JD for accuracy
4. ✅ Make manual edits if needed
5. ✅ Share with team before using

### Workflow 2 (Complete)
1. ✅ Fill out WORK form completely
2. ✅ Provide detailed basic JD
3. ✅ Have `interview_name` ready
4. ✅ Wait for both generation steps
5. ✅ Review both JD and interview together

---

## API Response Formats

### Workflow 1 Response
```json
{
  "success": true,
  "job_description_id": 123,
  "req_id": "REQ-12345",
  "basic_jd": { ... },
  "enhanced_jd": { ... },
  "work_inputs": { ... },
  "tokens_used": 1250,
  "created_at": "2025-01-09T12:00:00",
  "enhanced_at": "2025-01-09T12:00:05"
}
```

### Workflow 2 Response
```json
{
  "success": true,
  "job_description_id": 123,
  "interview_id": 456,
  "req_id": "REQ-12345",
  "interview": {
    "id": 456,
    "questions": [ ... ],
    "created_at": "2025-01-09T12:01:00"
  },
  "total_tokens_used": 3350,
  "created_at": "2025-01-09T12:00:00"
}
```

---

## Cost Estimation

### Workflow 1 (JD Enhancement)
- Cost per request: ~$0.05-0.10 (1,200-1,500 tokens at ~$0.003/1k tokens)
- Time: ~5-10 seconds

### Workflow 2 (Complete)
- Cost per request: ~$0.15-0.25 (3,200-4,000 tokens)
- Time: ~15-20 seconds

### Optimization
- Use **question caching** to reduce interview generation costs
- Similar topics will reuse cached questions

---

## Summary

| Need | Use This |
|------|----------|
| Just enhance JD | Workflow 1: `/api/interview/jd/enhance` |
| Enhance JD + generate interview together | Workflow 2: `/api/interview/workflow/full` |
| Generate interview from existing JD | Standalone: `/api/interview/generate` |
| Get previously saved JD | `/api/interview/jd/{req_id}` |
| Get previously saved interview | `/api/interview/{interview_id}` |

---

## Next Steps

1. **Understand WORK Methodology** → Read WORK_METHODOLOGY_GUIDE.md
2. **Test Workflow 1** → POST to `/api/interview/jd/enhance` with WORK inputs
3. **Test Workflow 2** → POST to `/api/interview/workflow/full`
4. **Review Results** → Check enhanced JD and interview questions
5. **Use in Production** → Integrate into your application
