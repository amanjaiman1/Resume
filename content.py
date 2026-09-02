"""Single source of truth for the resume. build.py renders DOCX + HTML + Markdown from this.

Tuned to fit ONE A4 page. If you add a bullet, run `python3 render_pdf.py` and confirm it still
reports 1 page before sending the resume anywhere.
"""

NAME = "AMAN JAIMAN"
TITLE = "Product Manager  |  Frontend Engineer"
CONTACT_1 = "Bharatpur, Rajasthan 321001, India  |  +91 6378722785  |  amanjaiman001@gmail.com"
CONTACT_2 = "linkedin.com/in/aman-jaiman  |  github.com/amanjaiman1  |  leetcode.com/u/amanjaiman890"

SUMMARY = (
    "Product Manager and Frontend Engineer with 2+ years shipping production web applications in React.js, "
    "Next.js, and TypeScript. Currently running an independent, stealth-stage product end to end, owning user "
    "discovery, roadmap, frontend architecture, and release. Proven record of lifting engagement and cutting "
    "load times against measurable targets."
)

SKILLS = [
    ("Languages & CS",
     "JavaScript (ES6+), TypeScript, C++, Java, Python, SQL, HTML5, CSS3, Data Structures & Algorithms, "
     "Object-Oriented Programming, DBMS"),
    ("Frontend",
     "React.js, Next.js (App Router, SSR/SSG/ISR), Redux Toolkit, React Query, Tailwind CSS, Three.js, "
     "Responsive Design, Web Accessibility (WCAG), SEO, Core Web Vitals"),
    ("Backend & Tools",
     "Node.js, Express.js, RESTful API Design & Integration, Prisma ORM, PostgreSQL, MySQL, Firebase, "
     "JWT/OAuth Authentication, Git, GitHub Actions, CI/CD, Vercel, Figma, Jira, Linux"),
    ("Product Management",
     "Product Roadmapping, User Research, PRD & User Story Authoring, Backlog Prioritization (RICE), "
     "Agile & Scrum, Sprint Planning, A/B Testing, Product Analytics, Stakeholder Management, Go-to-Market"),
]

EXPERIENCE = [
    {
        "role": "Founder, Product Manager & Frontend Engineer",
        "dates": "Apr 2025 - Present",
        "org": "Independent Product Venture (Stealth)  |  Remote",
        "stack": "Next.js, TypeScript, Tailwind CSS, PostgreSQL",
        "bullets": [
            "Founded and lead an independent, stealth-stage web product as sole Product Manager and Frontend "
            "Engineer, owning discovery, roadmap, UX, engineering, and release end to end.",
            "Ran 40+ user discovery interviews and competitive analysis, converting findings into PRDs, personas, "
            "and a RICE-prioritized backlog of 60+ user stories across 3 shipped milestones.",
            "Architected the product in Next.js (App Router), TypeScript, and Tailwind CSS with a 30+ component "
            "design system, cutting feature build time by 40% and holding a 95+ Lighthouse performance score.",
            "Engineered a type-safe REST layer on Prisma ORM and PostgreSQL with JWT authentication, automated "
            "releases through GitHub Actions and Vercel, and A/B tested onboarding to lift completion by 25%.",
        ],
    },
    {
        "role": "Frontend Engineer",
        "dates": "Apr 2024 - Apr 2025",
        "org": "Optus EdTech  |  Remote",
        "stack": "React.js, Next.js, Tailwind CSS, RESTful APIs",
        "bullets": [
            "Migrated a legacy multi-page platform into a single-page React application, improving customer "
            "engagement by 10% and eliminating full page reloads across core user journeys.",
            "Cut initial page load time by 35% via code splitting, lazy loading, asset compression, and React "
            "memoization, directly improving session retention.",
            "Shipped 25+ reusable, responsive React and Next.js components in Tailwind CSS from Figma designs, and "
            "redesigned UI workflows to reduce task completion time by 30%.",
            "Integrated RESTful APIs with robust loading and error states, and improved SEO and accessibility using "
            "semantic HTML, ARIA attributes, and Core Web Vitals optimization.",
        ],
    },
    {
        "role": "Java & DSA Trainer (Mentor)",
        "dates": "Jun 2024 - Nov 2024",
        "org": "CoderHouse  |  Remote",
        "stack": "Java, Recursion, Trees, Graphs, Dynamic Programming",
        "bullets": [
            "Mentored 300+ students in Java and Data Structures & Algorithms, designing 40+ lesson plans across "
            "Recursion, Trees, Graphs, and Dynamic Programming that raised batch assessment scores.",
        ],
    },
]

PROJECTS = [
    {
        "role": "DocMate - AI-Powered PDF Data Extraction Tool",
        "dates": "Mar 2024 - Jun 2024",
        "org": None,
        "stack": None,
        "bullets": [
            "Built a document intelligence tool that extracts specific information from PDFs via natural-language "
            "prompts, backed by a type-safe Prisma data model for storage, history, and retrieval. "
            "Next.js, React.js, TypeScript, Prisma, Tailwind CSS  |  github.com/amanjaiman1/DocMate",
        ],
    },
    {
        "role": "3D T-Shirt Designer - Real-Time Product Customization Platform",
        "dates": "Mar 2023 - Aug 2023",
        "org": None,
        "stack": None,
        "bullets": [
            "Developed a real-time 3D product customizer in Three.js letting users apply colors, logos, and text to "
            "a live rotatable model and export the result, with Firebase authentication and protected routing. "
            "React.js, Three.js, Node.js, Firebase, Tailwind CSS  |  github.com/amanjaiman1/Product_3D",
        ],
    },
]

EDUCATION = {
    "degree": "Bachelor of Technology (B.Tech), Computer Science & Engineering",
    "dates": "2020 - 2024",
    "institution": "Lovely Professional University, Phagwara, Punjab",
    "score": "CGPA: 7.4 / 10",
    "coursework": None,
}

ACHIEVEMENTS = [
    {"title": "Google Kick Start", "date": "Oct 2022", "detail": "Round H \u2014 ranked 1542nd globally."},
    {"title": "Punjab Hackathon", "date": "Nov 2023", "detail": "Secured 5th place overall."},
    {"title": "Best in Drill & Shooting", "date": "Jan 2024",
     "detail": "Indian Army Attachment Camp, Jalandhar."},
    {"title": "LeetCode", "date": None,
     "detail": "500+ DSA problems solved, 100+ day streak (leetcode.com/u/amanjaiman890)."},
]
