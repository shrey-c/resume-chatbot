from app.models.schemas import (
    Resume, Experience, Education, Skill, Project, 
    Certification, Award, Interest,
    ContactInfo, SkillCategory
)


# YOUR RESUME DATA - CUSTOMIZE THIS SECTION
def get_resume_data() -> Resume:
    """
    Returns the resume data. 
    
    CUSTOMIZE THIS FUNCTION with your actual resume information!
    """
    return Resume(
        name="Shreyansh Chheda",
        title="AI/ML Engineer | GenAI Specialist | Full-Stack Developer",
        summary="""AI/ML Engineer specializing in full-stack development, data science and AI/ML. Proven ability to build end-to-end machine learning solutions and drive business impact—such as saving 3M AUD annually through automation and enhancing customer experience via AskTelstra GenAI chatbot. Expert in Python, AI, Java, and cloud technologies, with a track record of innovation, leadership, and scalable software delivery.""",
        
        contact=ContactInfo(
            email="shreyansh.chheda@gmail.com",
            phone="+91 9820477990",
            linkedin="https://linkedin.com/in/shreyansh-chheda/",
            github="https://github.com/shreyansh",
            location="Pune, Maharashtra, India"
        ),
        
        experience=[
            Experience(
                company="Telstra (TLSA)",
                position="ML Engineer",
                location="Pune, Maharashtra, India",
                start_date="2025-07",
                end_date=None,  # Current job
                description="""Leading AI/ML initiatives including GenAI call drivers automation, AskTelstra chatbot enhancements, and advanced analytics solutions. Tech lead mentoring team on cutting-edge AI solutions.""",
                achievements=[
                    "Built GenAI Call Drivers automation analyzing 25K calls/day, delivering insights to board of directors, enabling multi-million dollar business decisions",
                    "Designed end-to-end pipeline using Azure Data Factory, AzureML, and PowerBI with GPT-5-mini reasoning model",
                    "Enhanced AskTelstra GenAI RAG chatbot, reducing build costs by 88% and scaling to 15K+ frontline agents",
                    "Automated NATAMA Fault Data Process saving 3M AUD annually and eliminating 28 days of manual effort monthly",
                    "Built GenAI ENPS verbatim analyzer using GPT-4.1-mini, saving a month of manual effort",
                    "Developed ensemble ML model (XGBoost, GRU, Logistic Regression) for PII identification in SMS",
                    "Leader and mentor accelerating developer onboarding and contributions"
                ]
            ),
            Experience(
                company="Telstra",
                position="Machine Learning Engineer",
                location="Pune, Maharashtra, India",
                start_date="2024-05",
                end_date="2025-06",
                description="""Enhanced AskTelstra RAG-based GenAI chatbot architecture, security, and performance. Streamlined deployment processes and improved system reliability.""",
                achievements=[
                    "Introduced unit testing with pytest, backend authentication, and SSO using JWT tokens",
                    "Designed comprehensive logging framework with unique identifiers improving traceability",
                    "Streamlined weekly releases deploying to 1,500 agents with scaling to 5,000",
                    "Improved performance via codebase modularization and optimized chunking/indexing",
                    "Awarded Team Awards for FY24 Q4 and FY25 Q1",
                    "Recognized as Data-engineering India Achiever of the Month (Jan 2025)"
                ]
            ),
            Experience(
                company="Telstra",
                position="Senior Associate Software Developer",
                location="Pune, Maharashtra, India (Hybrid)",
                start_date="2022-10",
                end_date="2024-04",
                description="""ML Developer and Java Developer building scalable email segregation systems and owning API development platform. Led mailbox onboarding initiatives and mentored junior developers.""",
                achievements=[
                    # ML Developer Achievements
                    "Mapped a scalable pathway to onboard new Mailboxes within timelines for stakeholders",
                    "Tested and implemented several ML and DL algorithms from renowned ML libraries to build email segregation systems",
                    "Completed full ML development lifecycle: Data Cleaning, Data Analysis, ML Modelling, ML Pipelining, Documentation and Presentation",
                    # Java Developer Achievements
                    "Took ownership of the API development platform as the lead developer",
                    "Implemented connection pooling for the APIs improving latency and response time by over 500%",
                    "Upgraded APIs and increased code coverage to at least 95% to resolve tech debt, making APIs more robust, efficient and secure",
                    "Mentored junior developers on the platform on how to develop fault-tolerant APIs"
                ]
            ),
            Experience(
                company="Telstra",
                position="Associate Software Engineer",
                location="India",
                start_date="2021-07",
                end_date="2022-10",
                description="""Chatbot Developer and Java Developer delivering automated chat flows and scalable Spring Boot APIs. Developed NLP models for sentiment analysis and topic modeling.""",
                achievements=[
                    # Chatbot Developer Achievements
                    "Delivered chat flows with automated testing based on stakeholder requirements",
                    "Developed a Google widget that saves 50% time in development and testing",
                    "Developed an Alert system that can alert a user of an update in chat flows",
                    "Developed Proof-of-concept Natural Language Processing Models: (1) Sentiment analysis to assimilate whether work completed by a worker was positive or negative, (2) Topic modeling to determine where the problem exists when multiple users face similar issues",
                    # Java Developer Achievements
                    "Developed scalable Spring Boot APIs after conversing with BAs and deployed them on Azure instances",
                    "Worked on Azure Functions PoC with senior developers and helped in JUnit5 migration"
                ]
            )
        ],
        
        education=[
            Education(
                institution="Veermata Jijabai Technological Institute (VJTI)",
                degree="Bachelor of Technology",
                field_of_study="Computer Science",
                location="Mumbai, India",
                start_date="05/2017",
                end_date="05/2021",
                gpa=None,
                honors=[]
            )
        ],
        
        skills=[
            # ========== GENERATIVE AI ==========
            Skill(name="Large Language Models (LLM)", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="GPT-4 & GPT-5", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="Ollama", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="Prompt Engineering", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="RAG (Retrieval Augmented Generation)", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="LangChain", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="LangGraph", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="Agentic AI Workflows", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="Multi-Agent Systems", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="Agent-to-Agent (A2A) Communication", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            Skill(name="Model Context Protocol (MCP)", category=SkillCategory.GENERATIVE_AI, proficiency="Advanced"),
            Skill(name="GenAI Solution Architecture", category=SkillCategory.GENERATIVE_AI, proficiency="Expert"),
            
            # ========== AI & MACHINE LEARNING ==========
            Skill(name="Machine Learning", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Deep Learning", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Natural Language Processing (NLP)", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Computer Vision", category=SkillCategory.AI_ML, proficiency="Intermediate"),
            Skill(name="Sentiment Analysis", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Topic Modeling", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Neural Networks", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Ensemble Learning", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="XGBoost", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Gradient Boosting Machines (GBM)", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Random Forest", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Logistic Regression", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Support Vector Machines (SVM)", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="K-Means Clustering", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Decision Trees", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Recurrent Neural Networks (RNN/GRU/LSTM)", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Convolutional Neural Networks (CNN)", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Transfer Learning", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Feature Engineering", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Model Optimization", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="Hyperparameter Tuning", category=SkillCategory.AI_ML, proficiency="Expert"),
            Skill(name="MLOps & ML Pipelines", category=SkillCategory.AI_ML, proficiency="Expert"),
            
            # ========== PROGRAMMING LANGUAGES ==========
            Skill(name="Python", category=SkillCategory.PROGRAMMING, proficiency="Expert"),
            Skill(name="Java", category=SkillCategory.PROGRAMMING, proficiency="Expert"),
            Skill(name="JavaScript", category=SkillCategory.PROGRAMMING, proficiency="Intermediate"),
            Skill(name="Bash/Shell Scripting", category=SkillCategory.PROGRAMMING, proficiency="Expert"),
            
            # ========== FRAMEWORKS & LIBRARIES ==========
            # ML/DL Frameworks
            Skill(name="PyTorch", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="TensorFlow", category=SkillCategory.FRAMEWORKS, proficiency="Intermediate"),
            Skill(name="Scikit-learn", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Keras", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Hugging Face Transformers", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="spaCy", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="NLTK", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            
            # Data Science
            Skill(name="Pandas", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="NumPy", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Matplotlib", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Seaborn", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Plotly", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            
            # Backend Frameworks
            Skill(name="FastAPI", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Flask", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Streamlit", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Spring Boot", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="RESTful API Design", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Microservices Architecture", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            
            # Frontend
            Skill(name="React.js", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="HTML/CSS", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Bootstrap", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            
            # Testing
            Skill(name="pytest", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="JUnit", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Mockito", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Unit Testing", category=SkillCategory.FRAMEWORKS, proficiency="Expert"),
            Skill(name="Integration Testing", category=SkillCategory.FRAMEWORKS, proficiency="Intermediate"),
            
            # ========== DATABASES & VECTOR STORES ==========
            Skill(name="FAISS", category=SkillCategory.DATABASES, proficiency="Expert"),
            Skill(name="ChromaDB", category=SkillCategory.DATABASES, proficiency="Expert"),
            Skill(name="Pinecone", category=SkillCategory.DATABASES, proficiency="Intermediate"),
            Skill(name="PostgreSQL", category=SkillCategory.DATABASES, proficiency="Intermediate"),
            Skill(name="MySQL", category=SkillCategory.DATABASES, proficiency="Intermediate"),
            Skill(name="MongoDB", category=SkillCategory.DATABASES, proficiency="Intermediate"),
            Skill(name="SQL", category=SkillCategory.DATABASES, proficiency="Expert"),
            Skill(name="NoSQL", category=SkillCategory.DATABASES, proficiency="Beginner"),
            Skill(name="Database Design", category=SkillCategory.DATABASES, proficiency="Intermediate"),
            Skill(name="Query Optimization", category=SkillCategory.DATABASES, proficiency="Intermediate"),
            
            # ========== CLOUD & DEVOPS ==========
            Skill(name="Microsoft Azure", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            
            # Azure AI Services
            Skill(name="Azure OpenAI Service", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure Cognitive Services", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure AI Search", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            
            # Azure Data & Analytics
            Skill(name="Azure Data Factory", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure Stream Analytics", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure Cosmos DB", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            
            # Azure Compute
            Skill(name="Azure Virtual Machines", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure App Service", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure Container Instances", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Azure Kubernetes Service (AKS)", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            
            # Azure ML & AI Infrastructure
            Skill(name="Azure ML Studio", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure ML Compute", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure ML Model Registry", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure ML Pipelines", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            
            # Azure Monitoring & Management
            Skill(name="Azure Monitor", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Azure Application Insights", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Azure Log Analytics", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Azure Alerts", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Azure Resource Manager (ARM)", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Azure CLI", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure Portal", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            
            # Azure Security & Identity
            Skill(name="Azure Active Directory (Entra ID)", category=SkillCategory.CLOUD_DEVOPS, proficiency="Beginner"),
            Skill(name="Azure Key Vault", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Azure Managed Identities", category=SkillCategory.CLOUD_DEVOPS, proficiency="Beginner"),
            Skill(name="Azure RBAC", category=SkillCategory.CLOUD_DEVOPS, proficiency="Beginner"),
            
            # Azure Integration
            Skill(name="Azure Service Bus", category=SkillCategory.CLOUD_DEVOPS, proficiency="Beginner"),
            
            # Azure DevOps & Other
            Skill(name="Azure Functions", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            Skill(name="Azure DevOps", category=SkillCategory.CLOUD_DEVOPS, proficiency="Expert"),
            
            # General DevOps
            Skill(name="Docker", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Kubernetes", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="CI/CD Pipelines", category=SkillCategory.CLOUD_DEVOPS, proficiency="Intermediate"),
            Skill(name="Infrastructure as Code (IaC)", category=SkillCategory.CLOUD_DEVOPS, proficiency="Beginner"),
            
            # ========== TOOLS & PLATFORMS ==========
            Skill(name="Git & GitHub", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="GitLab", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="PowerBI", category=SkillCategory.TOOLS, proficiency="Beginner"),
            Skill(name="Tableau", category=SkillCategory.TOOLS, proficiency="Beginner"),
            Skill(name="Jupyter Notebooks", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="VS Code", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="IntelliJ IDEA", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="PyCharm", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="Postman", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="Swagger/OpenAPI", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="JIRA", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="Confluence", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="Slack", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="Microsoft Teams", category=SkillCategory.TOOLS, proficiency="Expert"),
            Skill(name="Miro", category=SkillCategory.TOOLS, proficiency="Expert"),
            
            # ========== SOFT SKILLS ==========
            Skill(name="Technical Leadership", category=SkillCategory.SOFT_SKILLS, proficiency="Intermediate"),
            Skill(name="Team Mentoring & Coaching", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Cross-functional Collaboration", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Stakeholder Management", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Problem Solving & Critical Thinking", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Agile & Scrum Methodologies", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Code Review & Quality Assurance", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Technical Documentation", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Presentation & Communication", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Project Management", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Innovation & Research", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Business Analysis", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="System Design & Architecture", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Performance Optimization", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
            Skill(name="Debugging & Troubleshooting", category=SkillCategory.SOFT_SKILLS, proficiency="Expert"),
        ],
        
        projects=[
            Project(
                name="AskTelstra GenAI RAG Chatbot",
                description="""Enhanced enterprise-scale GenAI chatbot handling 8000+ daily queries 
                using RAG architecture. Achieved 88% cost reduction through optimization and 
                architectural improvements.""",
                technologies=["Python", "LangChain", "RAG", "Azure", "FAISS", "GenAI"],
                url="",
                start_date="2024-05",
                highlights=[
                    "Reduced operational costs by 88% through architectural optimization",
                    "Handles 8000+ daily customer queries",
                    "Implemented advanced RAG pipeline with vector similarity search",
                    "Awarded Team Quarterly Award Work as One FY25 Q1"
                ]
            ),
            Project(
                name="GenAI Call Drivers Automation",
                description="""Built automated system analyzing 25,000 calls daily using GPT-5-mini 
                reasoning models to extract key drivers and insights from customer interactions.""",
                technologies=["Python", "GenAI", "GPT-5-mini", "NLP", "Azure"],
                url="",
                start_date="2025-07",
                highlights=[
                    "Analyzes 25,000 calls per day automatically",
                    "Implemented GPT-5-mini reasoning for driver extraction",
                    "Provides actionable insights for customer service improvement",
                    "Awarded Team Quarterly Award Work as One FY24 Q4"
                ]
            ),
            Project(
                name="NATAMA Automation Platform",
                description="""Developed automation platform for network traffic analysis saving 
                3 million AUD annually through automated decision-making and process optimization.""",
                technologies=["Python", "Machine Learning", "Azure", "MLOps"],
                url="",
                start_date="2025-07",
                highlights=[
                    "Saved 3 million AUD annually in operational costs",
                    "Automated complex network traffic analysis workflows",
                    "Implemented ML-driven decision support system",
                    "Deployed at enterprise scale across Telstra operations"
                ]
            ),
            Project(
                name="NLP Mailboxes Solution",
                description="""Created intelligent NLP-based system for automated email classification 
                and routing. Improved API latency by 500% through optimization.""",
                technologies=["Python", "NLP", "Spacy", "Azure ML", "FastAPI"],
                url="",
                start_date="2022-10",
                end_date="2024-04",
                highlights=[
                    "500% improvement in API response latency",
                    "Automated classification of thousands of emails daily",
                    "Integrated with Azure ML for model deployment",
                    "Reduced manual email routing effort significantly"
                ]
            ),
            Project(
                name="ENPS Sentiment Analyzer",
                description="""Built sentiment analysis tool for Employee Net Promoter Score (ENPS) 
                surveys providing actionable insights for HR and management.""",
                technologies=["Python", "NLP", "Azure", "PowerBI"],
                url="",
                start_date="2023-01",
                end_date="2023-06",
                highlights=[
                    "Automated sentiment analysis of employee feedback",
                    "Generated insights for HR decision-making",
                    "Integrated with PowerBI for visualization",
                    "Improved employee engagement tracking"
                ]
            )
        ],
        
        certifications=[
            Certification(
                name="From Engineer to Technical Manager",
                issuer="Udemy",
                issue_date="2025-04",
                credential_id="UC-8a013bef-2691-4e8a-9694-f3014f00e83a",
                skills=["Leadership", "Team Leadership"]
            ),
            Certification(
                name="LangChain- Develop LLM powered applications with LangChain",
                issuer="Udemy",
                issue_date="2025-03",
                credential_id="UC-ea0a760e-1498-411d-92ef-58d9b574bc78",
                skills=["LangChain", "Generative AI"]
            ),
            Certification(
                name="Agile Software Development",
                issuer="LinkedIn",
                issue_date="2021-07",
                skills=["Computer Engineering"]
            ),
            Certification(
                name="Introduction to Quantum Computing Certificate of Completion",
                issuer="The Coding School",
                issue_date="2021-05",
                skills=["Software Development"]
            ),
            Certification(
                name="Deep Learning Specialization",
                issuer="Coursera",
                issue_date="2020-06",
                credential_id="LPM2R2FKSZMX",
                skills=["Software Development"]
            ),
            Certification(
                name="Advanced Styling with Responsive Design",
                issuer="Coursera",
                issue_date="2020-05",
                credential_id="DY44QLUXMAZH",
                skills=[]
            ),
            Certification(
                name="Business English: Networking",
                issuer="Coursera",
                issue_date="2020-05",
                credential_id="G3L2N25YJPBS",
                skills=["Software Development"]
            ),
            Certification(
                name="Introduction to Structured Query Language (SQL)",
                issuer="Coursera",
                issue_date="2020-05",
                credential_id="XPVPAGCKZUW9",
                skills=["Computer Engineering", "Software Development"]
            ),
            Certification(
                name="Introduction to Data Science in Python",
                issuer="Coursera",
                issue_date="2020-04",
                credential_id="Q5X2EV2CAWK4",
                skills=["Software Development"]
            ),
            Certification(
                name="Nvidia deep learning course completion",
                issuer="NVIDIA",
                issue_date="2019-02",
                skills=[]
            )
        ],
        
        awards=[
            Award(
                title="Data-engineering India Achiever of the Month",
                issuer="Telstra",
                date="2025-01",
                description="Recognized for outstanding contributions to data engineering and AI/ML initiatives"
            ),
            Award(
                title="Team Quarterly Award - Work as One FY25 Q1",
                issuer="Telstra",
                date="2024-10",
                description="Team recognition for exceptional collaboration and delivery"
            ),
            Award(
                title="Team Quarterly Award - Work as One FY24 Q4",
                issuer="Telstra",
                date="2024-06",
                description="Team recognition for outstanding performance and innovation"
            )
        ],
        
        languages=[
            "English (Native)",
            "Hindi (Native)"
        ],
        
        interests=[
            Interest(
                name="Motorcycle Touring",
                description="Passionate about long-distance motorcycle touring with full riding gear, exploring scenic routes and new destinations"
            ),
            Interest(
                name="Travel & Adventure",
                description="Adventure enthusiast who loves exploring new places, cultures, and challenging experiences"
            ),
            Interest(
                name="Photography",
                description="Capturing beautiful moments through lens, specializing in nature and landscape photography"
            ),
            Interest(
                name="Nature & Hiking",
                description="Avid hiker and nature lover, finding peace in the great outdoors and mountain trails"
            ),
            Interest(
                name="Fitness & Gym",
                description="Dedicated to maintaining physical fitness through regular gym workouts and training"
            ),
            Interest(
                name="Cat Parent",
                description="Proud cat dad who enjoys spending quality time with feline companion"
            )
        ]
    )


def get_resume_context() -> str:
    """
    Converts resume data to a text context for the AI model.
    
    Returns:
        Formatted string containing all resume information
    """
    resume = get_resume_data()
    
    context_parts = [
        f"Name: {resume.name}",
        f"Title: {resume.title}",
        f"Summary: {resume.summary}",
        f"\nContact Information:",
    ]
    
    # Contact
    if resume.contact.email:
        context_parts.append(f"  Email: {resume.contact.email}")
    if resume.contact.phone:
        context_parts.append(f"  Phone: {resume.contact.phone}")
    if resume.contact.location:
        context_parts.append(f"  Location: {resume.contact.location}")
    if resume.contact.linkedin:
        context_parts.append(f"  LinkedIn: {resume.contact.linkedin}")
    if resume.contact.github:
        context_parts.append(f"  GitHub: {resume.contact.github}")
    
    # Experience
    if resume.experience:
        context_parts.append("\nWork Experience:")
        for exp in resume.experience:
            end = exp.end_date if exp.end_date else "Present"
            context_parts.append(f"\n  {exp.position} at {exp.company} ({exp.start_date} - {end})")
            context_parts.append(f"  Location: {exp.location}")
            context_parts.append(f"  {exp.description}")
            if exp.achievements:
                context_parts.append("  Key Achievements:")
                for achievement in exp.achievements:
                    context_parts.append(f"    - {achievement}")
    
    # Education
    if resume.education:
        context_parts.append("\nEducation:")
        for edu in resume.education:
            end = edu.end_date if edu.end_date else "Present"
            context_parts.append(f"\n  {edu.degree} in {edu.field_of_study}")
            context_parts.append(f"  {edu.institution}, {edu.location} ({edu.start_date} - {end})")
            if edu.gpa:
                context_parts.append(f"  GPA: {edu.gpa}")
            if edu.honors:
                context_parts.append("  Honors: " + ", ".join(edu.honors))
    
    # Skills
    if resume.skills:
        context_parts.append("\nSkills:")
        skills_by_category = {}
        for skill in resume.skills:
            if skill.category.value not in skills_by_category:
                skills_by_category[skill.category.value] = []
            skills_by_category[skill.category.value].append(
                f"{skill.name} ({skill.proficiency})" if skill.proficiency else skill.name
            )
        
        for category, skills in skills_by_category.items():
            context_parts.append(f"  {category}: {', '.join(skills)}")
    
    # Projects
    if resume.projects:
        context_parts.append("\nProjects:")
        for proj in resume.projects:
            context_parts.append(f"\n  {proj.name}")
            context_parts.append(f"  {proj.description}")
            context_parts.append(f"  Technologies: {', '.join(proj.technologies)}")
            if proj.url:
                context_parts.append(f"  URL: {proj.url}")
            if proj.highlights:
                context_parts.append("  Highlights:")
                for highlight in proj.highlights:
                    context_parts.append(f"    - {highlight}")
    
    # Certifications
    if resume.certifications:
        context_parts.append("\nCertifications:")
        for cert in resume.certifications:
            cert_str = f"  - {cert.name} ({cert.issuer}, {cert.issue_date})"
            if cert.credential_id:
                cert_str += f" - ID: {cert.credential_id}"
            context_parts.append(cert_str)
            if cert.skills:
                context_parts.append(f"    Skills: {', '.join(cert.skills)}")
    
    # Awards & Recognition
    if resume.awards:
        context_parts.append("\nAwards & Recognition:")
        for award in resume.awards:
            context_parts.append(f"  - {award.title} ({award.issuer}, {award.date})")
            if award.description:
                context_parts.append(f"    {award.description}")
    
    # Languages
    if resume.languages:
        context_parts.append(f"\nLanguages: {', '.join(resume.languages)}")
    
    # Interests & Hobbies
    if resume.interests:
        context_parts.append("\nInterests & Hobbies:")
        for interest in resume.interests:
            context_parts.append(f"  - {interest.name}")
            if interest.description:
                context_parts.append(f"    {interest.description}")
    
    return "\n".join(context_parts)


# Global variable to store current resume
_current_resume: Resume = get_resume_data()


def update_resume_data(new_resume: Resume) -> None:
    """
    Update the resume data with new information from uploaded PDF.
    
    This function is called by the admin portal after parsing a PDF.
    It updates the global resume data without modifying the source file.
    
    For persistence, consider implementing database storage.
    
    Args:
        new_resume: New Resume object with updated information
    """
    global _current_resume
    _current_resume = new_resume


def get_current_resume() -> Resume:
    """
    Get the current resume data (may be updated via admin portal).
    
    Returns:
        Current Resume object
    """
    global _current_resume
    return _current_resume
