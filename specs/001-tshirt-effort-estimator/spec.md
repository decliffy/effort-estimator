# Feature Specification: T-Shirt Size Effort Estimator

**Feature Branch**: `001-tshirt-effort-estimator`
**Created**: 2026-05-07
**Status**: Draft
**Input**: User description: "I want to build an effort estimator that takes a task description and estimates in t-shirt size the effort needed to complete it"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get Effort Estimate for a Task (Priority: P1)

A user provides a plain-language description of a task and receives a t-shirt size
estimate (XS, S, M, L, XL, or XXL) along with a brief rationale explaining why that
size was assigned.

**Why this priority**: This is the core value proposition — without it, the tool does not
exist. All other stories build on this foundation.

**Independent Test**: Can be fully tested by providing a task description and verifying
that a valid t-shirt size and rationale are returned. Delivers standalone value as a
minimal viable estimator.

**Acceptance Scenarios**:

1. **Given** a clear, well-described task, **When** the user submits it for estimation,
   **Then** the tool returns one of XS / S / M / L / XL / XXL and a 1–3 sentence
   rationale that references specific aspects of the task description.

2. **Given** a very brief or vague task description, **When** the user submits it,
   **Then** the tool returns an estimate with a rationale that explicitly notes the
   assumptions made due to limited detail.

3. **Given** an empty or whitespace-only input, **When** the user submits it,
   **Then** the tool returns a clear error message asking the user to provide a task
   description — no estimate is produced.

---

### User Story 2 - Understand What Each Size Means (Priority: P2)

A user who is unfamiliar with the t-shirt sizing scale can ask the tool to explain
what each size represents in terms of relative effort and complexity.

**Why this priority**: Without a shared understanding of the scale, estimates are
meaningless. This story makes the output actionable for first-time users.

**Independent Test**: Can be fully tested by invoking the help/explain mode and
verifying that definitions for all six sizes (XS through XXL) are displayed with
consistent, comparable descriptions.

**Acceptance Scenarios**:

1. **Given** a user who wants to understand the sizing scale, **When** they request
   an explanation of the t-shirt sizes, **Then** the tool displays a description of
   each size (XS through XXL) covering relative effort, typical scope indicators,
   and examples.

2. **Given** an estimate has just been produced, **When** the user asks what the
   returned size means, **Then** the tool shows the definition of that specific size
   in context.

---

### User Story 3 - Batch Estimate Multiple Tasks (Priority: P3)

A user provides a list of task descriptions (one per line or via a file) and receives
a t-shirt size estimate for each task in a single operation.

**Why this priority**: Teams routinely need to estimate a backlog of tasks at once.
Batch mode eliminates repeated single invocations and enables comparison across tasks.

**Independent Test**: Can be fully tested by providing two or more task descriptions
and verifying that each receives its own size and rationale, with output clearly
associated to each input task.

**Acceptance Scenarios**:

1. **Given** a list of 2 or more task descriptions, **When** the user submits them
   for batch estimation, **Then** the tool returns a size and rationale for every
   task, preserving the input order.

2. **Given** a batch input where one task description is empty or invalid, **When**
   the user submits the batch, **Then** the tool returns an error for that specific
   task and still produces valid estimates for all other tasks.

---

### Edge Cases

- What happens when the task description is extremely long (>1000 words)?
  The tool MUST still produce an estimate; it MAY truncate or summarise the input
  internally but MUST disclose this in the rationale.
- What happens when the task is clearly out of scope (e.g., "build the entire internet")?
  The tool returns XXL with a rationale noting the task is too large to estimate
  meaningfully and should be broken down.
- What happens when the task description is in a language other than English?
  The tool returns an estimate if it can interpret the description; otherwise it
  returns an error indicating the input could not be understood.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The tool MUST accept a free-text task description as input and return
  a t-shirt size estimate from the set {XS, S, M, L, XL, XXL}.
- **FR-002**: Every estimate MUST be accompanied by a rationale of 1–3 sentences
  explaining the factors that drove the sizing decision.
- **FR-003**: The rationale MUST reference specific aspects of the provided task
  description (not generic boilerplate).
- **FR-004**: The tool MUST return a clear, actionable error message when given an
  empty or invalid input — no estimate is produced for invalid input.
- **FR-005**: The tool MUST provide a way for users to view the definition and
  scope indicators for each t-shirt size.
- **FR-006**: The tool MUST support estimating multiple tasks in a single invocation,
  returning one estimate per task in the order they were provided.
- **FR-007**: For vague or ambiguous task descriptions, the tool MUST still produce
  an estimate and MUST explicitly state in the rationale what assumptions were made.
- **FR-008**: The tool MUST support both human-readable and structured (e.g., JSON)
  output formats, selectable by the user at invocation time.

### Key Entities

- **Task**: A unit of work described in plain language. Key attributes: description
  (text), estimated size (XS/S/M/L/XL/XXL), rationale (text), assumptions (text,
  optional).
- **SizeDefinition**: The canonical description of a t-shirt size. Key attributes:
  size label, relative effort description, typical scope indicators, example task types.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can submit a task description and receive a t-shirt size estimate
  with rationale in under 10 seconds for single-task inputs.
- **SC-002**: When the same task description is submitted twice, the tool returns the
  same t-shirt size both times (deterministic output).
- **SC-003**: 100% of outputs include a rationale that references at least one element
  from the input task description — no generic, input-independent responses.
- **SC-004**: Users can estimate a backlog of 10 tasks in a single invocation in under
  60 seconds.
- **SC-005**: First-time users can obtain a correct estimate without reading external
  documentation, relying only on the tool's built-in help.

## Assumptions

- The tool is delivered as a command-line interface (CLI) consistent with the project's
  CLI Contract standard: text input via arguments or stdin; results to stdout;
  errors to stderr.
- T-shirt sizes represent relative effort and complexity, not calendar duration or
  team headcount.
- The sizing scale is fixed at six values: XS, S, M, L, XL, XXL. No custom scales
  are in scope for this version.
- No authentication or user accounts are required; the tool is stateless and does not
  persist estimates between invocations.
- No external integrations (issue trackers, project management tools) are in scope
  for this version.
- The primary input language is English; non-English inputs are best-effort.
- Single-user operation is assumed; no concurrent or multi-user scenarios are in scope.
