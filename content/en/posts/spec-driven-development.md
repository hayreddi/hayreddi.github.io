---
title: "Spec-Driven Development: Let the Contract Do the Talking"
date: 2026-03-10
draft: false
categories: ["Software Stack"]
tags: ["ai", "multi-agent", "spec-driven", "context-engineering", "developer-productivity", "claude-code"]
summary: "When you have six AI agents named after Ottoman court officials, you'd better have airtight contracts, or the empire falls apart."
---

There's a problem with multi-agent AI systems that nobody wants to talk about: they fail silently, confidently, and at the worst possible time.

You spin up an AI agent to decompose a feature into tasks. It produces something that *looks* reasonable. You hand that output to an implementation agent. It writes code that *looks* correct. A review agent approves it. You ship. And three days later, you discover the decomposition missed a critical dependency, the implementation skipped integration tests, and the reviewer waved it through because the output *looked* like what it expected.

The root cause isn't that AI agents are bad at their jobs. It's that nobody defined what "good" looks like at each handoff point.

This is the problem that spec-driven development solves.

## Standing on the Shoulders of Contracts

The idea of defining explicit agreements between software components is not new. It has a long and proven lineage:

**Design by Contract**, introduced by Bertrand Meyer in 1986 with the Eiffel programming language, established that software components should interact through formal preconditions ("what I require"), postconditions ("what I guarantee"), and invariants ("what stays true"). If a component violates its contract, the system fails loudly, not silently.

**API-First Development**, championed by the OpenAPI/Swagger ecosystem, took this further: design the API specification before writing a single line of implementation. The spec becomes the source of truth. Teams build against it in parallel. Mock servers generate from it. Documentation stays in sync because it *is* the spec.

**Consumer-Driven Contracts**, described by Ian Robinson on Martin Fowler's blog, flipped the direction: instead of providers dictating what they expose, contracts emerge from what consumers actually need. The provider's real contract is "the union of existing consumer expectations," nothing more, nothing less.

**Contract Testing**, popularized by the Pact framework, made these contracts machine-verifiable. Each service can be tested independently against its contract. The contract is generated from code, so it never drifts from reality.

**Context Engineering**, the discipline that emerged in 2025 around AI systems, recognized that "the art of providing all the context for the task to be plausibly solvable by the LLM" (as Shopify CEO Tobi Lutke put it) is itself an engineering problem. What goes into the context window, in what structure, with what constraints. This determines whether the AI succeeds or hallucinates.

What I'm calling **spec-driven development** is the convergence of all of these ideas, applied to a new domain: multi-agent AI workflows. It means defining explicit, machine-validated YAML contracts between every agent handoff, with required fields, type constraints, enum values, and business rules that are checked automatically, while carefully engineering the context each agent receives.

Think of it as Design by Contract meets Context Engineering. Every agent gets a contract that says: "Here's exactly what you'll receive as input. Here's exactly what you must produce as output. Here are the validation rules. Violate them and you don't pass go."

I built a framework around this idea called [divan-agents](https://github.com/hayreddi/divan-agents). And yes, I named all the AI agents after Ottoman court officials, because if you're going to build a bureaucracy, you might as well commit to the aesthetic.

{{< figure src="/images/spec-driven-development/ottoman-court.png" caption="The Divan in session: AI agents convene in the Imperial Council chamber, YAML decrees glowing at the center." >}}

## The Ottoman Court of AI Agents

In the Ottoman Empire, the Divan was the Imperial Council, a structured hierarchy where every official had a clearly defined role, explicit authority boundaries, and formal protocols for passing information up and down the chain. Sound familiar? It should. It's exactly what a multi-agent AI system needs.

Here's the court:

| Agent | Ottoman Title | Role |
|---|---|---|
| **Chief of Staff** | Sadrazam (Grand Vizier) | Orchestrates the entire workflow, validates contracts at every handoff |
| **Task Decomposer** | Divan Katibi (Council Scribe) | Breaks epics into child issues with dependency tracking |
| **Design Architect** | Mimar Basi (Chief Architect) | Creates comprehensive design documents |
| **Backend Expert** | Usta (Master Craftsman) | Implements backend services with mandatory integration tests |
| **Mobile Developer** | Hunkar Ustasi (Royal Craftsman) | Implements mobile features with i18n enforcement |
| **Code Reviewer** | Mufettis (Inspector) | Reviews implementation against quality checklist |

The Sadrazam doesn't trust anyone. Not because the agents are incompetent; they're quite good at their individual jobs. But because the Sadrazam knows that "quite good" without validation is how empires fall. Every time one agent hands work to another, the Sadrazam checks the output against a YAML contract. If validation fails, the work goes back. No exceptions. No "it's probably fine."

This is the Grand Vizier's one job: enforce the contracts. Just as Meyer's Design by Contract makes a failing precondition halt the program, a failing contract halts the pipeline. The error is loud, immediate, and traceable.

## The Contracts

Here's where it gets concrete. In [divan-agents](https://github.com/hayreddi/divan-agents), every agent handoff is governed by a YAML contract in `.claude/contracts/`. These are the postconditions: what each agent must guarantee.

The task decomposer contract defines exactly what the Divan Katibi must produce:

```yaml
output:
  parent_issue:
    title:
      type: string
      required: true
      pattern: "^\\[Epic\\]"  # Must start with [Epic]
    body:
      type: string
      required: true
      contains: "- [ ]"       # Must have task checkboxes
  child_issues:
    type: array
    min_length: 1
    items:
      title:
        pattern: "^\\[(backend|mobile)\\]"  # Must declare which repo
      body:
        contains: "Part of #"               # Must reference parent
      repository:
        type: string
        required: true
```

This isn't documentation. It's a machine-readable specification, closer to a Pact contract than a README. If the Divan Katibi produces an issue without the `[Epic]` prefix, it fails. If a child issue doesn't reference its parent, it fails. If a backend task gets routed to the mobile repo, it fails.

The implementation agent contract applies the same rigor to the Usta's output:

```yaml
validation_rules:
  completion_integrity:
    condition: "status == 'completed'"
    requires:
      - "all quality_checks values are true"
      - "cleanup_performed is true"
  backend_testing:
    condition: "project_type == 'backend'"
    requires:
      - "quality_checks.integration_tests is true"
  mobile_testing:
    condition: "project_type == 'mobile'"
    requires:
      - "testing_directives is not empty"
```

Translation: you cannot claim your work is "completed" unless every quality check passes, you've cleaned up after yourself, backend changes have integration tests, and mobile changes include testing directives for QA. The Usta doesn't get to say "done" until the contract says so. Meyer would approve.

{{< figure src="/images/spec-driven-development/contract-validation.png" caption="The Sadrazam's checkpoint: every agent output is validated against its YAML contract before it can pass." >}}

## Why This Works (And Why Vibes-Based Development Doesn't)

Most AI agent systems today run on vibes. The system prompt says "be thorough" and "check your work" and "follow best practices." These are the equivalent of a manager saying "do a good job" and then being surprised when the output is inconsistent.

This is the context engineering problem. As Drew Breunig identified, AI systems fail through context poisoning (errors that propagate), context distraction (too much noise), context confusion (superfluous information), and context clash (conflicting instructions). Vague prompts like "follow best practices" are practically designed to trigger all four failure modes.

Spec-driven development replaces vibes with verification:

| Vibes-Based | Spec-Driven |
|---|---|
| "Make sure to write tests" | `quality_checks.integration_tests: required: true` |
| "Reference the parent issue" | `body.contains: "Part of #"` |
| "Use the right repository" | `repository: enum: [backend-service, mobile-app]` |
| "Do a thorough code review" | Checklist with 6 boolean fields, all must be `true` for APPROVE |
| "Clean up when you're done" | `cleanup_performed: type: boolean, required: true` |

{{< figure src="/images/spec-driven-development/vibes-vs-specs.png" caption="Left: vibes-based development, chaos. Right: spec-driven development, order through contracts." >}}

The vibes approach works when you have one senior developer paying close attention. It collapses the moment you scale to multiple agents, multiple repositories, or multiple workflows running in parallel. The spec approach works the same whether you have one agent or twenty, whether you're watching or asleep.

This is the same lesson the API-first community learned: when you define the contract before implementation, everyone can work independently and still integrate correctly. The contract *is* the coordination mechanism.

## The Validation Layer

In `divan-agents`, contract validation is itself a [skill](https://github.com/hayreddi/divan-agents/blob/main/.claude/skills/contract-validation/SKILL.md), a reusable knowledge module that the Sadrazam invokes at every handoff point.

The validation process mirrors what Pact does for microservices, adapted for AI agents:

1. **Load** the relevant contract YAML
2. **Parse** the agent's output
3. **Validate schema**: are all required fields present? Correct types? Within enum values?
4. **Validate business rules**: do cross-field dependencies hold? Does the conditional logic check out?
5. **Auto-fix trivials**: whitespace issues, case mismatches get corrected silently
6. **Escalate failures**: anything substantive goes back to the agent with a structured error report

The Sadrazam doesn't read the code. The Sadrazam doesn't understand backend architecture or mobile patterns. The Sadrazam just checks contracts. And that's enough, because if the contracts are well-designed, checking them *is* checking quality.

This is the key insight: **you don't need a super-intelligent orchestrator. You need a super-strict one.** The Grand Vizier's power came not from being the smartest person in the room, but from being the one who enforced the Sultan's decrees without exception.

## Context Engineering Through Contracts

Here's what makes this more than just "contracts for AI": the contracts double as context engineering.

Each contract defines exactly what context the next agent receives. The task decomposer's output contract is the implementation agent's input context. By constraining what the decomposer can produce, you're also constraining, and optimizing, what the implementer receives.

This solves the four context failure modes:

- **Context Poisoning**: contracts catch errors before they propagate to downstream agents
- **Context Distraction**: contracts define only the fields that matter, filtering noise
- **Context Confusion**: required fields and types eliminate ambiguity
- **Context Clash**: validation rules ensure internal consistency

The contract is both the quality gate *and* the context window curator. Two problems, one artifact.

## Opt-In Orchestration

Not everything needs the full Ottoman bureaucracy. Sometimes you just want to fix a typo. Even the context-driven testing community would agree: the value of any practice depends on its context.

`divan-agents` uses opt-in orchestration triggered by keywords. Say "orchestrate issue #43" and you get the full Divan: decomposition, implementation, review, validation at every step. Say "fix issue #43" and you get a single agent working directly, no contracts, no ceremony.

```
"orchestrate issue #43"    → Sadrazam takes over, full workflow
"automate issue #43"       → Same as above
"full workflow for #43"    → Same as above

"fix issue #43"            → Direct implementation, no orchestration
"implement issue #43"      → Direct, single agent
```

The rule of thumb: orchestrate for new features and complex work, go direct for fixes and refinements. Even the Ottoman Empire didn't convene the full Imperial Council to fix a leaky faucet.

## The Spec Is the Documentation

Here's a side effect I didn't expect: the contracts became the best documentation in the project.

The API-first community discovered this years ago: when your OpenAPI spec *is* your API, documentation never drifts. The same principle applies here. The contracts are always up to date because they're enforced at runtime. If a contract is wrong, the workflow breaks, and someone fixes it immediately.

New to the team? Don't read a wiki. Read the contracts. They tell you exactly:

- What the task decomposer must produce (and what it must NOT produce)
- What "done" means for an implementation (every field is explicit)
- What the code reviewer checks (it's a boolean checklist, not prose)
- What triggers a rejection vs. an approval

Compare this to documentation that was accurate six months ago and has been slowly diverging from reality ever since.

## Building Your Own Spec-Driven Workflow

You don't need six Ottoman agents to adopt this pattern. Start with one contract:

1. **Pick your most error-prone handoff point**: the place where work most often comes back because "it wasn't what I expected"
2. **Write a YAML contract** defining the exact expected output: required fields, types, constraints. Think of it as writing the postcondition for that stage.
3. **Add validation** before the next stage can start. This is your precondition check.
4. **Iterate**: when failures happen, add the missing rule to the contract

This is the same iteration loop from [Build the Factory, Not the Product](/posts/build-the-factory-not-the-product/). The contract is the factory. The agent output is the product. When the product is wrong, you fix the factory.

Over time, your contracts will accumulate every edge case, every "obvious" requirement that wasn't obvious, every implicit expectation made explicit. They become the institutional memory of your process, a living specification that improves with every failure.

## Key Takeaways

- **The idea is old. The application is new.** Design by Contract (1986), API-First, Consumer-Driven Contracts, and Context Engineering all converge in spec-driven AI development. You're not inventing; you're synthesizing.
- **Define contracts before work starts.** Explicit YAML schemas with required fields, types, and validation rules beat vague instructions every time.
- **Contracts are context engineering.** Each contract defines what the next agent receives. Constrain the output, and you optimize the downstream context.
- **Validate at every handoff.** Don't trust that agents (human or AI) will produce correct output. Check it. Automatically.
- **The orchestrator doesn't need to be smart; it needs to be strict.** The Sadrazam's entire job is checking contracts. That's enough.
- **Opt-in complexity.** Not everything needs full orchestration. Use the Divan for complex features, direct agents for simple fixes.
- **Contracts are living documentation.** Unlike wikis, they're always current because they're enforced at runtime.

The [divan-agents](https://github.com/hayreddi/divan-agents) framework is open source. Go explore the contracts, summon the Sadrazam, and let the Ottoman court bring order to your multi-agent chaos.

Just don't try to rename the agents. The Grand Vizier will not approve.

## References

| Source | Description |
|---|---|
| Bertrand Meyer, *Object-Oriented Software Construction* (1988) | Design by Contract: preconditions, postconditions, invariants |
| Swagger/OpenAPI, *Adopting an API-First Approach* | API-first development principles and benefits |
| Ian Robinson, *Consumer-Driven Contracts* (martinfowler.com) | Contracts derived from consumer expectations |
| Pact Foundation, *What Is Contract Testing?* (pactflow.io) | Machine-verifiable contracts between services |
| Tobi Lutke / Simon Willison / Drew Breunig, *Context Engineering* (2025) | Managing AI context windows: poisoning, distraction, confusion, clash |
| Cem Kaner et al., *Context-Driven Testing* | "The value of any practice depends on its context" |
| [divan-agents](https://github.com/hayreddi/divan-agents) | Open-source spec-driven multi-agent orchestration framework |
