bind \e\\ __llm_cmdcomp

function __llm_cmdcomp -d "Fill in the command using an LLM"
  set __llm_oldcmd (commandline -b)
  set __llm_cursor_pos (commandline -C)
  echo # Start the program on a blank line
  set result (llm cmdcomp $__llm_oldcmd)
  if test $status -eq 0
    commandline -r $result
    echo # Move down a line to prevent fish from overwriting the program output
  end
  commandline -f repaint
end
