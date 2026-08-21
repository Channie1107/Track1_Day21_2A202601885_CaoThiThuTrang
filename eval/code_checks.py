"""Các kiểm tra xác định cho output của AI Tutor.

Mỗi hàm ``check_*`` trả về ``(passed: bool, rationale: str)``. Các hàm nhận
JSON đã parse, JSON string hoặc một row có field ``output``.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Mapping

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tutor"))
import tutor  # noqa: E402


# README.md định nghĩa contract sản phẩm, bao gồm cả scope.
REQUIRED_KEYS = frozenset({"scope", "answer", "sources", "followup_questions"})
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def _output(value: Any) -> tuple[Any, str | None]:
    """Lấy output object và rationale lỗi nếu có."""
    if isinstance(value, Mapping) and "output" in value:
        value = value["output"]
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            return None, f"JSON không hợp lệ: {exc.msg}"
    if isinstance(value, Mapping) and value.get("_parse_error"):
        return None, "JSON không parse được (xem raw_content)"
    return value, None


def check_schema_valid(value: Any) -> tuple[bool, str]:
    """Kiểm tra JSON hợp lệ, là object và có đủ key bắt buộc."""
    output, error = _output(value)
    if error:
        return False, error
    if not isinstance(output, Mapping):
        return False, "output phải là một JSON object"
    missing = REQUIRED_KEYS - set(output)
    if missing:
        return False, "thiếu field: " + ", ".join(sorted(missing))
    return True, "JSON hợp lệ và có đủ required keys"


def check_citation_exists(
    value: Any, valid_ids: set[tuple[str, str]] | None = None
) -> tuple[bool, str]:
    """Kiểm tra citation với manifest hoặc định dạng mock nghiêm ngặt."""
    output, error = _output(value)
    if error:
        return False, error
    if not isinstance(output, Mapping):
        return False, "không thể kiểm tra citation: output không phải object"
    sources = output.get("sources")
    if not isinstance(sources, list):
        return False, "sources phải là một JSON array"
    for index, source in enumerate(sources):
        if not isinstance(source, Mapping):
            return False, f"source thứ {index} không phải object"
        doc_id, section_id = source.get("doc_id"), source.get("section_id")
        if not isinstance(doc_id, str) or not isinstance(section_id, str):
            return False, f"source thứ {index} thiếu doc_id hoặc section_id"
        if valid_ids is not None:
            if (doc_id, section_id) not in valid_ids:
                return False, f"citation không tồn tại: {doc_id}#{section_id}"
        elif not ID_PATTERN.fullmatch(doc_id) or not ID_PATTERN.fullmatch(section_id):
            return False, f"citation có định dạng không hợp lệ: {doc_id}#{section_id}"
    return True, "tất cả citation đều tồn tại hoặc khớp định dạng manifest"


def check_quote_verbatim(
    value: Any, section_text: Mapping[tuple[str, str], str]
) -> tuple[bool, str]:
    """Kiểm tra quote không rỗng và là substring nguyên văn của section."""
    output, error = _output(value)
    if error:
        return False, error
    if not isinstance(output, Mapping):
        return False, "không thể kiểm tra quote: output không phải object"
    sources = output.get("sources")
    if not isinstance(sources, list):
        return False, "sources phải là một JSON array"
    for index, source in enumerate(sources):
        if not isinstance(source, Mapping):
            return False, f"source thứ {index} không phải object"
        key = (source.get("doc_id"), source.get("section_id"))
        quote = source.get("quote")
        text = section_text.get(key)
        if not isinstance(quote, str) or not quote:
            return False, f"source thứ {index} thiếu quote không rỗng"
        if not isinstance(text, str):
            return False, f"không tìm thấy section text cho {key[0]}#{key[1]}"
        if quote not in text:
            return False, f"quote không phải substring nguyên văn của {key[0]}#{key[1]}"
    return True, "mọi quote đều là substring nguyên văn của section đã cite"


# Tên tương thích ngược với runner hiện tại.
check_schema = check_schema_valid


def main(path: str = "results.jsonl") -> None:
    if not os.path.exists(path):
        raise SystemExit(f"Không thấy {path} — chạy eval/run_eval.py trước.")
    with open(path, encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]

    sections = tutor.load_corpus()
    valid_ids = {(s["doc_id"], s["section_id"]) for s in sections}
    section_text = {(s["doc_id"], s["section_id"]): s["text"] for s in sections}
    checks = (
        ("schema_valid", lambda row: check_schema_valid(row)),
        ("citation_exists", lambda row: check_citation_exists(row, valid_ids)),
        ("quote_verbatim", lambda row: check_quote_verbatim(row, section_text)),
    )
    totals = {name: [0, 0] for name, _ in checks}
    for row in rows:
        results = []
        for name, check in checks:
            passed, rationale = check(row)
            totals[name][0 if passed else 1] += 1
            results.append(f"{name}: {'pass' if passed else 'FAIL'} — {rationale}")
        print(f"{row.get('scenario_id', '?')} | " + " | ".join(results))

    print("\nTổng kết:")
    for name, (passed, failed) in totals.items():
        print(f"  {name}: {passed} pass / {failed} fail")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results.jsonl")
