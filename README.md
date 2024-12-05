# Shell completion using LLM

Use LLM to generate and execute commands in your shell

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-cmd-comp
```
Then install the shell integration for your preferred shell.

- **Fish**: place `share/llm-cmd-comp.fish` in `~/.config/fish/conf.d/`.

## Usage

1. Start typing a command.
2. Activate the key binding (Alt-Backslash by default).
3. Wait for the LLM to complete the command.
4. Press enter if you are happy. Otherwise give feedback on the command and repeat from step 3.
5. The LLM's command replaces the previous command you were writing.

Neat ways you can use this feature:

- **Type a command in English, convert it to bash.**
  `find all files larger than 100MB`
  🪄 `find . -type f -size +100M`
- **Give extra instructions as comments.**
  `sed -i '' 's/search/replace/g' file.go # Now do it for all go files in the project`
  🪄 `find . -name '*.go' -exec sed -i '' 's/search/replace/g' {} +`

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-cmd
python3 -m venv venv
source venv/bin/activate
```

Now install the dependencies and test dependencies:

```bash
pip install llm
llm install -e .
```