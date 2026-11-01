# Archived rig checks

These scripts describe the old skeletal rig, old pose sheets, low held-weapon poses,
or source-texture/landmark measurements superseded by rendered full-layer ablation.
They are preserved for history and excluded from the active test runner. They are
not evidence that the current Lv1 poses pass.

Active checks remain in `prototype/tests/` and the current Python/render pipeline
in `tools/`. `tools/print_frame_placement.gd` prints numeric placement only and is
deliberately outside the test count.

The v8 front-chest hand scope and v9 bow-only immutable-body scope were superseded
by the explicit per-frame reference-placement request. `check_held_scope_v8.py`
and `check_bow_scope_v9.py` remain historical; current scope/placement checks
are `tools/check_held_scope_v10.py`, `tools/check_held_reference_v10.py` and the
Godot `held_reference_placement_checks.gd` suite.
