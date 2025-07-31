from argparse import HelpFormatter
from colorama import Fore, Style

class ColorHelpFormatter(HelpFormatter):
    """Custom formatter to colorize argparse help output."""
    def __init__(self, prog):
        super().__init__(prog, max_help_position=40, width=100)

    def start_section(self, heading):
        heading = f"{Fore.GREEN}{Style.BRIGHT}{heading.upper()}{Style.RESET_ALL}"
        super().start_section(heading)

    def _format_action_invocation(self, action):
        # Color argument names
        if not action.option_strings:
            return super()._format_action_invocation(action)
        return f"{Fore.YELLOW}{', '.join(action.option_strings)}{Style.RESET_ALL}"

    def _metavar_formatter(self, action, default_metavar):
        # Color metavariables (e.g., FILE)
        formatter = super()._metavar_formatter(action, default_metavar)
        return lambda tuple_size: tuple(
            f"{Fore.MAGENTA}{m}{Style.RESET_ALL}" for m in formatter(tuple_size)
        )
