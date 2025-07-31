# Claude Pro Workflow Templates

## Daily Standup Template
```
DAILY STANDUP - [DATE]

PROJECT: Hybrid LLM Quantitative Trading Platform
CURRENT PHASE: Week 3 - LLM Integration & Orchestration
ROADMAP POSITION: 0.3.3.2 - Implementing RoutingLogger structured logging

YESTERDAY'S PROGRESS:
- [Specific accomplishments]
- [Code changes implemented]
- [Issues resolved]

TODAY'S OBJECTIVES:
- [Primary goal - specific and measurable]
- [Secondary tasks]
- [Technical debt to address]

CURRENT BLOCKERS/RISKS:
- [Immediate blockers requiring attention]
- [Technical risks identified]
- [Dependencies waiting on]

TECHNICAL CONTEXT:
- System Status: [e.g., "All services running, LLM routing functional"]
- Recent Changes: [e.g., "Modified orchestrator fallback logic"]
- Environment: [e.g., "WSL2 + Docker, GPU passthrough working"]

REQUEST:
1. Analyze progress against roadmap timeline
2. Identify technical risks and mitigation strategies  
3. Prioritize today's implementation tasks
4. Provide architectural guidance for current work
5. Flag any potential integration issues
```

## Implementation Request Template
```
IMPLEMENTATION REQUEST - [FEATURE/ISSUE NAME]

CONTEXT:
- Current Phase: [Roadmap section]
- System State: [What's currently working]
- Recent Changes: [What was modified recently]

OBJECTIVE:
- Primary Goal: [What needs to be accomplished]
- Success Criteria: [How to measure completion]
- Constraints: [Technical limitations or requirements]

TECHNICAL DETAILS:
- Current Code: [Paste relevant code sections]
- Error/Issue: [Specific problem if debugging]
- Expected Behavior: [What should happen]
- Current Behavior: [What actually happens]

FILES INVOLVED:
- [List relevant files and their roles]

REQUEST:
1. Analyze the current implementation
2. Identify root cause (if debugging)
3. Provide solution with working code
4. Include testing approach
5. Document any architectural decisions
6. Flag integration considerations

DELIVERABLES NEEDED:
- [ ] Working code implementation
- [ ] Unit tests for new functionality  
- [ ] Documentation updates
- [ ] Integration testing guidance
```

## Code Review Template
```
CODE REVIEW REQUEST - [MODULE/FEATURE NAME]

DEVELOPMENT CONTEXT:
- Roadmap Phase: [Current phase]
- Implementation Status: [What's complete]
- Integration Points: [How this connects to other systems]

CODE SUBMISSION:
[Paste all relevant code files]

SPECIFIC REVIEW AREAS:
- [ ] Architecture consistency with project patterns
- [ ] Code quality and maintainability
- [ ] Error handling and edge cases
- [ ] Performance implications
- [ ] Security considerations
- [ ] Testing coverage adequacy
- [ ] Documentation completeness

CONCERNS/QUESTIONS:
- [Specific areas where you need guidance]
- [Trade-offs you're unsure about]
- [Performance or scalability concerns]

REQUEST:
1. Comprehensive code quality assessment
2. Architecture alignment verification
3. Security and performance review
4. Refactoring recommendations
5. Technical debt identification
6. Integration risk assessment
```

## Debugging Session Template
```
DEBUGGING SESSION - [ISSUE DESCRIPTION]

CRITICAL INFORMATION:
- Issue Impact: [System functionality affected]
- Urgency Level: [High/Medium/Low]
- First Occurrence: [When issue started]

SYSTEM CONTEXT:
- Services Status: [Docker containers, APIs, databases]
- Recent Changes: [Code/config modifications in last 24h]
- Environment: [Development/staging details]
- Current Roadmap Phase: [Where in development cycle]

ERROR DETAILS:
- Error Messages: [Complete error logs]
- Stack Traces: [Full stack traces if available]
- Reproduction Steps: [How to trigger the issue]
- Expected vs Actual: [Behavior comparison]

INVESTIGATION COMPLETED:
- [What you've already tried]
- [Hypotheses tested]
- [Partial solutions attempted]

FILES/SYSTEMS INVOLVED:
- [All relevant code files]
- [Configuration files]
- [Docker services affected]

DEBUGGING REQUEST:
1. Root cause analysis with technical explanation
2. Step-by-step diagnostic procedure
3. Immediate fix recommendations
4. Long-term solution strategy
5. Prevention measures for future
6. Testing approach to verify fix

URGENCY CONTEXT:
- Business Impact: [How this affects project timeline]
- Workaround Available: [Yes/No + details]
- Dependencies Blocked: [What can't proceed until fixed]
```

## Weekly Planning Template
```
WEEKLY PLANNING SESSION - WEEK [NUMBER]

ROADMAP CONTEXT:
- Current Phase: [Phase 0.X.X]
- Week Objectives: [From roadmap]
- Critical Milestones: [Key deliverables this week]

PREVIOUS WEEK ASSESSMENT:
- Planned vs Actual: [What was planned vs completed]
- Technical Debt Created: [Shortcuts taken, cleanup needed]
- Unexpected Challenges: [Issues that arose]
- Knowledge Gained: [New insights or learning]

CURRENT SYSTEM STATE:
- Architecture Maturity: [How stable is current system]
- Test Coverage: [Current testing status]
- Documentation Status: [What's documented vs missing]
- Performance Metrics: [Any benchmarks established]

THIS WEEK'S PRIORITIES:
- Must-Complete: [Non-negotiable deliverables]
- Should-Complete: [Important but deferrable]
- Could-Complete: [Nice-to-have improvements]
- Research-Needed: [Areas requiring investigation]

TECHNICAL FOCUS AREAS:
- [Primary development focus]
- [Integration challenges to address]
- [Performance optimizations needed]
- [Security considerations]

RISK ASSESSMENT:
- Technical Risks: [Code/architecture risks]
- Timeline Risks: [Schedule concerns]
- Dependency Risks: [External factors]
- Resource Risks: [Skills/tools needed]

WEEKLY PLANNING REQUEST:
1. Validate week's objectives against roadmap
2. Assess technical feasibility of planned work
3. Identify potential blockers and mitigation strategies
4. Optimize task sequencing and dependencies
5. Recommend focus areas for maximum impact
6. Flag any architectural decisions needed this week
```

## Project Upload Template
```
PROJECT ANALYSIS REQUEST

ANALYSIS TYPE: [Full System Review / Specific Module / Integration Assessment]

PROJECT CONTEXT:
- Development Phase: Week 3 - Hybrid LLM Integration
- Current Focus: Implementing RoutingLogger with structured JSON logging
- System Status: LLM orchestration functional, logging hooks exist but don't emit

ANALYSIS SCOPE:
- [Specific areas needing review]
- [Integration points to examine]
- [Performance areas to assess]
- [Security considerations to verify]

UPLOADED FILES:
- Complete project codebase
- Configuration files (.env, docker-compose, pyproject.toml)
- Documentation and roadmap materials
- Recent logs or error outputs

ANALYSIS REQUEST:
1. Comprehensive architecture review
2. Code quality and consistency assessment
3. Integration point analysis
4. Performance and scalability evaluation
5. Security and compliance review
6. Technical debt identification
7. Roadmap alignment verification

SPECIFIC QUESTIONS:
- [Areas where guidance is needed]
- [Trade-offs requiring decisions]
- [Implementation approaches to evaluate]

DELIVERABLES NEEDED:
- [ ] Architecture analysis with recommendations
- [ ] Code quality report with priorities
- [ ] Integration risk assessment
- [ ] Performance optimization opportunities
- [ ] Security improvements needed
- [ ] Roadmap timeline validation
- [ ] Next steps prioritization
```

## Usage Guidelines

### When to Use Each Template:
- **Daily Standup**: Every morning before starting development
- **Implementation Request**: When starting new features or major changes
- **Code Review**: Before committing significant code changes
- **Debugging Session**: When encountering complex technical issues
- **Weekly Planning**: Monday mornings for week organization
- **Project Upload**: Monthly or when major milestones completed

### Template Customization:
- Fill in bracketed placeholders with specific information
- Add project-specific context as needed
- Modify sections based on current development phase
- Include relevant code snippets and error messages

### Response Optimization:
- Be specific about what you need from Claude
- Provide complete context to avoid back-and-forth
- Include success criteria and constraints
- Request specific deliverables (code, tests, documentation)
