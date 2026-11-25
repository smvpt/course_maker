"""Общее для замечаний: схема организаторов — одно замечание на цель."""
SEV_ORDER = {"critical": 0, "significant": 1, "minor": 2}


def one_per_target(remarks):
    """Сливает замечания с одной целью; главное — самое тяжёлое, оно и идёт первым."""
    merged = {}
    for r in sorted(remarks, key=lambda r: SEV_ORDER[r.severity]):
        m = merged.get(r.target)
        if m is None:
            merged[r.target] = r.model_copy()
        else:
            m.problem += "; " + r.problem
            m.fix += "; " + r.fix
            if m.page_pdf is None:
                m.page_pdf = r.page_pdf
    first = {}
    for i, r in enumerate(remarks):
        first.setdefault(r.target, i)
    return sorted(merged.values(), key=lambda r: (SEV_ORDER[r.severity], first[r.target]))
