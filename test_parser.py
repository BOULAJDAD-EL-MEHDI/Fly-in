"""
Ultimate parser stress tester for fly-in project.
Run from the root of your fly-in project:
    python3 test_parser.py
"""

import subprocess
import os
import tempfile
import sys

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
SECTION = "\033[96m\033[1m"
RESET = "\033[0m"

results = {"passed": 0, "failed": 0}


def run_map(content: str) -> tuple[int, str]:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as f:
        f.write(content)
        path = f.name
    result = subprocess.run(
        ["python3", "main.py", path],
        capture_output=True,
        text=True
    )
    os.unlink(path)
    return result.returncode, result.stdout + result.stderr


def expect_error(label: str, content: str) -> None:
    code, output = run_map(content)
    if code != 0:
        print(f"{PASS} {label}")
        results["passed"] += 1
    else:
        print(f"{FAIL} {label}")
        print(f"       Expected error but got exit 0")
        print(f"       Output: {output[:200]}")
        results["failed"] += 1


def expect_ok(label: str, content: str) -> None:
    code, output = run_map(content)
    if code == 0:
        print(f"{PASS} {label}")
        results["passed"] += 1
    else:
        print(f"{FAIL} {label}")
        print(f"       Expected success but got exit {code}")
        print(f"       Output: {output[:200]}")
        results["failed"] += 1


def section(title: str) -> None:
    print(f"\n{SECTION}{'=' * 55}")
    print(f"  {title}")
    print(f"{'=' * 55}{RESET}")


# ─────────────────────────────────────────────
section("1. NB_DRONES LINE")
# ─────────────────────────────────────────────

expect_error("Missing nb_drones entirely", """\
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("nb_drones is zero", """\
nb_drones: 0
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("nb_drones is negative", """\
nb_drones: -3
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("nb_drones is a float", """\
nb_drones: 2.5
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("nb_drones is a string", """\
nb_drones: two
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("nb_drones not on first line", """\
start_hub: hub 0 0
nb_drones: 2
end_hub: goal 10 10
connection: hub-goal
""")

expect_ok("nb_drones valid = 1", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_ok("nb_drones valid = 100", """\
nb_drones: 100
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

# ─────────────────────────────────────────────
section("2. START / END HUB")
# ─────────────────────────────────────────────

expect_error("Missing start_hub", """\
nb_drones: 2
end_hub: goal 10 10
hub: A 5 5
connection: A-goal
""")

expect_error("Missing end_hub", """\
nb_drones: 2
start_hub: hub 0 0
hub: A 5 5
connection: hub-A
""")

expect_error("Two start_hubs", """\
nb_drones: 2
start_hub: hub 0 0
start_hub: hub2 1 1
end_hub: goal 10 10
connection: hub-goal
connection: hub2-goal
""")

expect_error("Two end_hubs", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
end_hub: goal2 9 9
connection: hub-goal
connection: hub-goal2
""")

expect_error("start_hub and end_hub same zone", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: hub 0 0
""")

# ─────────────────────────────────────────────
section("3. ZONE NAMES")
# ─────────────────────────────────────────────

expect_error("Zone name with a dash", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: bad-name 5 5
connection: hub-goal
""")

expect_error("Zone name with a space", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: bad name 5 5
connection: hub-goal
""")

expect_error("Duplicate zone name", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
hub: A 3 3
connection: hub-A
connection: A-goal
""")

expect_error("Zone name same as start_hub", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: hub 5 5
connection: hub-goal
""")

# ─────────────────────────────────────────────
section("4. ZONE COORDINATES")
# ─────────────────────────────────────────────

expect_error("Zone coordinate is float", """\
nb_drones: 2
start_hub: hub 0.5 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("Zone coordinate is string", """\
nb_drones: 2
start_hub: hub zero 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("Zone missing Y coordinate", """\
nb_drones: 2
start_hub: hub 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("Zone missing both coordinates", """\
nb_drones: 2
start_hub: hub
end_hub: goal 10 10
connection: hub-goal
""")

# ─────────────────────────────────────────────
section("5. ZONE TYPES")
# ─────────────────────────────────────────────

expect_error("Invalid zone type", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=superfast]
connection: hub-A
connection: A-goal
""")

expect_error("Zone type is empty", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=]
connection: hub-A
connection: A-goal
""")

expect_ok("zone=normal is valid", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=normal]
connection: hub-A
connection: A-goal
""")

expect_ok("zone=restricted is valid", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=restricted]
connection: hub-A
connection: A-goal
""")

expect_ok("zone=priority is valid", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=priority]
connection: hub-A
connection: A-goal
""")

expect_ok("zone=blocked is valid (path exists around it)", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=blocked]
hub: B 3 3
connection: hub-A
connection: hub-B
connection: B-goal
""")

# ─────────────────────────────────────────────
section("6. MAX_DRONES CAPACITY")
# ─────────────────────────────────────────────

expect_error("max_drones is zero", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [max_drones=0]
connection: hub-A
connection: A-goal
""")

expect_error("max_drones is negative", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [max_drones=-1]
connection: hub-A
connection: A-goal
""")

expect_error("max_drones is float", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [max_drones=1.5]
connection: hub-A
connection: A-goal
""")

expect_error("max_drones is string", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [max_drones=many]
connection: hub-A
connection: A-goal
""")

expect_ok("max_drones=3 is valid", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [max_drones=3]
connection: hub-A
connection: A-goal
""")

# ─────────────────────────────────────────────
section("7. CONNECTIONS")
# ─────────────────────────────────────────────

expect_error("Connection to unknown zone", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-ghost
connection: ghost-goal
""")

expect_error("Connection from unknown zone", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
connection: ghost-goal
""")

expect_error("Duplicate connection a-b", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A
connection: hub-A
connection: A-goal
""")

expect_error("Duplicate connection b-a (reverse)", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A
connection: A-hub
connection: A-goal
""")

expect_error("Self-loop connection", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-hub
connection: hub-A
connection: A-goal
""")

expect_error("max_link_capacity is zero", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A [max_link_capacity=0]
connection: A-goal
""")

expect_error("max_link_capacity is negative", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A [max_link_capacity=-2]
connection: A-goal
""")

expect_error("max_link_capacity is float", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A [max_link_capacity=1.5]
connection: A-goal
""")

expect_error("max_link_capacity is string", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A [max_link_capacity=one]
connection: A-goal
""")

expect_ok("max_link_capacity=3 is valid", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A [max_link_capacity=3]
connection: A-goal
""")

# ─────────────────────────────────────────────
section("8. METADATA BLOCK SYNTAX")
# ─────────────────────────────────────────────

expect_error("Metadata block not closed", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=normal
connection: hub-A
connection: A-goal
""")

expect_error("Metadata block not opened", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 zone=normal]
connection: hub-A
connection: A-goal
""")

# expect_error("Unknown metadata key", """\
# nb_drones: 2
# start_hub: hub 0 0
# end_hub: goal 10 10
# hub: A 5 5 [zone=normal speed=fast]
# connection: hub-A
# connection: A-goal
# """)

# ─────────────────────────────────────────────
section("9. NO PATH EXISTS")
# ─────────────────────────────────────────────

expect_error("No path from start to end (all blocked)", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5 [zone=blocked]
connection: hub-A
connection: A-goal
""")

expect_error("Start and end not connected at all", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
hub: B 3 3
connection: hub-A
connection: B-goal
""")

# ─────────────────────────────────────────────
section("10. COMMENTS AND EMPTY LINES")
# ─────────────────────────────────────────────

expect_ok("Comments are ignored", """\
nb_drones: 1
# this is a comment
start_hub: hub 0 0
# another comment
end_hub: goal 10 10
connection: hub-goal
""")

expect_ok("Empty lines are ignored", """\
nb_drones: 1

start_hub: hub 0 0

end_hub: goal 10 10

connection: hub-goal
""")

# ─────────────────────────────────────────────
section("11. VALID COMPLETE MAPS")
# ─────────────────────────────────────────────

expect_ok("Minimal valid map", """\
nb_drones: 1
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_ok("Full metadata valid map", """\
nb_drones: 3
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: A 3 3 [zone=priority color=blue max_drones=2]
hub: B 6 6 [zone=restricted color=red]
connection: hub-A [max_link_capacity=2]
connection: A-B
connection: B-goal
""")

expect_ok("Tags in any order in metadata", """\
nb_drones: 1
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10
hub: A 5 5 [max_drones=2 color=blue zone=priority]
connection: hub-A
connection: A-goal
""")

# ─────────────────────────────────────────────
section("12. NASTY EDGE CASES")
# ─────────────────────────────────────────────

expect_error("Connection defined before zone", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-A
hub: A 5 5
connection: A-goal
""")

expect_error("Completely empty file", """\
""")

expect_error("Only comments", """\
# just a comment
# nothing else
""")

expect_error("nb_drones line has extra tokens", """\
nb_drones: 2 extra
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("Zone with negative coordinates and invalid type", """\
nb_drones: 2
start_hub: hub -1 -1
end_hub: goal 10 10
hub: A 5 5 [zone=flying]
connection: hub-A
connection: A-goal
""")

expect_ok("Negative coordinates are valid", """\
nb_drones: 1
start_hub: hub -5 -3
end_hub: goal 10 10
connection: hub-goal
""")

expect_error("Connection with three zones", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
hub: A 5 5
connection: hub-A-goal
""")

expect_error("Zone defined after connections that use it", """\
nb_drones: 2
start_hub: hub 0 0
end_hub: goal 10 10
connection: hub-A
connection: A-goal
hub: A 5 5
""")

# ─────────────────────────────────────────────
print(f"\n{'=' * 55}")
total = results['passed'] + results['failed']
print(f"Results: {results['passed']}/{total} passed", end="  ")
if results['failed'] == 0:
    print("\033[92mPERFECT PARSER\033[0m 🎯")
else:
    print(f"\033[91m{results['failed']} failures to fix\033[0m")
print('=' * 55)
