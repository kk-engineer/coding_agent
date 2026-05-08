from pathlib import Path
from datetime import datetime
import shutil
import uuid

ROLLBACK_DIR = ".agent_backups"

Path(ROLLBACK_DIR).mkdir(exist_ok=True)


def backup_file(file_path):

    """
    Create backup before modification.
    """

    rollback_id = str(uuid.uuid4())

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    original = Path(file_path)

    backup_name = (
        f"{timestamp}_"
        f"{rollback_id}_"
        f"{original.name}"
    )

    backup_path = (
        Path(ROLLBACK_DIR)
        / backup_name
    )

    shutil.copy2(
        original,
        backup_path
    )

    return rollback_id, str(backup_path)


def rollback_file(
    backup_path,
    target_path
):

    """
    Restore backup file.
    """

    backup = Path(backup_path)

    target = Path(target_path)

    if not backup.exists():

        raise FileNotFoundError(
            f"Backup not found: {backup_path}"
        )

    shutil.copy2(
        backup,
        target
    )

    return {
        "success": True,
        "restored_file": str(target),
        "backup_used": str(backup)
    }


def delete_backup(
    backup_path
):

    """
    Optional cleanup utility.
    """

    backup = Path(backup_path)

    if backup.exists():

        backup.unlink()

        return True

    return False