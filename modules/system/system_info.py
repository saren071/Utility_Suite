"""
System Info feature.

Purpose:
- Return an overview of machine hardware and OS: CPU model, cores, RAM, disks, GPU names, OS version.

API:
- run(args: dict = None, ctx: dict = None) -> dict
    - args typically unused; return structure is the data dict.

Implementation notes:
- Use utils.system_info helper functions.
- Return data for GUI/CLI formatting; do not print.

Dependencies:
- Internal: utils.system_info, utils.formatting, utils.logger
"""
