# Effort Estimator

A CLI tool that estimates software task effort using t-shirt sizes (XS/S/M/L/XL/XXL) via the Anthropic Claude API.

## Installation

```bash
git clone https://github.com/decliffy/effort-estimator.git
cd effort-estimator
python -m pip install -e ".[dev]"
```

## Requirements

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

```bash
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

### Estimate a single task

```bash
estimate estimate "Add pagination to the user list endpoint"
```

```
Size:       S
Rationale:  Adding pagination is a well-understood pattern requiring a query parameter
            and minor service logic change.
Assumptions: (none)
```

### Get JSON output

```bash
estimate estimate --format json "Refactor the authentication service"
```

### View the sizing scale

```bash
estimate sizes
estimate sizes --format json
```

### Estimate a batch of tasks

Create `tasks.txt` with one task per line, then:

```bash
estimate estimate --batch tasks.txt
estimate estimate --batch tasks.txt --format json
```

### Pipe from stdin

```bash
echo "Rewrite the reporting engine" | estimate estimate
```

## Running Tests

```bash
python -m pytest
```

## Environment Variables

| Variable            | Required | Description               |
|---------------------|----------|---------------------------|
| `ANTHROPIC_API_KEY` | Yes      | Your Anthropic API key    |
