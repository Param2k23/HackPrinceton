-----

# ❤️ HeartBridgeAI: Nurturing Family Well-being with AI

**HeartBridgeAI** is an innovative, AI-powered platform designed to strengthen **family connection** and support the **emotional well-being** of parents and teens. Leveraging empathetic AI agents, personalized activity suggestions, and a supportive web interface, we aim to bridge emotional gaps, reduce parental burnout, and provide crucial mental health support for the entire family.

## 🌟 The Inspiration: A Need for Connection

Our project stems from personal experiences and compelling research highlighting the challenges in modern family life:

  * **Parental Burnout & Isolation:** Research shows two-thirds (66%) of parents feel isolated or lonely, and 62% feel burned out. Nearly 4 in 5 (79%) would value a way to connect with other parents.
  * **Teen Social Support Gap:** Only 58.5% of U.S. teens consistently receive the social and emotional support they need (CDC, 2024).
  * **Distance and Mental Health:** Personal challenges, including the stress of long-distance relationships for international students, underscore the need for proactive mental health tools.

HeartBridgeAI is built on the foundation that **social support** and **strong family bonds** are critical for mental health.

-----

## 💻 Features: What We Built

HeartBridgeAI is composed of a multi-agent system, an intelligent event scheduler, and a supportive web application.

### 1\. AI Agent for Emotional Well-Being

Our core component, providing empathetic, context-aware support via **voice and text**.

  * **Empathetic Voice:** Utilizes the **Eleven Labs API** for natural, empathetic, and human-like voice interactions.
  * **Contextual Understanding:** Powered by **Grok AI** to accurately understand conversation context, intent, and emotional content.
  * **Mental Health Guardian:** Integrates the **Google Gemini API** to analyze children's messages for mood and severity. It notifies parents of potential mental health concerns in a timely manner while **maintaining the child's privacy**.
  * **Multi-Agent Coordination:** Ensures seamless, context-aware support and guidance for mental well-being.

### 2\. Event Suggestions for Positive Engagement

An intelligent system designed to turn passive interests into active, bonding family time.

  * **Personalized Recommendations:** Collects interests via the AI agent and uses the **Amazon Nova SDK** to suggest activities, classes, or sports that promote both **mental and physical health**.
  * **Seamless Scheduling:** Integrates with the **Google Calendar API** to easily schedule activities, reducing stress and encouraging positive parent-child bonding.

### 3\. Web App for Monitoring and Support

A central dashboard providing transparency and a space for positive memory reinforcement.

  * **Interactive Dashboard:** Displays important **AI notifications**, summarized **child mood reports**, and actionable **suggested activities**.
  * **Family Memories Page:** A space to reinforce positive shared moments and emotional connections.
  * **Family Tree Visualization:** Helps visualize and understand family relationships and emotional dynamics.
  * **Easy Access:** Enables seamless interaction with the AI agent via voice or text.

-----

## 🛠️ Tech Stack

| Layer | Tools & APIs | Purpose |
| :--- | :--- | :--- |
| **AI Agent (Voice & Text)** | Grok AI, Eleven Labs API | Contextual understanding & natural voice generation |
| **Mood & Severity Analysis**| Google Gemini API | Emotional detection & privacy-preserving alerts |
| **Event Discovery** | Amazon Nova SDK | Suggesting health-positive activities/classes |
| **Calendar Integration** | Google Calendar API | Scheduling family activities |
| **Database** | PostgreSQL | Secure data storage for relationships and mood data |
| **Frontend** | React.js / Web App | Interactive dashboard and user interface |
| **Backend** | Python | Core logic, API orchestration |

-----

## 🧠 Technical Challenges & Solutions

| Challenge | Description | Lessons Learned / Solution |
| :--- | :--- | :--- |
| **Database & Emotional Data** | Securely storing sensitive family relationship and mood data while prioritizing privacy. | Leveraged **PostgreSQL** for scalability and structured data management, with strict access control. |
| **Multi-Agent Coordination** | Coordinating multiple AI agents to maintain emotional context and respond empathetically. | Designed a **central state management system** to pass context and emotional information between agents effectively. |
| **Mood Detection & Privacy** | Detecting nuanced emotions using the Gemini API while strictly protecting child privacy. | Implemented a **privacy-by-design** approach: only severity-level alerts (not raw message content) are shared with parents. |
| **Activity Recommendation** | Suggesting activities that are relevant *and* demonstrably positive for mental/physical health. | Integrated the **Amazon Nova SDK** with a custom filtering layer focused on well-being parameters. |

-----

## 🚀 Future Directions

  * **Mobile App Development:** Create an iOS and Android version for on-the-go family engagement and mental health support.
  * **Proactive Conversation Prompts:** Implement AI-generated suggestions for meaningful conversations based on mood trends and emotional data.
  * **Professional Resource Integration:** Seamlessly integrate with external mental health resources and family counseling tools for professional, proactive support when needed.

-----

-----

## 📄 License

This project is licensed under the [Specify your license, e.g., MIT License] - see the `LICENSE` file for details.
