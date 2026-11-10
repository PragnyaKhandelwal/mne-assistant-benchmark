Assistant: ChatGPT (web)
Model: not shown in the free UI
Plan: free, logged in
Mode: Temporary Chat, new chat per question, Think off, no custom instructions
Dates: 2026-11-10 to 2026-11-1x

q001-q010 were redone with a fresh temporary chat per question, replacing an earlier
logged-out / shared-chat run (kept in git history, commit 8cfac01).
The web copy loses line breaks inside code blocks; `<id>.code.py` files restore them
without changing any statement. Where a reply recommends one of several blocks, that
block is selected (e.g. q002 "Recommended for dSPM"); q007 is run as written, all blocks
in order. Plotting/inspection blocks are not run.
