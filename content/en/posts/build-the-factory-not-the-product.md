---
title: "Build the Factory, Not the Product"
date: 2026-03-10
draft: false
categories: ["Software Stack"]
tags: ["ai", "software-engineering", "meta-programming", "developer-productivity"]
summary: "Stop writing code to solve problems. Start building systems that write the code for you. The upfront cost is higher, but the marginal cost drops to near zero."
---

There is a quiet revolution happening in how software gets built, and most developers are missing it.

The old way: you have a problem, you write code to solve it. Requirements change, you rewrite. A new edge case appears, you patch. Multiply this across every feature, every project, every team. This is the craft model, skilled hands producing one artifact at a time.

The new way: you build a system that writes the code. You don't solve the problem directly. You solve the *class* of problems by creating a machine that produces solutions. Then you iterate on the machine until its output is right.

This is the difference between being a craftsman and being a factory builder.

{{< figure src="/images/build-the-factory/craftsman-vs-factory.png" caption="Left: the craftsman, solving one problem at a time. Right: the factory builder, designing the system that solves them all." >}}

## The Paradigm Shift

Writing code directly solves one problem once. Building a system that writes code solves a class of problems forever.

Consider the difference:

- **Direct coding**: You need a REST API for a new service. You write the routes, the validation, the error handling, the tests. It takes a week. Next service? Another week.
- **System approach**: You build a system, a combination of templates, AI prompts, configuration schemas, and validation rules, that generates REST APIs from a spec. The first version takes two weeks. But the next service takes an hour. And the next one, ten minutes.

The upfront cost is higher. The marginal cost drops to near zero.

This isn't a new idea in principle. Compilers, code generators, and infrastructure-as-code tools have always embodied this thinking. What's new is that AI has collapsed the barrier to entry. Building "a system that writes code" no longer means writing a compiler. It means assembling a well-structured prompt, a context window, a feedback loop, and letting a language model do the generation.

## The Iteration Loop

Here's what nobody tells you: the system won't work on the first try. Or the fifth. Maybe not even the twentieth.

This is where most people give up. They try the system approach once, get mediocre output, and conclude that it's faster to just write the code themselves. They're measuring the wrong thing.

The iteration loop looks like this:

1. **Define** what the system should produce
2. **Run** the system
3. **Observe** where the output fails
4. **Refine** the system, not the output
5. **Repeat**

{{< figure src="/images/build-the-factory/iteration-loop.png" caption="The iteration loop: Define → Run → Observe → Refine the system → Repeat. Each cycle improves all future outputs." >}}

The critical discipline is step 4: you fix the *system*, not the *output*. If the generated code has a bug, you don't patch the generated code. You fix the generator so that bug can never appear again. Every iteration improves all future outputs, not just the current one.

This feels painfully slow at first. You could have "just written it" in the time it took to debug your system. But you're not optimizing for today. You're optimizing for the hundredth time you need the same kind of output.

## The Iteration Tax of Direct Coding

Every line of hand-written code carries a hidden tax: the cost of changing it later.

Requirements shift. Stakeholders change their minds. The market moves. And every time, you go back into the code, your carefully crafted, artisanal code, and rewrite. You refactor. You introduce bugs while fixing other bugs. You spend half your engineering time not building new things but maintaining and updating old things.

This is the iteration tax, and it compounds relentlessly.

With a system, the tax works differently. When requirements change, you adjust the system and regenerate. The system absorbs the complexity. The output stays clean. You don't carry forward the accumulated weight of every past decision. You regenerate from a source of truth that reflects current reality.

The system is the single point of change. The output is disposable.

## AI Makes This Viable Now

Before 2024, building "a system that writes code" was an enterprise-scale investment. You needed compiler engineers, DSL designers, or at minimum a team that could build and maintain sophisticated code generation pipelines.

Now you need a well-crafted prompt, a clear specification, and a feedback loop.

The components of a modern code-writing system:

- **A specification format**: what you want, expressed in a structured way (a schema, a config file, a natural language brief with constraints)
- **An AI model**: the engine that transforms specification into code
- **Context**: examples, conventions, existing codebase patterns that guide the output
- **A validation layer**: tests, type checks, linting, or human review that verify the output
- **A feedback mechanism**: failures in validation feed back into refining the system

This is not prompt engineering. This is systems engineering applied to AI-assisted code generation. The prompt is just one component. The system is the entire pipeline from intent to working, validated code.

## Real Examples

This pattern is already emerging everywhere:

- **Infrastructure as Code** (Terraform, Pulumi): You don't SSH into servers and run commands. You describe what you want, and the system produces the infrastructure. When requirements change, you change the description, not the infrastructure.

- **CI/CD pipelines**: You don't manually build, test, and deploy. You build a system that does it. The pipeline is the factory; the deployed artifact is the product.

- **AI coding agents**: Tools like Claude Code, Cursor, and Codex don't just autocomplete lines. When used well, they become the runtime of a system you design, where your prompts, context files, and conventions form the "factory" that produces the code.

- **This blog**: These posts are written in markdown, committed to a Git repository, and automatically built and deployed by a system (Hugo + GitHub Actions). The system is the factory. Each post is a product that flows through it with zero manual deployment effort.

## The Mindset Problem

Most developers are trained to think: *"What code solves this problem?"*

The new question is: *"What system produces the code that solves this problem?"*

It's one level of indirection, and it feels deeply unnatural. We are trained to be craftsmen. We take pride in elegant code, clever solutions, clean architectures. Building a system that generates "good enough" code feels like cheating. It feels like giving up control.

But this is exactly the shift that happened in manufacturing two centuries ago. Artisans who hand-built furniture were replaced not by better artisans but by people who built factories. The factory owner didn't need to be a better woodworker. They needed to be a better systems thinker.

The same transition is happening in software. The most productive developers of the next decade won't be the ones who write the best code. They'll be the ones who build the best systems for producing code.

## Who Wins

The math is brutal and simple:

- A developer writing code directly produces *N* units of output per week
- A developer who spends 3 weeks building a system that generates code produces *0* units for 3 weeks, then *50N* per week indefinitely

{{< figure src="/images/build-the-factory/leverage-multiplier.png" caption="The crossover point: the system builder invests upfront, then outproduces the manual coder exponentially." >}}

The system builder looks unproductive at first. They have nothing to show in sprint reviews. Their manager asks why they're "not shipping." But by month two, they're outproducing the entire team. By month six, they've changed what's possible.

Teams and individuals who build these meta-systems will outpace those who keep hand-writing code by 10-100x. Not because they're smarter or faster, but because they're operating at a different level of leverage.

The question isn't whether to make this shift. It's whether you make it now, while it's a competitive advantage, or later, when it's table stakes.

## Key Takeaways

- **Stop solving problems directly with code.** Build systems that produce the code to solve problems. The upfront cost is higher, but the marginal cost approaches zero.
- **Iterate on the system, not the output.** When the generated code has a bug, fix the generator, not the generated code. Every fix improves all future outputs.
- **AI collapsed the barrier.** You no longer need compiler engineers to build code-writing systems. A well-structured prompt + context + validation loop is a factory.
- **The iteration tax of direct coding compounds.** Every requirement change means rewriting hand-crafted code. With a system, you adjust the spec and regenerate.
- **The mindset shift is the hard part.** Moving from "what code solves this?" to "what system writes the code?" feels unnatural, but it's where the 10-100x leverage lives.
