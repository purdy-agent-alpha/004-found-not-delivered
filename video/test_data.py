"""The counts the video shows are the report's (no Manim needed)."""
import data


def test_runtime_counts():
    assert data.TOTAL_RUNS == 72 == data.REQUESTS * data.SAMPLES * 2
    assert (data.OLD["read_phone"], data.OLD["first_served"], data.NEW["first_served"]) == (34, 0, 34)
    assert (data.OLD["too_long"], data.NEW["too_long"]) == (8, 0)
    assert (data.OLD["shell_read"], data.OLD["route"], data.NEW["route"]) == (19, 14, 35)
    assert (data.OLD["brief_route"], data.OLD["delegated"]) == (6, 19)
    assert (data.NEW["brief_route"], data.NEW["delegated"]) == (17, 17)
    assert data.OLD["cost"] + data.NEW["cost"] == 0.42


def test_limits_and_production():
    assert data.SERVED_CHARS < data.BUDGET_CHARS < data.REFUSED_CHARS < data.OLD_SKILL_BYTES
    assert data.NEW_CORE_BYTES < data.SIZE_CAP_BYTES < data.BUDGET_CHARS
    assert len(data.REFUSED_READS) == 4 and data.SKILL_READS == 52
