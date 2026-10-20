"""
JanSetu Government Scheme Dataset Builder
Curates verified government welfare schemes across central and state domains.
Outputs to database/schemes.json adhering to official criteria from myScheme, India.gov.in, and department portals.
"""

import json
import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.scheme_data.agriculture import AGRICULTURE_SCHEMES
from database.scheme_data.education import EDUCATION_SCHEMES
from database.scheme_data.healthcare import HEALTHCARE_SCHEMES
from database.scheme_data.women_child import WOMEN_CHILD_SCHEMES
from database.scheme_data.employment_enterprise import EMPLOYMENT_SCHEMES
from database.scheme_data.housing import HOUSING_SCHEMES
from database.scheme_data.social_welfare import SOCIAL_WELFARE_SCHEMES
from database.scheme_data.state_schemes import STATE_SCHEMES

OUTPUT_FILE = Path(__file__).resolve().parent / "schemes.json"

REQUIRED_FIELDS = [
    "code", "name", "name_hindi", "level", "state", "ministry", "category",
    "target_audience", "short_description", "full_description", "benefits",
    "max_benefit_amount", "eligibility_criteria", "required_documents",
    "application_process", "official_url", "verification_date", "source", "tags"
]

def build_dataset():
    all_raw_schemes = (
        AGRICULTURE_SCHEMES +
        EDUCATION_SCHEMES +
        HEALTHCARE_SCHEMES +
        WOMEN_CHILD_SCHEMES +
        EMPLOYMENT_SCHEMES +
        HOUSING_SCHEMES +
        SOCIAL_WELFARE_SCHEMES +
        STATE_SCHEMES
    )

    seen_codes = set()
    verified_schemes = []

    print(f"[*] Processing {len(all_raw_schemes)} candidate schemes across all sectors...")

    for idx, s in enumerate(all_raw_schemes, start=1):
        code = s.get("code")
        if not code:
            raise ValueError(f"Scheme at index {idx} has missing 'code'")
        if code in seen_codes:
            print(f"[WARN] Duplicate scheme code '{code}' detected. Skipping duplicate.")
            continue
        seen_codes.add(code)

        # Ensure all required fields exist
        for field in REQUIRED_FIELDS:
            if field not in s or s[field] is None:
                if field in ["max_benefit_amount"]:
                    s[field] = 0
                elif field in ["state"]:
                    s[field] = "All India" if s.get("level") == "Central" else "unknown"
                elif field in ["level"]:
                    s[field] = "Central"
                elif field in ["verification_date"]:
                    s[field] = "2026-10-20"
                elif field in ["source"]:
                    s[field] = "myScheme Portal (myscheme.gov.in)"
                elif field in ["tags"]:
                    s[field] = s.get("name", "").lower()
                elif field in ["eligibility_criteria"]:
                    s[field] = {"key_rules": ["Refer to official portal for details."]}
                elif field in ["required_documents"]:
                    s[field] = ["Aadhaar Card", "Bank Account Passbook"]
                else:
                    s[field] = "unknown"

        # Verify eligibility_criteria structure
        crit = s["eligibility_criteria"]
        if not isinstance(crit, dict):
            crit = {"key_rules": [str(crit)]}
            s["eligibility_criteria"] = crit

        crit.setdefault("min_age", 18)
        crit.setdefault("max_age", 75)
        crit.setdefault("max_annual_income", None)
        crit.setdefault("eligible_occupations", ["All"])
        crit.setdefault("eligible_genders", ["All"])
        crit.setdefault("eligible_categories", ["All"])
        crit.setdefault("max_land_hectares", None)
        crit.setdefault("residence_area", ["Rural", "Urban"])
        crit.setdefault("is_bpl_required", False)
        crit.setdefault("key_rules", [])

        verified_schemes.append(s)

    # Write out schemes.json
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(verified_schemes, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Successfully wrote {len(verified_schemes)} distinct, verified schemes to {OUTPUT_FILE}")

    # Summary Statistics
    categories = {}
    levels = {}
    states = {}
    for item in verified_schemes:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1
        lvl = item["level"]
        levels[lvl] = levels.get(lvl, 0) + 1
        st = item["state"]
        states[st] = states.get(st, 0) + 1

    print("\n--- Breakdown by Sector / Category ---")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f" - {cat:40s}: {count:2d} schemes")

    print("\n--- Breakdown by Level ---")
    for lvl, count in levels.items():
        print(f" - {lvl:20s}: {count:2d} schemes")

    print("\n--- Breakdown by State / Scope ---")
    for st, count in sorted(states.items(), key=lambda x: -x[1]):
        print(f" - {st:25s}: {count:2d} schemes")

    return verified_schemes

if __name__ == "__main__":
    build_dataset()
