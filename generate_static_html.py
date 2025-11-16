"""
Generate a static HTML version with pre-rendered data for better HTML parsing.
This creates an SEO-friendly and parser-friendly version of the resume.
"""

from app.services.resume_data import get_resume_data
from pathlib import Path
import json


def generate_static_html():
    """Generate static HTML with all resume data pre-rendered."""
    
    resume = get_resume_data()

    # Export resume data to JSON for static site parity
    resume_json = resume.model_dump(mode="json")
    json_path = Path("static/resume_data.json")
    json_path.write_text(
        json.dumps(resume_json, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"✅ Generated static resume JSON: {json_path}")
    
    # Generate skills by category
    skills_html = ""
    skills_by_category = {}
    for skill in resume.skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(f"{skill.name} ({skill.proficiency})")
    
    for category, skills in skills_by_category.items():
        skills_html += f"""
        <div class="skill-category">
            <h3>{category}</h3>
            <div class="skill-items">
                {' '.join([f'<span class="skill-item">{skill}</span>' for skill in skills])}
            </div>
        </div>
        """
    
    # Generate experience
    experience_html = ""
    for exp in resume.experience:
        achievements_html = ""
        if exp.achievements:
            achievements_html = "<ul>" + "".join([f"<li>{a}</li>" for a in exp.achievements]) + "</ul>"
        
        experience_html += f"""
        <article class="job">
            <h3>{exp.position}</h3>
            <h4>{exp.company} | {exp.location}</h4>
            <p class="dates">{exp.start_date} - {exp.end_date or 'Present'}</p>
            <p>{exp.description}</p>
            {achievements_html}
        </article>
        """
    
    # Generate education
    education_html = ""
    for edu in resume.education:
        education_html += f"""
        <div class="education-item">
            <h3>{edu.degree} in {edu.field_of_study}</h3>
            <h4>{edu.institution}</h4>
            <p class="dates">{edu.start_date} - {edu.end_date or 'Present'}</p>
            {f'<p>GPA: {edu.gpa}</p>' if edu.gpa else ''}
        </div>
        """
    
    # Generate projects
    projects_html = ""
    for proj in resume.projects:
        highlights_html = ""
        if proj.highlights:
            highlights_html = "<ul>" + "".join([f"<li>{h}</li>" for h in proj.highlights]) + "</ul>"
        
        projects_html += f"""
        <article class="project">
            <h3>{proj.name}</h3>
            <p class="description">{proj.description}</p>
            <p class="technologies"><strong>Technologies:</strong> {', '.join(proj.technologies)}</p>
            {highlights_html}
        </article>
        """
    
    # Generate certifications
    certs_html = ""
    for cert in resume.certifications:
        certs_html += f"""
        <div class="cert-card">
            <h4>{cert.name}</h4>
            <p class="cert-issuer">{cert.issuer}</p>
            <p class="cert-date">{cert.issue_date}</p>
            {f'<p class="cert-id">Credential ID: {cert.credential_id}</p>' if cert.credential_id else ''}
        </div>
        """
    
    # Generate awards
    awards_html = ""
    for award in resume.awards:
        awards_html += f"""
        <div class="award-card">
            <h4>{award.title}</h4>
            <p class="award-issuer">{award.issuer}</p>
            <p class="award-date">{award.date}</p>
            {f'<p class="award-description">{award.description}</p>' if award.description else ''}
        </div>
        """
    
    # Generate interests
    interests_html = ""
    for interest in resume.interests:
        interests_html += f"""
        <div class="interest-card">
            <h4>{interest.name}</h4>
            {f'<p>{interest.description}</p>' if interest.description else ''}
        </div>
        """
    
    # Create static content snippet to insert into HTML
    static_content = f"""
<!-- STATIC RESUME DATA FOR HTML PARSING -->
<!-- This section is used by the HTML parser for chatbot responses -->

<div id="resume-static-data" style="display: none;">
    <div id="static-intro">
        <h1>{resume.name}</h1>
        <h2>{resume.title}</h2>
        <p>{resume.summary}</p>
        <div class="contact">
            <p>Email: {resume.contact.email}</p>
            <p>Phone: {resume.contact.phone}</p>
            <p>LinkedIn: {resume.contact.linkedin}</p>
            <p>GitHub: {resume.contact.github}</p>
        </div>
    </div>
    
    <div id="static-experience">
        <h2>Professional Experience</h2>
        {experience_html}
    </div>
    
    <div id="static-education">
        <h2>Education</h2>
        {education_html}
    </div>
    
    <div id="static-skills">
        <h2>Skills</h2>
        {skills_html}
    </div>
    
    <div id="static-projects">
        <h2>Projects</h2>
        {projects_html}
    </div>
    
    <div id="static-certifications">
        <h2>Certifications</h2>
        {certs_html}
    </div>
    
    <div id="static-awards">
        <h2>Awards & Recognition</h2>
        {awards_html}
    </div>
    
    <div id="static-interests">
        <h2>Interests</h2>
        {interests_html}
    </div>
</div>
<!-- END STATIC RESUME DATA -->
"""
    
    # Save to file
    output_path = Path("static/resume_static_data.html")
    output_path.write_text(static_content, encoding='utf-8')
    
    print(f"✅ Generated static resume data: {output_path}")
    print(f"   Size: {len(static_content)} characters")
    print("\nTo use in index.html, add this line after <body>:")
    print('  <!-- include static/resume_static_data.html -->')
    
    return static_content


if __name__ == "__main__":
    generate_static_html()
