from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import (
    change_applier,
    lesson_plan_builder,
    lesson_plan_contracts,
    notebook_builder,
    ppt_designer,
    ppt_script_sync,
    release_packager,
    run_state as run_state_tool,
)


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping YAML: {path}")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply a confirmed teacher change and regenerate affected artifacts.")
    parser.add_argument("--chapter", required=True, help="Chapter id.")
    parser.add_argument("--run-id", required=True, help="Run id under outputs/runs/<chapter>/<run_id>.")
    parser.add_argument("--request", required=True, help="Path to change_request.yaml")
    parser.add_argument("--confirmation", required=True, help="Path to change_confirmation.yaml")
    parser.add_argument("--output", default="outputs/runs", help="Run output root.")
    parser.add_argument(
        "--reuse-existing-ppt-script",
        action="store_true",
        help="Allow PPT regeneration from the existing source_bundle/ppt_script.yaml even if lesson_plan changed.",
    )
    return parser.parse_args()


def require_confirmation(request: dict, confirmation: dict) -> None:
    if confirmation.get("request_id") != request.get("request_id"):
        raise ValueError("confirmation.request_id does not match change request")
    if confirmation.get("run_id") != request.get("run_id"):
        raise ValueError("confirmation.run_id does not match change request")
    if not confirmation.get("summary_presented"):
        raise ValueError("change summary must be presented before confirmation")
    if not confirmation.get("approved"):
        raise ValueError("change was not approved")


def load_source_bundle(run_root: Path, chapter_id: str) -> dict[str, object]:
    bundle = run_root / "source_bundle"
    return {
        "bundle": bundle,
        "course": load_yaml(bundle / "course.yaml"),
        "chapter": load_yaml(bundle / f"chapter_{chapter_id}.yaml"),
        "good_lesson": load_yaml(bundle / "good_lesson.yaml"),
        "visual_ppt": load_yaml(bundle / "visual_ppt.yaml"),
        "lesson_plan": bundle / "lesson_plan.yaml",
        "legacy_lesson_plan": bundle / "legacy_lesson_plan.yaml",
        "lesson_plan_bridge": load_yaml(bundle / "lesson_plan_bridge.yaml"),
        "ppt_script": bundle / "ppt_script.yaml",
        "teacher_profile": (bundle / "teacher_profile.md").read_text(encoding="utf-8"),
    }


def main() -> None:
    args = parse_args()
    run_root = ROOT / args.output / args.chapter / args.run_id
    if not run_root.exists():
        raise SystemExit(f"Run root does not exist: {run_root}")

    request = load_yaml(Path(args.request))
    confirmation = load_yaml(Path(args.confirmation))
    require_confirmation(request, confirmation)

    summary_lines = change_applier.build_change_summary(request)
    change_applier.write_change_summary(summary_lines, run_root / "review" / "summary" / "change_summary.md")

    bundle = load_source_bundle(run_root, args.chapter)
    lesson_plan_path = bundle["lesson_plan"]
    legacy_lesson_plan_path = bundle["legacy_lesson_plan"]
    override_path = bundle["bundle"] / "override.yaml"
    override_history_path = bundle["bundle"] / "override_history.yaml"

    run_state_path = run_root / "runtime" / "run_state.yaml"
    current_state = run_state_tool.read_run_state(run_state_path)
    current_state["status"] = "regenerating"
    current_state["updated_at"] = run_state_tool.utc_now_iso()
    run_state_tool.write_run_state(current_state, run_state_path)
    try:
        updated_structured_lesson_plan = change_applier.apply_field_changes(
            lesson_plan_path,
            request.get("proposed_changes", []),
            output_path=lesson_plan_path,
        )
        legacy_lesson_plan = load_yaml(legacy_lesson_plan_path)
        updated_lesson_plan = lesson_plan_contracts.structured_to_legacy(
            updated_structured_lesson_plan,
            legacy_template=legacy_lesson_plan,
            bridge=bundle["lesson_plan_bridge"],
        )
        legacy_lesson_plan_path.write_text(
            yaml.safe_dump(updated_lesson_plan, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        override_doc = change_applier.build_override_document(request)
        override_path.write_text(yaml.safe_dump(override_doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
        change_applier.append_override_history(request, override_history_path)

        regen_scope = confirmation["regen_scope"]

        lesson_plan_builder.build_docx(
            bundle["course"],
            bundle["chapter"],
            updated_lesson_plan,
            bundle["good_lesson"],
            bundle["teacher_profile"],
            run_root / "docx" / "teaching_pack.docx",
        )
        lesson_plan_builder.write_quality_report(
            bundle["course"],
            bundle["chapter"],
            updated_lesson_plan,
            bundle["good_lesson"],
            run_root / "review" / "quality_check.md",
        )

        if regen_scope.get("regenerate_notebook"):
            notebook_builder.build_notebook(updated_lesson_plan, run_root / "ipynb" / f"{args.chapter}_lab.ipynb")

        ppt_regen_note = "PPT not regenerated."
        if regen_scope.get("regenerate_ppt"):
            ppt_script = load_yaml(bundle["ppt_script"])
            if args.reuse_existing_ppt_script:
                synced_ppt_script = ppt_script
                ppt_regen_note = "PPT re-rendered from the existing ppt_script without lesson-plan synchronization."
            else:
                synced_ppt_script = ppt_script_sync.sync_ppt_script_from_lesson_plan(
                    ppt_script,
                    updated_structured_lesson_plan,
                )
                ppt_script_sync.write_synced_ppt_script(synced_ppt_script, bundle["ppt_script"])
                ppt_regen_note = "PPT script synchronized from the updated structured lesson plan and re-rendered."
            ppt_designer.render_pptx(synced_ppt_script, bundle["visual_ppt"], run_root / "pptx" / f"{args.chapter}.pptx")
            ppt_designer.write_ppt_skill_report(synced_ppt_script, bundle["visual_ppt"], run_root / "pptx" / "ppt_skill_report.md")

        total_score = updated_lesson_plan["teacher_quality_review"]["total_score"]
        pass_threshold = updated_lesson_plan["teacher_quality_review"]["pass_threshold"]
        gate_passed = total_score >= pass_threshold

        teacher_summary_lines = release_packager.build_teacher_summary(
            chapter_title=updated_lesson_plan["lesson"]["title"],
            run_id=args.run_id,
            quality_verdict=updated_lesson_plan["teacher_quality_review"]["verdict"],
            total_score=total_score,
            output_paths={
                "pptx": run_root / "pptx" / f"{args.chapter}.pptx",
                "docx": run_root / "docx" / "teaching_pack.docx",
                "ipynb": run_root / "ipynb" / f"{args.chapter}_lab.ipynb",
                "review": run_root / "review" / "quality_check.md",
                "teacher_summary": run_root / "review" / "summary" / "teacher_summary.md",
            },
        )
        teacher_summary_lines.extend(["", "## Change Execution Notes", "", f"- {ppt_regen_note}"])
        release_packager.write_teacher_summary(teacher_summary_lines, run_root / "review" / "summary" / "teacher_summary.md")

        manifest = release_packager.build_release_manifest(
            run_id=args.run_id,
            chapter_id=args.chapter,
            output_paths={
                "pptx": run_root / "pptx" / f"{args.chapter}.pptx",
                "docx": run_root / "docx" / "teaching_pack.docx",
                "ipynb": run_root / "ipynb" / f"{args.chapter}_lab.ipynb",
                "teacher_summary": run_root / "review" / "summary" / "teacher_summary.md",
            },
            gate_passed=gate_passed,
        )
        release_packager.write_release_manifest(manifest, run_root / "release_manifest.yaml")

        final_state = run_state_tool.build_run_state(
            run_id=args.run_id,
            chapter_id=args.chapter,
            status="released" if gate_passed else "blocked",
            requested_outputs=current_state.get("requested_outputs", ["pptx", "docx", "ipynb"]),
            gate_passed=gate_passed,
            started_at=current_state.get("started_at"),
        )
        final_state["teacher_id"] = request.get("teacher_id", current_state.get("teacher_id", "unknown"))
        final_state["space_id"] = current_state.get("space_id", "default-course-space")
        final_state["artifacts"] = {
            "teacher_summary": str(run_root / "review" / "summary" / "teacher_summary.md"),
            "release_manifest": str(run_root / "release_manifest.yaml"),
            "override": str(override_path),
        }
        run_state_tool.write_run_state(final_state, run_state_path)

        print("Applied confirmed change and regenerated affected artifacts:")
        print(f"- run_root: {run_root}")
        print(f"- override: {override_path}")
        print(f"- teacher_summary: {run_root / 'review' / 'summary' / 'teacher_summary.md'}")
        print(f"- release_manifest: {run_root / 'release_manifest.yaml'}")
        print(f"- status: {final_state['status']}")
    except Exception:
        failed_state = dict(current_state)
        failed_state["status"] = "failed"
        failed_state["updated_at"] = run_state_tool.utc_now_iso()
        run_state_tool.write_run_state(failed_state, run_state_path)
        raise


if __name__ == "__main__":
    main()
