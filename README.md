## TaskMaster - local development
==============================

## Prerequisites
-------------
- Python 3.10+ installed and on your PATH.
- Git (optional) if you cloned the repository.

Create and activate a virtual environment (Windows PowerShell)
```
python -m venv .venv
.
& ".\.venv\Scripts\Activate.ps1"
```

Install dependencies
--------------------
Install the required package (`flet`) into the activated virtual environment:
```
pip install flet
```

Run the app
----------
With the virtual environment activated run:
```
python main.py
```

## Select the correct Python interpreter (VS Code)
--------------------------------------------
If you use VS Code, make sure the editor is using the virtual environment's Python interpreter so debugging and run commands use the installed packages:

- Press `Ctrl+Shift+P` to open the Command Palette.
- Type `Python: Select Interpreter` and choose the entry that points to `.venv\Scripts\python.exe` (or `./.venv/bin/python` on WSL/macOS).
- Alternatively choose `Enter interpreter path...` and browse to the `.venv` interpreter.

This ensures `python main.py`, the debugger, and the language server use the same environment.

## Notes
-----
- If you use a different shell (cmd.exe or Bash) the activation command differs.
- On first run Flet will open a desktop window. If you prefer running in a browser see the Flet docs for `flet` CLI options.

