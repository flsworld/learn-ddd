from src.staffoptimizer.domain.model import Task, Status, Editor


def make_task_and_editor(ref, status, team, name, editor_id):
    return Task(ref, status, team), Editor(name, editor_id)


def test_task_is_staffed():
    task = ...
    editor = ...
    task.assign(editor)
    assert task.staffed is True


def test_task_is_unallocated():
    task, editor = make_task_and_editor(
        "Vidéo d'Emma", Status.REVIEW_STAFFING.value, "Arts and Craft", "Medhi", "MB13"
    )
    task.unassign(editor)
    assert task.unallocated is True
