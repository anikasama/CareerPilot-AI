import re

from app.services.job_matcher import detect_skills


SECTION_PATTERNS = {
    "Projects": [
        r"\bprojects?\b",
        r"\bpersonal projects?\b",
        r"\bacademic projects?\b",
    ],
    "Experience": [
        r"\bexperience\b",
        r"\bwork experience\b",
        r"\binternship\b",
        r"\binternships\b",
    ],
    "Education": [
        r"\beducation\b",
        r"\bacademic background\b",
    ],
    "Achievements": [
        r"\bachievements?\b",
        r"\bawards?\b",
        r"\baccomplishments?\b",
    ],
    "Certifications": [
        r"\bcertifications?\b",
        r"\bcertificates?\b",
        r"\bcourses?\b",
    ],
}


def has_section(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def score_contact(text: str) -> tuple[int, list[str]]:
    score = 0
    suggestions = []

    email_found = bool(
        re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )
    )

    phone_found = bool(
        re.search(
            r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
            text,
        )
    )

    linkedin_found = "linkedin.com" in text.lower()
    github_found = "github.com" in text.lower()

    if email_found:
        score += 6
    else:
        suggestions.append("Add a professional email address.")

    if phone_found:
        score += 4
    else:
        suggestions.append("Add a valid phone number.")

    if linkedin_found:
        score += 3
    else:
        suggestions.append("Add your LinkedIn profile.")

    if github_found:
        score += 2
    else:
        suggestions.append(
            "Add GitHub if you have relevant technical projects."
        )

    return min(score, 15), suggestions


def score_length(word_count: int) -> tuple[int, list[str]]:
    if 350 <= word_count <= 1000:
        return 10, []

    if 250 <= word_count < 350:
        return 8, [
            "Your resume is slightly short. Add useful project "
            "or experience details."
        ]

    if 100 <= word_count < 250:
        return 5, [
            "Your resume is short. Add more detail about projects, "
            "skills, experience and achievements."
        ]

    if word_count > 1000:
        return 7, [
            "Your resume is longer than recommended. Remove "
            "repetitive or less relevant content."
        ]

    return 2, [
        "Your resume is too short. Add relevant technical and "
        "career details."
    ]


def score_skills(skills_found: list[str]) -> tuple[int, list[str]]:
    count = len(skills_found)

    if count >= 12:
        return 20, []

    if count >= 8:
        return 16, [
            "Add more role-relevant technical skills where applicable."
        ]

    if count >= 5:
        return 12, [
            "Increase the number of relevant technical skills shown "
            "on the resume."
        ]

    if count >= 1:
        return 7, [
            "Your resume contains few recognizable technical skills. "
            "Add relevant tools, technologies and programming skills."
        ]

    return 0, [
        "No recognizable technical skills were detected. "
        "Add a clear Technical Skills section."
    ]


def score_projects(text: str) -> tuple[int, list[str]]:
    if not has_section(text, SECTION_PATTERNS["Projects"]):
        return 0, [
            "Add a Projects section with 2–3 relevant technical projects."
        ]

    project_keywords = len(
        re.findall(
            r"\b(project|developed|built|implemented|created|designed)\b",
            text,
            re.IGNORECASE,
        )
    )

    if project_keywords >= 6:
        return 15, []

    return 10, [
        "Strengthen project descriptions with technologies, "
        "your contribution and measurable results."
    ]


def score_experience(text: str) -> tuple[int, list[str]]:
    if not has_section(text, SECTION_PATTERNS["Experience"]):
        return 2, [
            "Add internship, training, freelance or practical "
            "experience if available."
        ]

    return 10, []


def score_education(text: str) -> tuple[int, list[str]]:
    if not has_section(text, SECTION_PATTERNS["Education"]):
        return 3, [
            "Add an Education section with degree, institution, "
            "graduation year and CGPA if relevant."
        ]

    return 10, []


def score_achievements(text: str) -> tuple[int, list[str]]:
    if not has_section(text, SECTION_PATTERNS["Achievements"]):
        return 3, [
            "Add measurable achievements such as hackathons, awards, "
            "rankings or project results."
        ]

    return 10, []


def score_certifications(text: str) -> tuple[int, list[str]]:
    if not has_section(text, SECTION_PATTERNS["Certifications"]):
        return 3, [
            "Add relevant certifications, workshops or completed courses."
        ]

    return 10, []


def calculate_ats_score(resume_text: str) -> dict:
    text = resume_text.strip()
    word_count = len(re.findall(r"\b[\w+#.-]+\b", text))

    skills_found = detect_skills(text)

    contact_score, contact_suggestions = score_contact(text)
    length_score, length_suggestions = score_length(word_count)
    skills_score, skills_suggestions = score_skills(skills_found)
    projects_score, projects_suggestions = score_projects(text)
    experience_score, experience_suggestions = score_experience(text)
    education_score, education_suggestions = score_education(text)
    achievements_score, achievements_suggestions = score_achievements(text)
    certifications_score, certifications_suggestions = score_certifications(
        text
    )

    total = (
        contact_score
        + length_score
        + skills_score
        + projects_score
        + experience_score
        + education_score
        + achievements_score
        + certifications_score
    )

    suggestions = (
        contact_suggestions
        + length_suggestions
        + skills_suggestions
        + projects_suggestions
        + experience_suggestions
        + education_suggestions
        + achievements_suggestions
        + certifications_suggestions
    )

    return {
        "score": total,
        "report": {
            "Contact Information": contact_score,
            "Resume Length": length_score,
            "Skills": skills_score,
            "Projects": projects_score,
            "Experience": experience_score,
            "Education": education_score,
            "Achievements": achievements_score,
            "Certifications": certifications_score,
        },
        "skills_found": skills_found,
        "suggestions": suggestions,
        "word_count": word_count,
    }