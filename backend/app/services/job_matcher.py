import re


SKILL_ALIASES = {
    "python": ["python", "python3"],
    "java": ["java", "java se", "java ee"],
    "c": ["c programming", "c language", " c "],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql", "my sql"],
    "postgresql": ["postgresql", "postgres", "postgre sql"],
    "mongodb": ["mongodb", "mongo db", "mongo"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "javascript": ["javascript", "java script"],
    "typescript": ["typescript", "type script"],
    "react": ["react", "react.js", "reactjs"],
    "react native": ["react native", "react-native"],
    "node": ["node", "node.js", "nodejs"],
    "express": ["express", "express.js", "expressjs"],
    "fastapi": ["fastapi", "fast api"],
    "django": ["django"],
    "flask": ["flask"],
    "git": ["git", "git scm"],
    "github": ["github", "git hub"],
    "docker": ["docker", "docker container", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud", "google cloud platform"],
    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis",
        "rest api development",
    ],
    "graphql": ["graphql", "graph ql"],
    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml",
    ],
    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl",
    ],
    "tensorflow": ["tensorflow", "tensor flow"],
    "pytorch": ["pytorch", "py torch"],
    "pandas": ["pandas"],
    "numpy": ["numpy", "num py"],
    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn",
    ],
    "dbms": [
        "dbms",
        "database management system",
    ],
    "oop": [
        "oop",
        "object oriented programming",
        "object-oriented programming",
    ],
    "data structures": [
        "data structures",
        "data structure",
        "dsa",
    ],
    "algorithms": [
        "algorithms",
        "algorithm",
        "algorithmic problem solving",
    ],
    "problem solving": [
        "problem solving",
        "problem-solving",
    ],
}


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")
    text = re.sub(r"\s+", " ", text)
    return f" {text.strip()} "


def alias_exists(text: str, alias: str) -> bool:
    alias = alias.strip().lower()

    if not alias:
        return False

    escaped = re.escape(alias)

    if re.fullmatch(r"[a-z0-9]+", alias):
        pattern = rf"(?<!\w){escaped}(?!\w)"
        return re.search(pattern, text) is not None

    return re.search(escaped, text) is not None


def skill_exists(text: str, aliases: list[str]) -> bool:
    return any(alias_exists(text, alias) for alias in aliases)


def detect_skills(text: str) -> list[str]:
    normalized = normalize_text(text)

    found = []

    for skill, aliases in SKILL_ALIASES.items():
        if skill_exists(normalized, aliases):
            found.append(skill)

    return sorted(found)


def match_resume_with_job(
    resume_text: str,
    job_description: str,
) -> dict:
    resume_skills = set(detect_skills(resume_text))
    required_skills = set(detect_skills(job_description))

    matched_skills = sorted(resume_skills.intersection(required_skills))
    missing_skills = sorted(required_skills.difference(resume_skills))

    total_required = len(required_skills)

    if total_required:
        score = round(
            (len(matched_skills) / total_required) * 100
        )
    else:
        score = 0

    if total_required:
        message = (
            "Match calculated from the technical skills "
            "recognized in the job description."
        )
    else:
        message = (
            "No recognized technical skills were found in the "
            "job description. Add specific technologies or "
            "requirements for a more meaningful match."
        )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_required_skills": total_required,
        "skill_coverage": score,
        "message": message,
    }