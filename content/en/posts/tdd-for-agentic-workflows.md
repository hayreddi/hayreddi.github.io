---
title: "TDD for Agentic Workflows: Tests First, Architecture Later"
date: 2026-03-11
draft: false
categories: ["Software Stack"]
tags: ["ai", "tdd", "agentic-workflows", "simplicity", "testing", "claude-code", "kiro", "ground-truth"]
summary: "What if your entire codebase was just an orchestrator, a few agent prompts, and some tool definitions? And what if the tests came first, and the agents figured out the rest?"
---

Here is a radical idea: what if you wrote the tests first, and the AI agents figured out their own architecture?

Not "tests that validate code" in the traditional sense. Tests that define *what the system should accomplish*: the outcomes, the behaviors, the quality bars. And then agents, just system prompts, an orchestrator, and a set of tools, organize themselves to make those tests pass.

No application code. No frameworks. No service layers. Just tests, prompts, and tools.

This is what happens when you take test-driven development seriously in the age of AI agents. The result is something radically simple, and that simplicity is the entire point.

## The Simplest Possible Codebase

Let's be honest about what an agentic codebase actually needs:

1. **An orchestrator**: decides which agent handles what, manages handoffs
2. **Agents**: each defined by a system prompt describing its role and constraints
3. **Tools**: functions the agents can call (file operations, API calls, database queries, shell commands)
4. **Tests**: the expected behaviors and outcomes that define "done"

That's it. There is no business logic layer. No service classes. No repository pattern. No dependency injection container. No abstract factory factory. The agents *are* the business logic; their prompts encode the domain knowledge, their tools provide the capabilities, and the orchestrator manages the flow.

{{< figure src="/images/tdd-for-agentic-workflows/agentic-codebase.png" caption="The entire agentic codebase: tests, prompts, tools, and an orchestrator. That's it." >}}

Anthropic's own guidance on building effective agents confirms this instinct. They recommend "finding the simplest solution possible, and only increasing complexity when needed" and warn that "success in the LLM space isn't about building the most sophisticated system. It's about building the *right* system for your needs."

Simon Willison puts it even more directly: agents are just "LLMs calling tools in a loop to achieve a goal." That's the whole architecture. Everything else is accidental complexity.

## Tests Drive the Architecture

In traditional TDD, you write a failing test, then write the minimum code to make it pass. The tests drive the *implementation*. But the architecture, the classes, the modules, the interfaces, still comes from the developer's head.

In agentic TDD, the tests drive something deeper: they drive the *agent architecture itself*.

Here's how:

You start by writing comprehensive test cases that define what the system must do. Not how, but what. For example:

```yaml
test: "user-registration"
given:
  - a new user submits email and password
expect:
  - account is created in the database
  - welcome email is sent
  - auth token is returned
  - password is hashed, never stored in plaintext
  - duplicate email returns a clear error

test: "order-processing"
given:
  - a user places an order for 3 items
expect:
  - inventory is decremented for each item
  - payment is charged exactly once
  - confirmation email includes order summary
  - out-of-stock items are flagged before payment
```

These aren't unit tests for functions. They're behavioral specifications for outcomes. They're the *what*, the acceptance criteria that define success.

Now here's the key move: you give these test cases to an orchestrator agent, along with a set of tools (database access, email service, payment API, file system), and you let the agent figure out how to organize the work. It decides which sub-agents to invoke, in what order, with what prompts. It runs the tests. When they fail, it adjusts its approach, not by modifying code, but by refining prompts, reordering tool calls, or decomposing tasks differently.

The tests are the spec. The agents are the implementation. The architecture emerges from the conversation between the two.

## Why This Is Radically Simple

Consider what you're *not* doing in this model:

- **No application framework.** No Spring Boot, no Express, no Django. The orchestrator handles routing.
- **No service layer.** The agent's system prompt *is* the service; it encodes what the agent knows and what it should do.
- **No ORM or repository pattern.** The agent calls database tools directly. The tool interface is the abstraction.
- **No custom error handling hierarchy.** The agent observes failures and adapts. The test tells it what success looks like.
- **No deployment pipeline for application code.** There's no application code to deploy. You deploy prompts and tool definitions.

Your entire project looks like this:

```
project/
├── tests/
│   ├── user-registration.yaml
│   ├── order-processing.yaml
│   └── ...
├── agents/
│   ├── orchestrator.md          # System prompt
│   ├── backend-worker.md        # System prompt
│   ├── data-validator.md        # System prompt
│   └── reviewer.md              # System prompt
├── tools/
│   ├── database.py              # Tool definitions
│   ├── email.py                 # Tool definitions
│   ├── payment.py               # Tool definitions
│   └── filesystem.py            # Tool definitions
└── config.yaml                  # Orchestration rules
```

Count the moving parts. Tests, prompts, tools, config. A senior engineer can understand the entire system in an afternoon. A new team member can read every agent's system prompt in an hour.

Compare this to a typical microservice architecture: dozens of services, hundreds of classes, thousands of lines of glue code connecting things that could have been a prompt and a tool call.

{{< figure src="/images/tdd-for-agentic-workflows/tests-vs-code.png" caption="Traditional codebase: layers upon layers. Agentic codebase: four thin files." >}}

## The Eval Loop Is the New Red-Green-Refactor

Kent Beck's TDD cycle is: Red (write a failing test) → Green (make it pass) → Refactor (clean up).

The agentic equivalent is:

1. **Red**: Write a behavioral test that defines the expected outcome. Run it. The agent fails.
2. **Green**: Refine the agent's system prompt, adjust tool definitions, or restructure the orchestration until the test passes.
3. **Refactor**: Simplify. Can two agents become one? Can a tool be more general? Can a prompt be shorter?

Hamel Husain's framework for AI evaluations maps perfectly here. His Level 1 (unit tests, fast assertions on agent behavior), Level 2 (human review of agent traces), and Level 3 (A/B testing in production) form a natural progression from development to deployment.

The critical discipline, which Husain emphasizes, is looking at the data: "You are doing it wrong if you aren't looking at lots of data." In agentic TDD, this means reading agent traces, the full sequence of tool calls, decisions, and outputs, not just checking pass/fail. The trace *is* the implementation. Understanding it is understanding the system.

LangSmith's evaluation framework reinforces this: for agents, you test "correct tool selection and proper argument formatting or trajectory that the agent took." You're not testing code paths; you're testing decision paths.

## Testing What Matters

The biggest shift in agentic TDD is what you test. Traditional TDD tests implementation correctness: does this function return the right value? Agentic TDD tests behavioral outcomes: does the system achieve the right result?

This means your tests look different:

**Traditional TDD:**
```python
def test_hash_password():
    result = hash_password("secret123")
    assert result != "secret123"
    assert verify_password("secret123", result)
```

**Agentic TDD:**
```yaml
test: "password-security"
given:
  - user registers with password "secret123"
then:
  - database contains no plaintext passwords
  - user can authenticate with "secret123"
  - user cannot authenticate with "wrong-password"
```

The traditional test checks that a function works. The agentic test checks that the *system* works, regardless of how the agent chose to implement password hashing. Maybe it called a bcrypt tool. Maybe it used argon2. The test doesn't care. It cares about the outcome.

This is also where contract testing and the spec-driven patterns from [the previous post](/posts/spec-driven-development/) connect. The tests are the contracts. They define the expected behavior at each boundary. The agents can be reorganized, re-prompted, or even replaced. As long as the tests pass, the system is correct.

## Context Engineering Through Tests

Here's something subtle: well-written tests are also excellent context engineering.

Tobi Lutke described context engineering as "the art of providing all the context for the task to be plausibly solvable by the LLM." Drew Breunig identified four failure modes: context poisoning, distraction, confusion, and clash.

Comprehensive behavioral tests solve all four:

- **Poisoning**: tests catch errors immediately, preventing propagation
- **Distraction**: tests focus the agent on what matters: the expected outcome
- **Confusion**: tests eliminate ambiguity about what "done" means
- **Clash**: tests surface contradictions ("this test expects X but that test expects not-X")

When you give an orchestrator agent a complete test suite, you're giving it the best possible context for the task. The tests *are* the specification, the success criteria, and the validation layer, all in one artifact.

## When You Already Have the Answers

There is an even more powerful variant of this pattern: what happens when you already have a ground truth dataset?

In many real-world domains, you have labeled data. You know what the correct output should be for a given input. Classification tasks, data extraction pipelines, content moderation systems, medical triage tools, fraud detection. The expected answers already exist, sitting in spreadsheets, databases, or annotated datasets that domain experts have painstakingly built over years.

This changes the game entirely. Instead of writing behavioral tests that describe *what should happen*, you load a dataset that contains *what the right answer is* for hundreds or thousands of cases. Then you point a builder agent, Claude Code, Kiro, or any agentic coding tool, at the dataset and say: "Iterate on the system design until precision and recall both hit 100%."

The builder agent's loop looks like this:

1. **Run** the current system against the ground truth dataset
2. **Measure** precision and recall (and any other metrics you care about)
3. **Analyze** the failure cases: false positives, false negatives, edge cases
4. **Refine** the prompts, tools, agent structure, or orchestration logic
5. **Repeat** until the metrics converge on the target

```yaml
ground_truth: "labeled-dataset.csv"
metrics:
  precision: 1.0
  recall: 1.0
iterate:
  agent: builder
  tools: [prompt-editor, tool-definer, orchestrator-config]
  strategy: "analyze failures, refine system, re-evaluate"
  stop_when: "all metrics meet targets"
```

This is not hypothetical. Kiro, AWS's spec-driven agentic IDE, already embodies this pattern: it transforms natural language intent into structured requirements, generates implementation with tests, and iterates until the specs are satisfied. Claude Code does the same when you give it a failing test suite and tell it to make everything green. The ground truth dataset is just a more comprehensive, domain-specific version of that test suite.

Hamel Husain's evaluation framework supports this directly. His Level 1 evaluations (fast assertions against known answers) are exactly ground truth checks. He emphasizes measuring "precision and recall separately to get a more accurate picture," especially when dataset classes are imbalanced. The ground truth dataset becomes both the evaluation harness and the training signal for iterative refinement.

The beauty of this approach is that the human expertise lives in the dataset, not in the code. Domain experts curate the ground truth. The builder agent figures out how to match it. When new edge cases appear, you add them to the dataset and re-run the loop. The system improves without anyone touching a prompt or rewriting a tool definition manually.

This is the ultimate expression of "tests first, architecture later." The ground truth *is* the test suite. The builder agent *is* the architect. And the iteration loop runs until the system is correct, not approximately correct, not "good enough for a demo," but correct against every labeled example in the dataset.

{{< figure src="/images/tdd-for-agentic-workflows/ground-truth-loop.png" caption="The ground truth iteration loop: run, measure, analyze failures, refine, repeat until precision and recall converge." >}}

## The Elegance of It

There's a reason this approach feels right. With the enormous power that AI models bring, the surrounding system should be *inversely* simple. The more capable the engine, the less scaffolding you need around it.

Think about it: if you have an engine that can understand natural language instructions, reason about complex problems, and call arbitrary tools, why would you write thousands of lines of code to constrain and direct it? Just tell it what you want (the tests), give it what it needs (the tools), and let it figure out the rest.

Anthropic recommends starting with a single LLM call before building orchestration. Use the simplest workflow pattern that works. Add complexity only when tests prove it's needed, not when your architecture diagram says so.

This is the same philosophy that made Unix powerful: small, composable tools connected by a simple interface (pipes). In the agentic world: small, focused prompts connected by a simple orchestrator. The tools are the capabilities. The tests are the specification. Everything else is noise.

## Getting Started

You don't need a framework to try this. Here's the minimum:

1. **Write 5 behavioral tests** for your next feature: what should happen, not how
2. **Define the tools** your agents need: database queries, API calls, file operations
3. **Write one agent prompt** that describes the agent's role and constraints
4. **Run the tests** and observe where the agent fails
5. **Refine the prompt** until the tests pass
6. **Add a second agent** only when the first one's prompt gets too complex for a single role

You'll be surprised how few agents you need. The instinct is to create one for every responsibility. The reality is that a well-prompted agent with good tools can handle more than you think.

Start simple. Stay simple. Add complexity only when the tests demand it.

## Key Takeaways

- **Your codebase is just tests, prompts, tools, and an orchestrator.** No frameworks, no service layers, no glue code. The agents *are* the business logic.
- **Tests come first, and they drive the architecture.** Write comprehensive behavioral tests, give them to the orchestrator, and let agents organize themselves to pass them.
- **Test outcomes, not implementations.** Agentic tests define what the system should accomplish, not how. The agent decides the how.
- **Simplicity is the goal, not a compromise.** The more powerful the AI engine, the less scaffolding you need. Complexity is a sign you're fighting the model instead of using it.
- **The eval loop is the new red-green-refactor.** Write a failing behavioral test → refine prompts/tools until it passes → simplify.
- **Ground truth datasets are the ultimate test suite.** When you have labeled data, point a builder agent at it and let it iterate until precision and recall hit 100%. The human expertise lives in the dataset, not the code.
- **Tests are context engineering.** A comprehensive test suite is the best possible context for an orchestrator agent: it's the spec, the success criteria, and the validation layer in one artifact.

## References

| Source | Description |
|---|---|
| [Anthropic, *Building Effective Agents*](https://www.anthropic.com/engineering/building-effective-agents) | "Find the simplest solution possible, and only increase complexity when needed" |
| [Anthropic, *SWE-bench Sonnet*](https://www.anthropic.com/engineering/swe-bench-sonnet) | Agent evaluation: testing the model + scaffolding as a unit |
| [Simon Willison, *AI Agents*](https://simonwillison.net/tags/agents/) | "LLMs calling tools in a loop to achieve a goal," simplicity as architecture |
| [Hamel Husain, *Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) | Three-level eval framework: unit tests → human review → A/B testing |
| [LangSmith, *Evaluation Concepts*](https://docs.smith.langchain.com/evaluation/concepts) | Testing tool selection, argument formatting, and agent trajectory |
| [Drew Breunig, *How Long Contexts Fail*](https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html) | Context failure modes: poisoning, distraction, confusion, clash |
| Kent Beck, *Test-Driven Development* (2003) | The original Red → Green → Refactor cycle |
| [Kiro](https://kiro.dev) | Spec-driven agentic IDE: requirements → design → implementation with iterative agent loops |
| [divan-agents](https://github.com/hayreddi/divan-agents) | Spec-driven multi-agent orchestration with YAML contracts |
