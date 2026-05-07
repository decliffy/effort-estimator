# Quickstart: T-Shirt Size Effort Estimator

**Phase 1 output** | **Branch**: `001-tshirt-effort-estimator` | **Date**: 2026-05-07

## Prerequisites

- Python 3.11 or later
- An Anthropic API key

## Setup

```bash
# Clone and enter the repo
git clone https://github.com/decliffy/effort-estimator.git
cd effort-estimator

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Set your API key
export ANTHROPIC_API_KEY=your_key_here   # Windows: set ANTHROPIC_API_KEY=your_key_here
```

## Estimate a Single Task

```bash
estimate "Add pagination to the user list endpoint"
```

Expected output:
```
Size:       S
Rationale:  Adding pagination to an existing endpoint is a well-understood pattern
            requiring a query parameter, minor service logic, and a test update.
Assumptions: (none)
```

## Get a JSON Response

```bash
estimate --format json "Add pagination to the user list endpoint"
```

## View the Sizing Scale

```bash
estimate sizes
```

## Estimate a Batch of Tasks

Create a file `tasks.txt`:
```
Add pagination to the user list endpoint
Migrate the authentication system to OAuth2
Fix typo in the onboarding email subject line
```

Then run:
```bash
estimate --batch tasks.txt
```

## Pipe from Stdin

```bash
echo "Rebuild the reporting engine from scratch" | estimate --format json
```

## Run the Tests

```bash
pytest
```

All tests MUST pass before submitting a PR. Tests MUST be written before implementation
(see constitution Principle III).

## Validate the Quickstart

After any significant change to the project, run through the steps above end-to-end to
confirm nothing is broken before merging.
