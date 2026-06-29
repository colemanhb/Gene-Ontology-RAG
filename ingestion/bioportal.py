import requests

API_KEY = "622683ad-2781-4efd-96b6-af9c82bf31d6"

HEADERS = {
    "Authorization": f"apikey token={API_KEY}"
}

ONTOLOGY_URL = "https://data.bioontology.org/ontologies"


def _safe_get(url):
    """Helper for optional follow-up API calls."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


def load_all_metadata(fetch_submissions: bool = True):
    """
    Load enriched ontology metadata from BioPortal.
    Optionally follows latest_submission for richer descriptions.
    """

    response = requests.get(ONTOLOGY_URL, headers=HEADERS, timeout=30)

    print("Got response:", response.status_code)

    response.raise_for_status()

    ontologies = []

    for o in response.json():
        latest = {}

        if fetch_submissions and o.get("links", {}).get("latest_submission"):
            latest = _safe_get(o["links"]["latest_submission"])

        ontologies.append({
            # identity
            "id": o.get("acronym", ""),
            "name": o.get("name", "") or o.get("title", ""),
            "ontology_type": o.get("ontologyType"),

            # descriptions (BioPortal is inconsistent here → merge both sources)
            "description": "\n\n".join(
                part for part in [
                    o.get("description"),
                    o.get("summary"),
                    o.get("notes"),
                ]
                if part
            ),

            # versioning / provenance
            "version": o.get("version"),
            "status": o.get("status"),
            "submitted_on": latest.get("submissionDate"),
            "contact": latest.get("contact"),
            "contact_email": latest.get("contactEmail"),

            # structure / semantics
            "categories": [
                c.get("acronym", "")
                for c in o.get("categories", [])
            ],
            "keywords": o.get("keywords", []),
            "has_views": o.get("viewOf"),
            "group": o.get("group"),

            # links (VERY useful context for LLM reasoning)
            "ui": o.get("links", {}).get("ui"),
        })

    return ontologies

def make_blob(o):
    """
    Build a high-information embedding document.
    """

    def join(x):
        if not x:
            return ""
        if isinstance(x, list):
            return ", ".join([str(i) for i in x if i])
        return str(x)

    return f"""
ONTOLOGY METADATA RECORD

Name:
{o.get("name", "")}

Acronym:
{o.get("id", "")}

Type:
{o.get("ontology_type", "")}

Status:
{o.get("status", "")}

Version:
{o.get("version", "")}

DESCRIPTION (BioPortal):
{o.get("description", "")}

DESCRIPTION (latest submission):
{o.get("summary", "")}

NOTES:
{o.get("notes", "")}

KEYWORDS:
{join(o.get("keywords", []))}

CATEGORIES:
{join(o.get("categories", []))}

GROUP / DOMAIN:
{o.get("group", "")}

PROVENANCE:
Submitted on: {o.get("submitted_on", "")}
Contact: {o.get("contact", "")}
Email: {o.get("contact_email", "")}
""".strip()