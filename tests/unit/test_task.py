from src.staffoptimizer.domain.model import Task, Status, Editor


def make_task_and_editor(ref, status, team, name, editor_id):
    return Task(ref, status, team), Editor(name, editor_id)


# def test_task_is_staffed():
#     task = ...
#     editor = ...
#     task.assign(editor)
#     assert task.staffed is True


def test_task_is_unallocated():
    task = Task("Vidéo d'Emma", Status.REVIEW_STAFFING.value, "Arts and Craft")
    editor = Editor("Medhi", "MB13")
    task.assign(editor)
    assert task.staffed is True
    task.unassign(editor)
    assert task.unallocated is True
