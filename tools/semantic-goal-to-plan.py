#!/usr/bin/env python3
import argparse
import json
import re

HIGH_IMPACT = {"deploy", "deployment", "production", "merge", "database", "migration", "delete", "secret", "credential", "permission", "डिप्लॉय", "तैनात", "प्रोडक्शन", "उत्पादन", "मर्ज", "डेटाबेस", "माइग्रेशन", "डिलीट", "हटाओ", "मिटाओ", "गुप्त", "क्रेडेंशियल", "अनुमति"}
SECURITY_TERMS = {"security", "auth", "authentication", "authorization", "credential", "secret", "सुरक्षा", "क्रेडेंशियल", "गुप्त"}
MUTATING_IMPACTS = {"LOW_IMPACT_MUTATION", "HIGH_IMPACT_MUTATION", "PRODUCTION_OR_DESTRUCTIVE"}
READ_ONLY_PREFIXES = ("inspect ", "read ", "list ", "show ", "examine ", "view ")
READ_ONLY_TERMS = ("जांचो", "जाँचो", "देखो", "पढ़ो", "सूची")
NON_MATERIAL_GATING_ANNOTATIONS = {"HIGH_IMPACT_REQUIRES_AUTHORIZATION_CHECK"}
CONSTRAINT_TERMS = {
    "DO_NOT_DEPLOY": ("deploy", "deployment", "डिप्लॉय", "तैनात"),
    "DO_NOT_PRODUCTION": ("production", "प्रोडक्शन", "उत्पादन"),
    "DO_NOT_MERGE": ("merge", "मर्ज"),
    "DO_NOT_DATABASE": ("database", "डेटाबेस"),
    "DO_NOT_MIGRATION": ("migration", "माइग्रेशन"),
    "DO_NOT_DELETE": ("delete", "डिलीट", "हटाओ", "मिटाओ"),
    "DO_NOT_SECRET": ("secret", "गुप्त"),
    "DO_NOT_CREDENTIAL": ("credential", "क्रेडेंशियल"),
    "DO_NOT_PERMISSION": ("permission", "अनुमति"),
}


def classify(text: str) -> str:
    t = text.casefold().strip()
    # Security-sensitive reads remain gated, but ordinary inspection is read-only
    # even when the subject contains mutation words such as update/deploy/database.
    if any(term in t for term in SECURITY_TERMS):
        return "SECURITY_SENSITIVE"
    if t.startswith(READ_ONLY_PREFIXES) or any(term in t for term in READ_ONLY_TERMS):
        return "READ_ONLY"
    if any(term in t for term in ("delete", "production", "deploy", "डिलीट", "हटाओ", "मिटाओ", "प्रोडक्शन", "उत्पादन", "डिप्लॉय", "तैनात")):
        return "PRODUCTION_OR_DESTRUCTIVE"
    if any(term in t for term in HIGH_IMPACT):
        return "HIGH_IMPACT_MUTATION"
    if any(term in t for term in ("change", "fix", "add", "update", "implement", "write", "create")):
        return "LOW_IMPACT_MUTATION"
    return "READ_ONLY"


def expand_read_before_write(phrases: list[str]) -> list[str]:
    expanded: list[str] = []
    for phrase in phrases:
        impact = classify(phrase)
        previous_is_read_only = bool(expanded) and classify(expanded[-1]) == "READ_ONLY"
        if impact in MUTATING_IMPACTS and not previous_is_read_only:
            expanded.append(f"inspect current repository state relevant to: {phrase}")
        expanded.append(phrase)
    return expanded


def _negative_constraint_conflict(steps: list[dict], constraints: list[str]) -> str | None:
    for constraint in constraints:
        terms = CONSTRAINT_TERMS.get(constraint)
        if not terms:
            continue
        for step in steps:
            # Ordinary read-before-write inspection does not itself violate a
            # mutation prohibition. Security/secret constraints remain gated by
            # their own classification and downstream Security Gate.
            if step["impact"] == "READ_ONLY":
                continue
            if any(term in step["objective"].casefold() for term in terms):
                return f"compiled step conflicts with explicit negative constraint {constraint}"
    return None


def compile_plan(intent: str, objective: str, project: str | None, constraints: list[str], ambiguity: list[str]) -> dict:
    annotations = sorted({
        a.strip() for a in ambiguity
        if a.strip() in NON_MATERIAL_GATING_ANNOTATIONS
    })
    material_ambiguity = [
        a.strip() for a in ambiguity
        if a.strip() and a.strip() not in NON_MATERIAL_GATING_ANNOTATIONS
    ]
    if not project:
        material_ambiguity.append("project unresolved")
    if not objective.strip():
        material_ambiguity.append("objective unresolved")

    if material_ambiguity:
        return {
            "protocol": "DEVOS-GOAL-PLAN-v1",
            "objective": objective or None,
            "project": project,
            "steps": [],
            "dependencies": [],
            "constraints": constraints,
            "assumptions": [],
            "ambiguity": sorted(set(material_ambiguity)),
            "gating_annotations": annotations,
            "authority_requirements": [],
            "verification_requirements": [],
            "decision": "CLARIFY",
            "authorization": "UNCHANGED",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }

    phrases = [p.strip() for p in re.split(r"\b(?:then|and then|after that|phir)\b|;", objective, flags=re.I) if p.strip()]
    if not phrases:
        phrases = [objective.strip()]
    phrases = expand_read_before_write(phrases)

    steps = []
    authority_requirements = []
    verification_requirements = []
    dependencies = []

    for i, phrase in enumerate(phrases, 1):
        sid = f"S{i}"
        deps = [f"S{i-1}"] if i > 1 else []
        impact = classify(phrase)
        requires_auth = impact in {"HIGH_IMPACT_MUTATION", "SECURITY_SENSITIVE", "PRODUCTION_OR_DESTRUCTIVE"}
        verification = "fresh evidence of stated outcome"
        if impact != "READ_ONLY":
            verification = "fresh applicable test/check plus observed resulting state"
        step = {
            "id": sid,
            "objective": phrase,
            "depends_on": deps,
            "expected_evidence": ["repository/source/runtime evidence appropriate to the step"],
            "impact": impact,
            "authorization_required": requires_auth,
            "verification": verification,
            "stop_or_escalate_if": "material ambiguity, missing capability, missing authorization, failed verification, or repository state conflict",
        }
        steps.append(step)
        for dep in deps:
            dependencies.append({"from": dep, "to": sid})
        if requires_auth:
            authority_requirements.append({"step": sid, "requirement": "independent authorization/Security Gate check"})
        verification_requirements.append({"step": sid, "requirement": verification})

    constraint_conflict = _negative_constraint_conflict(steps, constraints)
    if constraint_conflict:
        return {
            "protocol": "DEVOS-GOAL-PLAN-v1",
            "objective": objective,
            "project": project,
            "steps": steps,
            "dependencies": dependencies,
            "constraints": constraints,
            "assumptions": [],
            "ambiguity": [],
            "gating_annotations": annotations,
            "authority_requirements": authority_requirements,
            "verification_requirements": verification_requirements,
            "decision": "BLOCKED",
            "blockers": [constraint_conflict],
            "authorization": "UNCHANGED",
            "authority": "UNCHANGED",
            "execution": "NONE",
        }

    return {
        "protocol": "DEVOS-GOAL-PLAN-v1",
        "intent": intent,
        "objective": objective,
        "project": project,
        "steps": steps,
        "dependencies": dependencies,
        "constraints": constraints,
        "assumptions": [],
        "ambiguity": [],
        "gating_annotations": annotations,
        "authority_requirements": authority_requirements,
        "verification_requirements": verification_requirements,
        "decision": "PLANNED",
        "authorization": "UNCHANGED",
        "authority": "UNCHANGED",
        "execution": "NONE",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--intent", default="INVESTIGATE")
    p.add_argument("--objective", required=True)
    p.add_argument("--project")
    p.add_argument("--constraints", default="[]", help="JSON list")
    p.add_argument("--ambiguity", default="[]", help="JSON list")
    args = p.parse_args()
    print(json.dumps(compile_plan(args.intent, args.objective, args.project, json.loads(args.constraints), json.loads(args.ambiguity)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
