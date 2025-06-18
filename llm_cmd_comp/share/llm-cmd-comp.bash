# Bind Alt+\ to the LLM command completion
bind -x '"\e\\": __llm_cmdcomp'

__llm_cmdcomp() {
    # Store the current command line
    local old_cmd="${READLINE_LINE}"
    local cursor_pos="${READLINE_POINT}"
    local result
    
    # Move to a new line
    echo
    
    # Get the LLM completion
    if result="$(llm cmdcomp "${old_cmd}")"; then
        # Replace the command line with the result
        READLINE_LINE="${result}"
        READLINE_POINT="${#result}"
        # Move down a line to prevent bash from overwriting output
        echo
    else
        # Restore original command on error
        READLINE_LINE="${old_cmd}"
        READLINE_POINT="${cursor_pos}"
        echo "Command completion failed" >&2
    fi
}
