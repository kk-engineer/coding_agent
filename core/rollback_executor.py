from core.rollback_manager import rollback_file


def rollback_all(rollback_entries):

    for entry in rollback_entries:

        rollback_file(
            entry["backup_path"],
            entry["file"]
        )