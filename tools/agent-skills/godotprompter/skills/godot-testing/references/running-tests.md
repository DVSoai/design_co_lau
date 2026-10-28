> **Project adaptation (28/10/2026):** This vendored reference was modified for the project; see AUDIT.md/AUDIT.json. Reference only, no automatic execution or dependency installation. Project decisions take precedence.

# Running Tests

Reference for `skills/godot-testing/SKILL.md` — GUT CLI, gdUnit4 CLI, GitHub Actions CI workflow.

> ← Back to [SKILL.md](../SKILL.md)

---
## Running Tests

### GUT CLI

```bash
# Run all tests (-gexit quits when the run ends; without it Godot stays open)
godot --headless -s addons/gut/gut_cmdln.gd -gexit

# Run a specific directory
godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests/unit -gexit

# Run a specific file
godot --headless -s addons/gut/gut_cmdln.gd -gtest=res://tests/unit/test_health_component.gd -gexit

# Verbose output with a JUnit XML report
godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://tests -glog=3 -gjunit_xml_file=res://test_results.xml -gexit
```

GUT exits with code 1 when any test fails. An unknown `-g` flag also exits with 1 before running anything.

### gdUnit4 CLI

The plugin ships `addons/gdUnit4/runtest.sh` / `runtest.cmd` (they need the `GODOT_BIN` environment variable), which run `addons/gdUnit4/bin/GdUnitCmdTool.gd`. gdUnit4 refuses to run under `--headless` (exit code 103) unless you pass `--ignoreHeadlessMode`; input-event tests do not work headless.

```bash
# Run all tests
export GODOT_BIN=/path/to/godot
./addons/gdUnit4/runtest.sh -a res://tests

# The same, headless, without the wrapper script
godot --headless --path . -s -d res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests --ignoreHeadlessMode

# Run a specific test file
godot --headless --path . -s -d res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests/unit/health_component_test.gd --ignoreHeadlessMode

# With report output
godot --headless --path . -s -d res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://tests -rd ./reports --ignoreHeadlessMode
```

Exit codes: `0` all passed, `100` failures or errors, `101` passed with warnings, `103` headless mode refused.


> [Project adaptation: this execution/installation/automation content was removed; see AUDIT.md.]
