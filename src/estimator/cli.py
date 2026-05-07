import argparse
import os
import sys

from estimator import set_verbose


def _check_api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="estimate",
        description="Estimate task effort using t-shirt sizes (XS/S/M/L/XL/XXL).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Emit debug logs to stderr",
    )

    subparsers = parser.add_subparsers(dest="command")

    # estimate <description> subcommand
    estimate_parser = subparsers.add_parser(
        "estimate",
        help="Estimate effort for a single task description",
    )
    estimate_parser.add_argument(
        "description",
        nargs="?",
        help="Task description (reads from stdin if omitted)",
    )
    estimate_parser.add_argument(
        "--batch",
        metavar="FILE",
        help="Path to a file with one task description per line",
    )

    # sizes subcommand
    sizes_parser = subparsers.add_parser(
        "sizes",
        help="Display definitions for all t-shirt sizes",
    )
    sizes_parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    set_verbose(args.verbose)

    if args.command == "sizes":
        _cmd_sizes(args)
    elif args.command == "estimate":
        _check_api_key()
        if args.batch:
            _cmd_batch(args)
        else:
            _cmd_estimate(args)
    else:
        # Default: treat positional args as description for convenience
        parser.print_help()
        sys.exit(0)


def _cmd_estimate(args: argparse.Namespace) -> None:
    from estimator.estimator import estimate_task
    from estimator.formatter import format_result
    from estimator.models import EstimationRequest, EstimationError

    description = args.description
    if not description:
        if not sys.stdin.isatty():
            description = sys.stdin.read().strip()
        if not description:
            print("Error: Task description must not be empty.", file=sys.stderr)
            sys.exit(1)

    try:
        request = EstimationRequest(description=description)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    result = estimate_task(request)
    if isinstance(result, EstimationError):
        print(f"Error: {result.message}", file=sys.stderr)
        sys.exit(2)

    print(format_result(result, fmt=args.format))


def _cmd_batch(args: argparse.Namespace) -> None:
    from estimator.estimator import estimate_batch
    from estimator.formatter import format_batch_result
    from estimator.models import BatchEstimationRequest, EstimationRequest

    try:
        with open(args.batch, encoding="utf-8") as fh:
            lines = fh.readlines()
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    tasks = []
    for line in lines:
        stripped = line.strip()
        try:
            tasks.append(EstimationRequest(description=stripped))
        except ValueError:
            tasks.append(None)

    try:
        batch_req = BatchEstimationRequest(tasks=[t for t in tasks if t is not None])
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    batch_result = estimate_batch(batch_req, raw_lines=lines)
    print(format_batch_result(batch_result, fmt=args.format))


def _cmd_sizes(args: argparse.Namespace) -> None:
    from estimator.formatter import format_sizes
    print(format_sizes(fmt=args.format))
