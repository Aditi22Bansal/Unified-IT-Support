from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime
import random
import json

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

def get_intelligent_response(message: str) -> str:
    """Get intelligent response using pattern matching and knowledge base"""
    message_lower = message.lower().strip()

    # Greetings and basic interactions
    if any(word in message_lower for word in ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]):
        return """👋 **Hello! I'm your AI IT Support Assistant**

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

    # IT Support Topics
    elif any(word in message_lower for word in ["password", "reset", "forgot", "login", "access", "account"]):
        return """🔐 **Password & Account Help**

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

    elif any(word in message_lower for word in ["vpn", "remote", "connect", "network", "virtual private network"]):
        return """🌐 **VPN & Network Connectivity**

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

    elif any(word in message_lower for word in ["slow", "performance", "lag", "freeze", "hanging", "optimize"]):
        return """⚡ **Performance Optimization & Troubleshooting**

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

    elif any(word in message_lower for word in ["software", "install", "application", "program", "app"]):
        return """💻 **Software Installation & Management**

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

    elif any(word in message_lower for word in ["cybersecurity", "security", "hack", "malware", "virus", "phishing"]):
        return """🛡️ **Cybersecurity & Information Security**

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

    elif any(word in message_lower for word in ["programming", "code", "development", "python", "javascript", "java", "coding"]):
        return """💻 **Programming & Software Development**

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

    elif any(word in message_lower for word in ["information", "info", "data", "knowledge", "facts", "details"]):
        return """📚 **Information & Knowledge**

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

    elif any(word in message_lower for word in ["what", "how", "why", "when", "where", "who", "explain", "define", "meaning"]):
        return f"""🤔 **I'd be happy to help explain that!**

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

    # Default intelligent response
    else:
        return f"""🤖 **I'm here to help with anything!**

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
        "status": "operational"
    }

@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics():
    """Get comprehensive dashboard metrics."""
    return {
        "system_health": {
            "cpu_usage": round(random.uniform(20, 80), 1),
            "memory_usage": round(random.uniform(30, 90), 1),
            "disk_usage": round(random.uniform(10, 70), 1),
            "uptime_hours": round(random.uniform(24, 168), 1),
            "active_alerts": random.randint(0, 5),
            "status": "operational"
        },
        "tickets": {
            "total": random.randint(50, 200),
            "open": random.randint(10, 50),
            "resolved_today": random.randint(5, 25),
            "avg_resolution_time": f"{random.randint(2, 48)} hours"
        },
        "alerts": [
            {
                "id": random.randint(1000, 9999),
                "type": random.choice(["warning", "error", "info"]),
                "message": random.choice([
                    "High CPU usage detected",
                    "Memory usage above threshold",
                    "Disk space running low",
                    "Network connectivity issue",
                    "Service restart required"
                ]),
                "timestamp": datetime.now().isoformat(),
                "severity": random.choice(["low", "medium", "high", "critical"])
            }
            for _ in range(random.randint(0, 5))
        ]
    }

@app.post("/api/tickets/create")
async def create_ticket(ticket_data: dict):
    """Create a new support ticket."""
    return {
        "id": random.randint(100, 999),
        "title": ticket_data.get("title", "New Ticket"),
        "description": ticket_data.get("description", ""),
        "priority": ticket_data.get("priority", "medium"),
        "status": "open",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resolved_at": None
    }

@app.post("/api/chatbot/chat")
async def chat_with_bot(chat_data: dict):
    """Chat with the intelligent assistant using pattern matching."""
    message = chat_data.get("message", "").strip()

    if not message:
        return {
            "response": "Please enter a message to start our conversation!",
            "session_id": f"session_{random.randint(1000, 9999)}",
            "confidence_score": 0.5,
            "was_escalated": False,
            "ticket_id": None
        }

    # Get intelligent response using pattern matching
    response_text = get_intelligent_response(message)

    # Calculate confidence based on response length and content
    confidence = min(0.95, max(0.7, len(response_text) / 1000))

    return {
        "response": response_text,
        "session_id": f"session_{random.randint(1000, 9999)}",
        "confidence_score": confidence,
        "was_escalated": False,
        "ticket_id": None
    }

@app.get("/api/chatbot/faqs")
async def get_faqs():
    """Get FAQ entries."""
    return [
        {
            "id": 1,
            "question": "How do I reset my password?",
            "answer": "Click 'Forgot Password' on the login page and follow the email instructions.",
            "category": "Account"
        },
        {
            "id": 2,
            "question": "How do I connect to VPN?",
            "answer": "Download the VPN client from the IT portal and use your company credentials.",
            "category": "Network"
        },
        {
            "id": 3,
            "question": "What are the support hours?",
            "answer": "IT support is available Monday-Friday, 8 AM - 6 PM. Emergency support is 24/7.",
            "category": "General"
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
        "simple_main_fallback:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
