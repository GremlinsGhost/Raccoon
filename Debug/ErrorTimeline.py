import traceback
import sys
import linecache

GENERAL_EXPLANATIONS = {
    "AttributeError": "This error occurs when you try to access a method or attribute that the object does not have.",
    "KeyError": "This error occurs when a dictionary lookup fails because the key does not exist.",
    "ModuleNotFoundError": "Python cannot find the requested module. The file may be missing or in a different directory.",
    "PermissionError": "The operating system blocked the operation. Usually the file is not executable.",
    "TypeError": "This error occurs when a function receives a value of the wrong type.",
    "ValueError": "This error occurs when a function receives a value of the correct type but an invalid value."
}

def explain_error(e, expected=None, received=None):
    notes = []

    # 1) WHAT THE PROGRAM WAS DOING
    tb = traceback.extract_tb(sys.exc_info()[2])
    notes.append("🔵 What the program was doing:")
    for frame in tb:
        notes.append(f" - {frame.name}() → {frame.filename}:{frame.lineno}")

    # 2) WHERE IT CRASHED
    last = tb[-1]
    code_line = linecache.getline(last.filename, last.lineno).strip()
    notes.append("\n🟥 Where it crashed:")
    notes.append(f"   {last.filename}:{last.lineno}")
    notes.append(f"   → {code_line}")

    # 3) WHAT THIS ERROR USUALLY MEANS
    err_type = e.__class__.__name__
    err_msg = str(e)

    notes.append("\n🟨 What this error usually means:")
    notes.append(f"   {err_type}: {err_msg}")

    if err_type in GENERAL_EXPLANATIONS:
        notes.append(f"   {GENERAL_EXPLANATIONS[err_type]}")

    # 4) POSSIBLE FIXES (GENERAL)
    notes.append("\n🟩 Possible fixes:")
    notes.append("   • Check the variable type before using it.")
    notes.append("   • Verify the data structure matches what the function expects.")
    notes.append("   • Inspect the code line and confirm the values are valid.")
    notes.append("   • Ensure the module/file paths are correct.")

    # 5) VALUE MISMATCH ANALYSIS
    if expected is not None or received is not None:
        notes.append("\n🟪 Value mismatch analysis:")
        notes.append(f"   Expected: {expected}")
        notes.append(f"   Received: {received}")
        notes.append("   → These values do not match the function's requirements.")

    # 6) ENVIRONMENT SANITY CHECKS
    notes.append("\n🟫 Environment sanity checks:")
    notes.append("   • Are you in the correct directory?")
    notes.append("   • Does the file exist?")
    notes.append("   • Did you mean a different filename?")
    notes.append("   • Is __init__.py missing?")
    notes.append("   • Is the module path correct?")

    return notes
