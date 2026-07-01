# BelastingBuddy – Product Requirements Document

#1. Overview
BelastingBuddy is an AI assistant that helps users understand Dutch income tax filing requirements and workflows through grounded question answering.

#2. Problem statement
Users often find Dutch tax filing confusing because rules, document requirements, and filing paths vary by situation.

#3. Goal
Provide clear, source-grounded, non-legal guidance for Dutch tax filing questions.

#4. Users
- Dutch residents filing annual income tax returns
- Expats or migrants dealing with Dutch filing guidance
- Users needing help preparing documents before filing

#5. Primary use cases
- What documents do I need to file?
- How do I file online?
- What should I do if I moved into or out of the Netherlands this year?
- Where can I log in and start my tax return?

#6. In scope
- Guidance for Dutch individual income tax return flows
- Document checklist support
- Filing-step assistance
- Special migration-year guidance

#7. Out of scope
- Legal advice
- Tax calculation engine
- Submission to Belastingdienst
- Personalized tax outcome prediction

#8. Functional requirements
- Upload and manage trusted documents in Plain Text (.txt) and PDF (.pdf) formats
- Answer questions with citations
- Show source title and excerpt
- Maintain conversation history per session
- Capture feedback on answers

#9. Non-functional requirements
- Secure, local-only handling of uploaded content (GDPR compliant)
- Fast enough for interactive use (under 3 seconds per query locally)
- Explainable answers with source grounding
- Logging and traceability
- Automated unit/integration test coverage (>80% of backend and helper functions)

#10. Success metrics
- Answer grounding rate
- User feedback score
- Median response time
- Coverage of top user questions

#11. Risks
- Hallucinated answers
- Outdated tax guidance
- Over-trust by users
- Incomplete source coverage

#12. Open questions
- Which official sources will be included first?
- Will access be public demo only or internal?
- Which model will be used in v1?
