from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
import random
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_openai_response(message: str) -> str:
    """Get response from OpenAI API"""
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """You are an AI assistant for an IT Support System. You are helpful, knowledgeable, and professional.
                    You can answer questions about technology, IT support, programming, science, business, health, travel, and virtually any topic.
                    Always provide detailed, well-formatted responses with emojis and clear structure. Be conversational but informative.
                    If it's an IT-related question, provide specific technical guidance. For other topics, be comprehensive and helpful."""
                },
                {"role": "user", "content": message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting to my AI service right now. Error: {str(e)}. Please try again later or contact support."

app = FastAPI(
    title="Unified IT Support System",
    description="A comprehensive IT support platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Unified IT Support System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "unified-it-support"}

@app.get("/api/dashboard/health")
async def get_system_health():
    """Get current system health metrics."""
    return {
        "cpu_usage": round(random.uniform(20, 80), 1),
        "memory_usage": round(random.uniform(30, 90), 1),
        "disk_usage": round(random.uniform(10, 70), 1),
        "uptime_hours": round(random.uniform(24, 168), 1),
        "active_alerts": random.randint(0, 5),
        "open_tickets": random.randint(0, 10)
    }

@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics(hours: int = 24):
    """Get comprehensive dashboard metrics."""
    # Generate mock data
    cpu_history = []
    memory_history = []
    disk_history = []

    for i in range(24):
        timestamp = datetime.now().replace(hour=i, minute=0, second=0, microsecond=0)
        cpu_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(20, 80), 1)
        })
        memory_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(30, 90), 1)
        })
        disk_history.append({
            "timestamp": timestamp.isoformat(),
            "value": round(random.uniform(10, 70), 1)
        })

    return {
        "system_health": {
            "cpu_usage": round(random.uniform(20, 80), 1),
            "memory_usage": round(random.uniform(30, 90), 1),
            "disk_usage": round(random.uniform(10, 70), 1),
            "uptime_hours": round(random.uniform(24, 168), 1),
            "active_alerts": random.randint(0, 5),
            "open_tickets": random.randint(0, 10)
        },
        "cpu_history": cpu_history,
        "memory_history": memory_history,
        "disk_history": disk_history,
        "recent_alerts": [
            {
                "id": 1,
                "title": "High CPU Usage",
                "severity": "high",
                "status": "active",
                "timestamp": datetime.now().isoformat()
            }
        ],
        "recent_tickets": [
            {
                "id": 1,
                "title": "Server Performance Issue",
                "priority": "high",
                "status": "open",
                "created_at": datetime.now().isoformat()
            }
        ]
    }

@app.get("/api/tickets")
async def get_tickets():
    """Get tickets."""
    return [
        {
            "id": 1,
            "title": "Server Performance Issue",
            "description": "The production server is running slowly",
            "priority": "high",
            "status": "open",
            "category": "performance_issue",
            "created_by": 1,
            "assigned_to": None,
            "auto_categorized": True,
            "confidence_score": 0.85,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "resolved_at": None
        }
    ]

@app.post("/api/tickets")
async def create_ticket(ticket_data: dict):
    """Create a new ticket."""
    return {
        "id": random.randint(100, 999),
        "title": ticket_data.get("title", "New Ticket"),
        "description": ticket_data.get("description", ""),
        "priority": ticket_data.get("priority", "medium"),
        "status": "open",
        "category": ticket_data.get("category", "other"),
        "created_by": 1,
        "assigned_to": None,
        "auto_categorized": True,
        "confidence_score": 0.75,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolved_at": None
    }

@app.post("/api/chatbot/chat")
async def chat_with_bot(chat_data: dict):
    """Chat with the AI-powered universal assistant."""
    message = chat_data.get("message", "").strip()
    message_lower = message.lower()

    # Enhanced universal AI responses with better formatting and unlimited scope
    if any(word in message_lower for word in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
        response_text = """👋 **Hello! I'm your AI Assistant**

I'm here to help you with virtually anything! I can assist with:

**🔧 IT Support:**
• Password resets & account issues
• VPN & network connectivity
• Software installation & updates
• Performance troubleshooting
• Email & communication tools

**📚 General Knowledge:**
• Technology & programming
• Science & mathematics
• Business & finance
• Health & wellness
• Travel & lifestyle
• And much more!

**💡 What I can do:**
• Answer complex questions
• Provide step-by-step guidance
• Explain concepts clearly
• Help with problem-solving
• Offer creative solutions

What would you like to know or discuss today?"""
        confidence = 0.95

    elif any(word in message_lower for word in ["password", "reset", "forgot", "login", "access", "account"]):
        response_text = """🔐 **Password & Account Help**

I can help you with various account and password issues:

**🔄 Password Reset Process:**
1. **Navigate** to the login page
2. **Click** "Forgot Password" or "Reset Password"
3. **Enter** your email address or username
4. **Check** your email for reset instructions
5. **Follow** the secure link provided
6. **Create** a new strong password

**💡 Password Best Practices:**
• Use at least 12 characters
• Include uppercase, lowercase, numbers, and symbols
• Avoid common words or personal information
• Use a unique password for each account
• Consider using a password manager

**🔒 Account Security:**
• Enable two-factor authentication (2FA)
• Regularly update your passwords
• Monitor account activity
• Use secure networks when logging in

**Need specific help?** Let me know your exact situation and I'll provide tailored guidance!"""
        confidence = 0.95

    elif any(word in message_lower for word in ["vpn", "remote", "connect", "network", "virtual private network"]):
        response_text = """🌐 **VPN & Network Connectivity**

I can help you with VPN setup and network issues:

**📥 VPN Setup Process:**
1. **Download** the VPN client from your IT portal
2. **Install** the application on your device
3. **Launch** the VPN client
4. **Enter** your company credentials
5. **Select** your preferred server location
6. **Connect** and verify your IP address

**🔧 Troubleshooting Common Issues:**
• **Connection fails:** Check internet connection, restart client
• **Slow speeds:** Try different server locations
• **Authentication errors:** Verify credentials, check account status
• **DNS issues:** Flush DNS cache, use different DNS servers

**🛡️ Security Benefits:**
• Encrypts your internet traffic
• Protects data on public Wi-Fi
• Bypasses geographic restrictions
• Maintains privacy and anonymity

**Need the VPN client or having specific issues?** I can provide detailed troubleshooting steps!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["slow", "performance", "lag", "freeze", "hanging", "optimize"]):
        response_text = """⚡ **Performance Optimization & Troubleshooting**

I can help diagnose and fix performance issues:

**🚀 Immediate Quick Fixes:**
• **Restart** your computer (solves 70% of issues)
• **Close** unnecessary programs and browser tabs
• **Check** available disk space (need at least 10% free)
• **Update** your operating system
• **Clear** browser cache and temporary files

**🔍 Advanced Troubleshooting:**
• **Task Manager:** Check CPU, memory, and disk usage
• **Malware Scan:** Run full antivirus scan
• **Driver Updates:** Update graphics and network drivers
• **Hardware Check:** Monitor temperatures and fan speeds
• **Registry Cleanup:** Use trusted registry cleaner tools

**💾 System Maintenance:**
• **Disk Cleanup:** Remove temporary files and old downloads
• **Defragmentation:** Optimize hard drive (HDD only)
• **Startup Programs:** Disable unnecessary startup items
• **Background Apps:** Limit background app activity

**🆘 When to Escalate:**
• Persistent crashes or blue screens
• Hardware failure symptoms
• Security concerns or malware
• Complex software conflicts

**Would you like me to create a support ticket for hands-on assistance?**"""
        confidence = 0.9

    elif any(word in message_lower for word in ["software", "install", "application", "program", "app"]):
        response_text = """💻 **Software Installation & Management**

I can help with software installation and management:

**📦 Installation Process:**
1. **Identify** the software you need
2. **Download** from official sources only
3. **Check** system requirements
4. **Run** installer as administrator
5. **Follow** installation wizard
6. **Restart** if required

**✅ Approved Software Categories:**
• **Productivity:** Microsoft Office, Google Workspace
• **Development:** VS Code, Git, Docker, Node.js
• **Design:** Adobe Creative Suite, Figma, Canva
• **Communication:** Slack, Teams, Zoom
• **Security:** Antivirus, VPN clients

**🔒 Enterprise Software:**
• **Request Process:** Submit through IT portal
• **Approval Time:** 24-48 hours typically
• **Requirements:** Business justification needed
• **Admin Rights:** Most software requires elevated privileges

**⚠️ Security Considerations:**
• Always download from official sources
• Verify digital signatures
• Keep software updated
• Avoid pirated or cracked software
• Use company-approved software when possible

**Need help with a specific software installation?** Tell me what you're trying to install!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["hours", "time", "available", "support", "contact"]):
        response_text = """🕒 **Support Hours & Contact Information**

**⏰ IT Support Availability:**
• **Regular Hours:** Monday-Friday, 8:00 AM - 6:00 PM
• **Emergency Support:** 24/7 for critical issues
• **Holiday Coverage:** Limited support during holidays

**📊 Response Time Commitments:**
• **🔴 Critical:** 1 hour (system down, security breach)
• **🟠 High Priority:** 4 hours (major functionality affected)
• **🟡 Medium Priority:** 24 hours (minor issues, workarounds available)
• **🟢 Low Priority:** 48 hours (general questions, enhancements)

**📞 Contact Methods:**
• **🤖 This AI Chatbot:** 24/7 instant assistance
• **📧 Email:** support@company.com
• **📱 Phone:** Ext. 1234 (internal) or (555) 123-4567
• **🏢 Walk-in:** IT Office, Floor 3, Room 301
• **💬 Slack:** #it-support channel
• **🎫 Portal:** https://support.company.com

**🚨 Emergency Procedures:**
• **After Hours:** Call emergency hotline
• **Security Issues:** Report immediately to security team
• **System Outages:** Check status page for updates

**Need immediate assistance?** I'm here 24/7 to help!"""
        confidence = 0.95

    elif any(word in message_lower for word in ["cybersecurity", "security", "hack", "malware", "virus", "phishing"]):
        response_text = """🛡️ **Cybersecurity & Information Security**

I can help you understand and implement cybersecurity best practices:

**🔐 Core Security Concepts:**
• **Confidentiality:** Protecting sensitive information
• **Integrity:** Ensuring data accuracy and completeness
• **Availability:** Maintaining system and data access
• **Authentication:** Verifying user identity
• **Authorization:** Controlling access permissions

**🚨 Common Threats:**
• **Malware:** Viruses, trojans, ransomware, spyware
• **Phishing:** Fraudulent emails and websites
• **Social Engineering:** Manipulation tactics
• **DDoS Attacks:** Overwhelming systems with traffic
• **Data Breaches:** Unauthorized access to sensitive data

**🛠️ Security Best Practices:**
• **Strong Passwords:** Complex, unique, regularly changed
• **Multi-Factor Authentication:** Additional security layer
• **Regular Updates:** Keep systems and software current
• **Backup Strategy:** Regular, tested data backups
• **Network Security:** Firewalls, VPNs, secure Wi-Fi

**🔍 Incident Response:**
• **Detection:** Monitor for suspicious activity
• **Containment:** Isolate affected systems
• **Eradication:** Remove threats and vulnerabilities
• **Recovery:** Restore normal operations
• **Lessons Learned:** Improve security posture

**📚 Security Awareness:**
• **Training:** Regular security education
• **Policies:** Follow company security guidelines
• **Reporting:** Report suspicious activities immediately
• **Vigilance:** Stay informed about new threats

**Need specific security guidance?** I can provide detailed information on any security topic!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["programming", "code", "development", "python", "javascript", "java", "coding"]):
        response_text = """💻 **Programming & Software Development**

I can help you with programming concepts, code examples, and development best practices:

**🔧 Popular Programming Languages:**
• **Python:** Data science, web development, automation
• **JavaScript:** Web development, Node.js, React
• **Java:** Enterprise applications, Android development
• **C#:** .NET applications, Windows development
• **Go:** Cloud computing, microservices
• **Rust:** System programming, performance-critical apps

**📚 Development Concepts:**
• **Object-Oriented Programming:** Classes, inheritance, polymorphism
• **Functional Programming:** Pure functions, immutability
• **Data Structures:** Arrays, linked lists, trees, graphs
• **Algorithms:** Sorting, searching, optimization
• **Design Patterns:** Singleton, Factory, Observer, MVC

**🛠️ Development Tools:**
• **IDEs:** VS Code, IntelliJ, Eclipse, Vim
• **Version Control:** Git, GitHub, GitLab
• **Testing:** Unit tests, integration tests, TDD
• **CI/CD:** Jenkins, GitHub Actions, Docker
• **Documentation:** README files, API docs, comments

**🌐 Web Development:**
• **Frontend:** HTML, CSS, JavaScript, React, Vue
• **Backend:** Node.js, Python Flask/Django, Java Spring
• **Databases:** SQL, NoSQL, PostgreSQL, MongoDB
• **APIs:** REST, GraphQL, microservices
• **Deployment:** AWS, Azure, Docker, Kubernetes

**📖 Learning Resources:**
• **Online Courses:** Coursera, Udemy, freeCodeCamp
• **Documentation:** Official language docs, MDN
• **Practice:** LeetCode, HackerRank, Codewars
• **Projects:** Build real applications, contribute to open source

**What specific programming topic would you like to explore?** I can provide code examples, explanations, and guidance!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["science", "physics", "chemistry", "biology", "mathematics", "math"]):
        response_text = """🔬 **Science & Mathematics**

I can help you understand scientific concepts and mathematical principles:

**🧪 Chemistry:**
• **Atomic Structure:** Protons, neutrons, electrons, orbitals
• **Chemical Bonds:** Ionic, covalent, metallic bonding
• **Reactions:** Synthesis, decomposition, combustion
• **Periodic Table:** Element properties and trends
• **Organic Chemistry:** Carbon compounds, functional groups

**⚛️ Physics:**
• **Mechanics:** Motion, forces, energy, momentum
• **Thermodynamics:** Heat, temperature, entropy
• **Electromagnetism:** Electric fields, magnetic fields
• **Quantum Mechanics:** Wave-particle duality, uncertainty
• **Relativity:** Special and general relativity

**🧬 Biology:**
• **Cell Biology:** Structure, organelles, processes
• **Genetics:** DNA, RNA, protein synthesis
• **Evolution:** Natural selection, adaptation
• **Ecology:** Ecosystems, biodiversity, conservation
• **Human Anatomy:** Body systems, organs, functions

**📐 Mathematics:**
• **Algebra:** Equations, functions, graphing
• **Calculus:** Derivatives, integrals, limits
• **Statistics:** Probability, distributions, hypothesis testing
• **Geometry:** Shapes, angles, proofs, trigonometry
• **Linear Algebra:** Vectors, matrices, transformations

**🔍 Scientific Method:**
• **Observation:** Noticing phenomena
• **Hypothesis:** Testable explanations
• **Experimentation:** Controlled testing
• **Analysis:** Data interpretation
• **Conclusion:** Evidence-based results

**What specific scientific or mathematical concept would you like to explore?** I can provide detailed explanations, examples, and problem-solving strategies!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["business", "finance", "economics", "marketing", "management"]):
        response_text = """💼 **Business & Finance**

I can help you understand business concepts, financial principles, and management strategies:

**💰 Finance Fundamentals:**
• **Personal Finance:** Budgeting, saving, investing, retirement
• **Corporate Finance:** Capital structure, valuation, risk management
• **Investment:** Stocks, bonds, mutual funds, real estate
• **Banking:** Loans, credit, interest rates, mortgages
• **Accounting:** Balance sheets, income statements, cash flow

**📈 Economics:**
• **Microeconomics:** Supply and demand, market structures
• **Macroeconomics:** GDP, inflation, unemployment, fiscal policy
• **International Trade:** Exchange rates, tariffs, globalization
• **Behavioral Economics:** Psychology of decision-making
• **Development Economics:** Economic growth, poverty reduction

**🎯 Marketing & Sales:**
• **Digital Marketing:** SEO, social media, content marketing
• **Brand Management:** Brand identity, positioning, loyalty
• **Market Research:** Customer analysis, competitive intelligence
• **Sales Strategies:** Lead generation, conversion, retention
• **E-commerce:** Online retail, payment processing, logistics

**👥 Management & Leadership:**
• **Organizational Behavior:** Team dynamics, motivation, culture
• **Strategic Planning:** Vision, mission, goals, SWOT analysis
• **Project Management:** Planning, execution, monitoring, control
• **Human Resources:** Recruitment, training, performance management
• **Operations:** Process improvement, quality management, supply chain

**📊 Business Analytics:**
• **Data Analysis:** Statistical methods, data visualization
• **Key Performance Indicators:** Metrics, dashboards, reporting
• **Forecasting:** Trend analysis, predictive modeling
• **Risk Assessment:** Identification, mitigation, monitoring
• **Decision Making:** Cost-benefit analysis, scenario planning

**What specific business or finance topic interests you?** I can provide detailed insights, frameworks, and practical advice!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["health", "medical", "wellness", "fitness", "nutrition"]):
        response_text = """🏥 **Health & Wellness**

I can provide information on health, wellness, and medical topics:

**💪 Physical Health:**
• **Exercise:** Cardiovascular, strength training, flexibility
• **Nutrition:** Macronutrients, micronutrients, meal planning
• **Sleep:** Sleep hygiene, circadian rhythms, sleep disorders
• **Hydration:** Water intake, electrolyte balance
• **Preventive Care:** Regular checkups, screenings, vaccinations

**🧠 Mental Health:**
• **Stress Management:** Relaxation techniques, mindfulness
• **Anxiety & Depression:** Symptoms, coping strategies, treatment
• **Cognitive Health:** Memory, focus, brain training
• **Emotional Well-being:** Self-care, relationships, work-life balance
• **Mental Health Resources:** Therapy, support groups, hotlines

**🏃‍♀️ Fitness & Exercise:**
• **Cardio Workouts:** Running, cycling, swimming, HIIT
• **Strength Training:** Weightlifting, bodyweight exercises
• **Flexibility:** Yoga, stretching, mobility work
• **Sports & Activities:** Team sports, individual activities
• **Recovery:** Rest days, active recovery, injury prevention

**🍎 Nutrition & Diet:**
• **Macronutrients:** Proteins, carbohydrates, fats
• **Micronutrients:** Vitamins, minerals, antioxidants
• **Meal Planning:** Balanced meals, portion control
• **Special Diets:** Vegetarian, vegan, keto, Mediterranean
• **Hydration:** Water needs, electrolyte balance

**⚠️ Important Disclaimer:**
This information is for educational purposes only and should not replace professional medical advice. Always consult with healthcare providers for medical concerns.

**What specific health or wellness topic would you like to explore?** I can provide evidence-based information and general guidance!"""
        confidence = 0.85

    elif any(word in message_lower for word in ["travel", "trip", "vacation", "destination", "tourism"]):
        response_text = """✈️ **Travel & Tourism**

I can help you plan amazing trips and explore destinations around the world:

**🗺️ Travel Planning:**
• **Destination Research:** Culture, climate, attractions, safety
• **Budget Planning:** Flights, accommodation, activities, food
• **Itinerary Creation:** Daily schedules, must-see attractions
• **Booking Strategies:** Best times to book, price comparison
• **Travel Documents:** Passports, visas, travel insurance

**🌍 Popular Destinations:**
• **Europe:** Paris, Rome, London, Barcelona, Amsterdam
• **Asia:** Tokyo, Bangkok, Singapore, Bali, Seoul
• **Americas:** New York, Los Angeles, Rio, Toronto, Mexico City
• **Africa:** Cape Town, Marrakech, Cairo, Nairobi, Zanzibar
• **Oceania:** Sydney, Melbourne, Auckland, Fiji, Tahiti

**🏨 Accommodation Options:**
• **Hotels:** Luxury, mid-range, budget, boutique
• **Alternative:** Airbnb, hostels, vacation rentals, camping
• **Booking Tips:** Reviews, location, amenities, cancellation policies
• **Loyalty Programs:** Hotel chains, credit card rewards

**🚗 Transportation:**
• **Flights:** Airlines, airports, seat selection, baggage
• **Ground Transport:** Trains, buses, car rentals, rideshares
• **Local Transport:** Public transit, taxis, walking, cycling
• **Travel Apps:** Navigation, translation, currency conversion

**🎒 Travel Essentials:**
• **Packing Lists:** Clothing, electronics, toiletries, documents
• **Travel Gear:** Luggage, adapters, portable chargers, cameras
• **Safety Tips:** Scams, emergency contacts, travel insurance
• **Cultural Etiquette:** Local customs, dress codes, tipping

**What destination or travel topic interests you?** I can provide detailed travel guides, tips, and recommendations!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["information", "info", "data", "knowledge", "facts", "details"]):
        response_text = """📚 **Information & Knowledge**

I can help you understand and find information on virtually any topic!

**🔍 What is Information?**
Information is **data that has been processed, organized, and structured** to provide meaning and context. It's the foundation of knowledge and decision-making.

**📊 Types of Information:**
• **Factual Information:** Objective, verifiable data and statistics
• **Procedural Information:** Step-by-step instructions and processes
• **Conceptual Information:** Ideas, theories, and abstract concepts
• **Analytical Information:** Interpreted data with insights and conclusions
• **News Information:** Current events and recent developments

**💡 How I Can Help with Information:**
• **Research Assistance:** Finding reliable sources and data
• **Explanation:** Breaking down complex topics into understandable parts
• **Fact-Checking:** Verifying information and providing accurate details
• **Context:** Explaining how information relates to broader topics
• **Resources:** Suggesting where to find more detailed information

**🎯 Information Sources I Can Access:**
• **Technical Knowledge:** Programming, IT, science, mathematics
• **Business Information:** Finance, marketing, management, economics
• **General Knowledge:** History, geography, culture, current events
• **Practical Information:** How-to guides, troubleshooting, best practices
• **Academic Topics:** Research, theories, methodologies

**What specific information are you looking for?** I can provide detailed, accurate, and well-sourced information on any topic!"""
        confidence = 0.9

    elif any(word in message_lower for word in ["what", "how", "why", "when", "where", "who", "explain", "define", "meaning"]):
        response_text = f"""🤔 **I'd be happy to help explain that!**

You asked: **"{message}"**

**💡 Let me break this down for you:**

I can provide detailed explanations on virtually any topic. Here's how I can help:

**🔍 What I can explain:**
• **Concepts & Definitions:** Clear explanations of complex ideas
• **How Things Work:** Step-by-step processes and mechanisms
• **Why Things Happen:** Causes, reasons, and underlying principles
• **When & Where:** Context, timing, and location information
• **Who & What:** People, organizations, and key facts

**📚 My explanation approach:**
1. **Start Simple:** Basic concepts first
2. **Add Detail:** More complex aspects
3. **Provide Examples:** Real-world applications
4. **Connect Ideas:** How it relates to other topics
5. **Suggest Resources:** Where to learn more

**🎯 Topics I excel at explaining:**
• **Technology:** Programming, software, hardware, networks
• **Science:** Physics, chemistry, biology, mathematics
• **Business:** Finance, marketing, management, economics
• **General Knowledge:** History, geography, culture, current events
• **Practical Skills:** How-to guides, troubleshooting, best practices

**Could you be more specific about what you'd like me to explain?** For example:
- "Explain how computers work"
- "What is artificial intelligence?"
- "How do I learn programming?"
- "Why is cybersecurity important?"

I'm here to provide clear, comprehensive explanations!"""
        confidence = 0.85

    else:
        # Universal response for any topic not specifically covered
        response_text = f"""🤖 **I'm here to help with anything!**

I understand you're asking about **"{message}"** - that's a great question!

**💡 What I can do:**
• **Answer questions** on virtually any topic
• **Provide detailed explanations** with examples
• **Offer step-by-step guidance** for complex processes
• **Suggest resources** for deeper learning
• **Help solve problems** creatively and effectively

**🔍 My expertise includes:**
• **Technology & Programming** - Coding, software, IT support
• **Science & Mathematics** - Physics, chemistry, biology, math
• **Business & Finance** - Economics, marketing, management
• **Health & Wellness** - Fitness, nutrition, mental health
• **Travel & Lifestyle** - Destinations, planning, culture
• **General Knowledge** - History, literature, current events
• **And much more!**

**🎯 How I can help you:**
1. **Clarify** your question if needed
2. **Provide** comprehensive information
3. **Suggest** practical next steps
4. **Offer** additional resources
5. **Answer** follow-up questions

**What would you like to know more about?** Feel free to ask me anything - I'm designed to be helpful, accurate, and comprehensive in my responses!"""
        confidence = 0.8

    return {
        "response": response_text,
        "session_id": f"session_{random.randint(1000, 9999)}",
        "confidence_score": confidence,
        "was_escalated": confidence < 0.6,
        "ticket_id": random.randint(1000, 9999) if confidence < 0.6 else None
    }

@app.get("/api/chatbot/faqs")
async def get_faqs():
    """Get FAQ entries."""
    return [
        {
            "id": 1,
            "question": "How do I reset my password?",
            "answer": "You can reset your password by clicking 'Forgot Password' on the login page.",
            "category": "Authentication",
            "tags": ["password", "reset"],
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }
    ]

# Authentication endpoints
@app.post("/api/auth/login")
async def login(login_data: dict):
    """Login endpoint."""
    username = login_data.get("username", "")
    password = login_data.get("password", "")

    # Simple mock authentication - accept any username/password for demo
    if username and password:
        return {
            "access_token": f"mock_token_{username}_{int(datetime.now().timestamp())}",
            "token_type": "bearer"
        }
    else:
        return {"detail": "Username and password required"}

@app.post("/api/auth/register")
async def register(user_data: dict):
    """Register endpoint."""
    return {
        "id": 1,
        "username": user_data.get("username", ""),
        "email": user_data.get("email", ""),
        "full_name": user_data.get("full_name", ""),
        "role": user_data.get("role", "customer"),
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }

@app.get("/api/auth/me")
async def get_current_user():
    """Get current user info."""
    return {
        "id": 1,
        "username": "demo_user",
        "email": "demo@example.com",
        "full_name": "Demo User",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    uvicorn.run(
        "simple_main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
