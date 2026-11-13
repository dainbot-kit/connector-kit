# Shortcut: "Make Skill" (dictation to reusable skill block)

Speak in labelled parts, get a clean skill/instruction block on your clipboard and saved as a text file. Deterministic: no model needed.

## How you speak
"Role: you're my coding helper. Task: review my Swift files. Rules: never delete anything, plain English. Output: a short checklist."

## Actions (in order)
1. **Dictate Text**: Language English (Australia); Stop Listening: After Pause.
2. **Match Text** x4 on the dictated text (one per part):
   - Role:   `(?i)role:?\s*(.*?)(?=task:|rules:|output:|$)`
   - Task:   `(?i)task:?\s*(.*?)(?=role:|rules:|output:|$)`
   - Rules:  `(?i)rules:?\s*(.*?)(?=role:|task:|output:|$)`
   - Output: `(?i)output:?\s*(.*?)(?=role:|task:|rules:|$)`
   Use **Get Group from Matched Text** (group 1) after each.
3. **Text** (template):
   ```
   ROLE: [Role]
   TASK: [Task]
   CONSTRAINTS: [Rules]
   OUTPUT FORMAT: [Output]
   ```
4. **Copy to Clipboard**.
5. **Save File**: to a folder you choose, filename `skill-[Current Date].txt`, Ask Where to Save off.
6. **Show Notification**: "Skill copied".

Optional free-talk mode: after step 1, add the Apple Intelligence model action with: "Rewrite this into Role, Task, Constraints, Output Format. Keep my exact meaning and add nothing." Runs on-device.

## Triggers
- Siri: "Hey Siri, Make Skill".
- Voice Control: System Settings > Accessibility > Voice Control > Commands > + ; phrase "capture this"; Perform: Run Shortcut > Make Skill.
- Keyboard: shortcut details > Add Keyboard Shortcut.

## Piping dictation into a script instead
Dictate Text -> **Run Shell Script** (Shell: zsh, Pass Input: to stdin), e.g. `cat >> ~/Documents/notes.txt` or `python3 ~/scripts/handle.py` (reads stdin).

## Permissions (first run)
Allow microphone/dictation for Shortcuts; enable Shortcuts > Settings > Advanced > Allow Running Scripts.

Note: steps written from macOS Shortcuts knowledge; not run on a Mac yet.
