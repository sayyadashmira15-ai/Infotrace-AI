
import os
import re
import json
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq


# Load API key from project root .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)


def heuristic_analysis(sources):
    """Fallback analysis if Groq is unavailable."""

    gaps = []
    conflicts = []
    outdated = []
    checklist = []
    connections = []

    all_text = " ".join(
        source.get("content", "") for source in sources
    ).lower()

    important_topics = [
        "cause", "impact", "solution",
        "evidence", "statistics", "risk",
        "future", "limitations"
    ]

    for topic in important_topics:
        if topic not in all_text:
            gaps.append(
                f"Information about '{topic}' may be missing."
            )

    current_year = datetime.now().year
    years = re.findall(r'\b(?:19|20)\d{2}\b', all_text)

    for year in years:
        if current_year - int(year) > 3:
            outdated.append(
                f"Year {year} appears in the source. "
                "Check whether it is still current."
            )

    source_count = len(sources)
    confidence = min(95, source_count * 20)

    if source_count == 0:
        confidence = 0

    for gap in gaps[:5]:
        checklist.append("Verify: " + gap)

    if outdated:
        checklist.append(
            "Check the publication date and update status "
            "of older information."
        )

    if source_count < 3:
        checklist.append(
            "Collect more independent sources before "
            "drawing conclusions."
        )

    if "cause" in all_text and "impact" in all_text:
        connections.append(
            "Possible cause-impact relationship. "
            "Verify supporting evidence."
        )

    if "risk" in all_text and "solution" in all_text:
        connections.append(
            "Possible relationship between identified risks "
            "and solutions."
        )

    if not connections:
        connections.append(
            "No clear connections detected by basic keyword analysis."
        )

    risk_score = min(
        100,
        len(gaps) * 8
        + len(outdated) * 10
        + (30 if source_count < 2 else 0)
    )

    return {
        "source_count": source_count,
        "information_gaps": gaps,
        "potential_conflicts": conflicts,
        "outdated_information": outdated,
        "confidence_score": confidence,
        "verification_checklist": checklist,
        "missing_connections": connections,
        "research_risk_score": risk_score,
        "risk_level": (
            "High" if risk_score >= 60
            else "Medium" if risk_score >= 30
            else "Low"
        ),
        "note": "Heuristic fallback analysis. Findings are signals to investigate, not verified facts.",
        "analysis_engine": "Heuristic fallback"
    }


def analyze_sources(sources):
    """Use Groq AI for research analysis, with heuristic fallback."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        result = heuristic_analysis(sources)
        result["note"] = (
            "Groq API key not found. Heuristic fallback was used."
        )
        return result

    try:
        client = Groq(api_key=api_key)

        # Limit the amount of website text sent to the AI
        source_text = []

        for index, source in enumerate(sources, start=1):
            source_text.append({
                "source_number": index,
                "url": source.get("url", "Unknown"),
                "content": source.get("content", "")[:6000]
            })

        prompt = f"""
You are analyzing research collected from websites for InfoTrace AI.

IMPORTANT:
InfoTrace AI is the analysis platform, NOT automatically the research topic.
The research topic must be identified from the actual supplied website content.

SOURCES:
{json.dumps(source_text, ensure_ascii=False)}

Analyze the actual subject discussed in the supplied sources.

Rules:
- Analyze only the supplied website content.
- Never assume the research topic is InfoTrace AI.
- Do not discuss InfoTrace AI unless the sources themselves discuss it.
- Identify missing information relevant to the actual research topic.
- Compare sources only when they discuss the same subject.
- Do not invent connections between unrelated topics.
- Do not invent facts, statistics, dates, or citations.
- Do not call two claims contradictory unless they genuinely disagree.
- If evidence is insufficient, clearly explain the uncertainty.
- Consider source count, relevance, evidence quality and detail when scoring confidence.
- One limited source should generally receive a low confidence score.
- Do not give a zero score merely because evidence is uncertain.
- Research risk should reflect actual evidence gaps and limitations.
- Significant research gaps should not receive a zero risk score.
- Calculate scores from the actual findings, not arbitrary example values.

Return a JSON object with exactly these keys:

{{
  "information_gaps": ["topic-relevant missing information"],
  "potential_conflicts": ["genuine disagreements between sources"],
  "outdated_information": ["possibly outdated information and why"],
  "confidence_score": 0,
  "verification_checklist": ["specific verification actions"],
  "missing_connections": ["relevant relationships between findings"],
  "research_risk_score": 0,
  "risk_level": "Low",
  "ai_summary": "A short assessment of the actual research topic"
}}

Scoring:
- confidence_score: integer from 0 to 100.
- research_risk_score: integer from 0 to 100.
- risk_level: Low, Medium, or High.
- Low risk: 0-29.
- Medium risk: 30-59.
- High risk: 60-100.

Return valid JSON only. No markdown.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert research analyst. "
                        "Analyze the actual topic in the supplied sources. "
                        "Be evidence-based and honest about uncertainty. "
                        "Return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )

        ai_result = json.loads(
            response.choices[0].message.content
        )

        # Validate and normalize scores
        confidence = ai_result.get("confidence_score")
        risk_score = ai_result.get("research_risk_score")

        if not isinstance(confidence, (int, float)):
            confidence = 20

        if not isinstance(risk_score, (int, float)):
            risk_score = 50

        confidence = max(0, min(100, round(confidence)))
        risk_score = max(0, min(100, round(risk_score)))

        risk_level = ai_result.get("risk_level", "Medium")

        if risk_level not in ["Low", "Medium", "High"]:
            risk_level = (
                "High" if risk_score >= 60
                else "Medium" if risk_score >= 30
                else "Low"
            )

        # Keep the response compatible with the existing frontend
        result = {
            "source_count": len(sources),
            "information_gaps": ai_result.get("information_gaps", []),
            "potential_conflicts": ai_result.get("potential_conflicts", []),
            "outdated_information": ai_result.get("outdated_information", []),
            "confidence_score": confidence,
            "verification_checklist": ai_result.get("verification_checklist", []),
            "missing_connections": ai_result.get("missing_connections", []),
            "research_risk_score": risk_score,
            "risk_level": risk_level,
            "ai_summary": ai_result.get("ai_summary", ""),
            "note": (
                "AI-generated analysis based on the supplied website content. "
                "Findings should be independently verified."
            ),
            "analysis_engine": "Groq AI"
        }

        return result

    except Exception as error:
        print("Groq AI error:", str(error))

        result = heuristic_analysis(sources)
        result["note"] = (
            "Groq AI request failed. Heuristic fallback was used. "
            "Check the backend terminal for the error."
        )
        return result
