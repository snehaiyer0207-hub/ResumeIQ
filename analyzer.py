import pdfplumber
import re

JOB_SKILLS = {
    "Data Analyst": ["python", "sql", "excel", "tableau", "power bi", "pandas", "numpy", "statistics", "data analysis", "data visualization"],
    "Python Developer": ["python", "django", "flask", "fastapi", "sql", "mysql", "postgresql", "api", "git"],
    "Web Developer": ["html", "css", "javascript", "react", "node.js", "express", "bootstrap", "git", "github", "api"],
    "Frontend Developer": ["html", "css", "javascript", "react", "typescript", "tailwind", "bootstrap", "responsive design", "git", "github"],
    "Backend Developer": ["python", "java", "node.js", "express", "sql", "mysql", "mongodb", "api", "rest api", "git"],
    "Java Developer": ["java", "spring", "spring boot", "hibernate", "sql", "mysql", "rest api", "maven", "git", "oops"],
    "Full Stack Developer": ["html", "css", "javascript", "react", "node.js", "express", "mongodb", "sql", "git", "api"],
    "Software Developer": ["python", "java", "c++", "sql", "data structures", "algorithms", "oops", "git", "github"],
    "Database Administrator": ["sql", "mysql", "oracle", "postgresql", "database", "backup", "security", "database management", "linux"],
    "UI/UX Designer": ["figma", "adobe xd", "wireframing", "prototyping", "user research", "user experience", "user interface", "usability", "design systems"],
    "Digital Marketing": ["seo", "sem", "social media", "google ads", "google analytics", "content marketing", "email marketing", "keyword research"],
    "Cybersecurity Analyst": ["cybersecurity", "network security", "ethical hacking", "penetration testing", "linux", "firewall", "siem", "cryptography", "vulnerability assessment"],
    "Cloud Engineer": ["aws", "azure", "google cloud", "docker", "kubernetes", "linux", "terraform", "cloud computing", "devops", "ci/cd"],
    "Machine Learning Engineer": ["python", "machine learning", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "statistics", "deep learning", "data science"]
}

SECTIONS = [
    "education", "skills", "experience", "projects",
    "certifications", "achievements", "summary", "objective"
]


def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()


def analyze_resume(file, role):
    text = extract_text(file)
    keywords = JOB_SKILLS.get(role, [])

    matched = [k for k in keywords if k in text]
    missing = [k for k in keywords if k not in text]

    skills = sorted({
        skill
        for keywords in JOB_SKILLS.values()
        for skill in keywords
        if skill in text
    })

    sections = {
        s.title(): bool(re.search(r"\b" + re.escape(s) + r"\b", text))
        for s in SECTIONS
    }

    word_count = len(text.split())
    keyword_score = round(len(matched) / len(keywords) * 100) if keywords else 0

    section_score = sum(sections.values()) / len(SECTIONS) * 25

    if 150 <= word_count <= 700:
        length_score = 15
    elif 100 <= word_count <= 900:
        length_score = 10
    else:
        length_score = 5

    ats_score = min(
        100,
        round(keyword_score * 0.60 + section_score + length_score)
    )

    recommendations = []

    if not sections["Achievements"]:
        recommendations.append("Add important achievements and measurable results.")

    if not sections["Summary"]:
        recommendations.append("Add a short professional summary for your target role.")

    if missing:
        recommendations.append("Consider adding: " + ", ".join(missing[:5]))

    if keyword_score < 60:
        recommendations.append("Improve keyword alignment with the selected job role.")

    if word_count < 150:
        recommendations.append("Your resume is quite short. Add relevant projects or experience.")

    if not recommendations:
        recommendations.append("Your resume has strong alignment with this job role.")

    return {
        "ats_score": ats_score,
        "keyword_score": keyword_score,
        "word_count": word_count,
        "skills": skills,
        "sections": sections,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "recommendations": recommendations
    }