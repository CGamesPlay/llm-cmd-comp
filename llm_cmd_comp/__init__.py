import click
import platform
import os
import llm
import string
from prompt_toolkit import PromptSession
from prompt_toolkit.input import create_input
from prompt_toolkit.output import create_output

SYSTEM_PROMPT = string.Template(
    """Return only the command to be executed as a raw string, no string delimiters wrapping it, no yapping, no markdown, no fenced code blocks, what you return will be passed to the shell directly.
For example, if the user asks: undo last git commit
You return only: git reset --soft HEAD~1
The shell is $shell on $platform
""".strip()
)


@llm.hookimpl
def register_commands(cli):
    @cli.command()
    @click.option(
        "--init",
        type=click.Choice(["bash", "zsh", "fish"]),
        help="Output shell integration code for the specified shell and exit.",
    )
    @click.argument("args", nargs=-1)
    @click.option("-m", "--model", default=None, help="Specify the model to use")
    @click.option("-s", "--system", help="Custom system prompt")
    @click.option("--key", help="API key to use")
    def cmdcomp(init, args, model, system, key):
        """Generate commands directly in your command line (requires shell integration)
        Optionally output shell integration code with --init SHELL (bash, zsh, fish)
        """
        import sys
        from llm.cli import get_default_model

        if init:
            share_dir = os.path.join(os.path.dirname(__file__), "share")
            filename = f"llm-cmd-comp.{init}"
            filepath = os.path.join(share_dir, filename)
            if not os.path.exists(filepath):
                click.echo(f"Error: Integration file for {init} not found.", err=True)
                sys.exit(1)
            with open(filepath) as f:
                click.echo(f.read())
            return

        prompt = " ".join(args)
        model_id = model or get_default_model()
        model_obj = llm.get_model(model_id)
        if model_obj.needs_key:
            model_obj.key = llm.get_key(key, model_obj.needs_key, model_obj.key_env_var)
        conversation = model_obj.conversation()
        system = system or render_default_prompt()
        interactive_exec(conversation, prompt, system)


def render_default_prompt():
    return SYSTEM_PROMPT.substitute(
        shell=os.path.basename(os.getenv("SHELL") or "sh"), platform=platform.system()
    )


def interactive_exec(conversation, command, system):
    ttyin = create_input(always_prefer_tty=True)
    ttyout = create_output(always_prefer_tty=True)
    session = PromptSession(input=ttyin, output=ttyout)
    system = system or SYSTEM_PROMPT

    command = conversation.prompt(command, system=system)
    while True:
        ttyout.write("$ ")
        for chunk in command:
            ttyout.write(chunk.replace("\n", "\n> "))
        command = command.text()
        ttyout.write("\n# Provide revision instructions; leave blank to finish\n")
        feedback = session.prompt("> ")
        if feedback == "":
            break
        command = conversation.prompt(feedback, system=system)
    print(command)
