# Dental Clinic Bot

## **Project Overview**

The goal of this project is to develop an AI-powered dental clinic booking bot that is intuitive, user-friendly, and emotionally engaging. The bot will handle appointment scheduling, gather patient details, and provide a seamless confirmation process via WhatsApp. The bot will be designed to feel human-like, with natural conversational abilities and empathy.

## **Key Features**

1. **Natural Language Interaction**:
    - The bot will use a conversational tone, asking about the user’s well-being and gathering details like:
        - Name, age, and contact information (if not specified)
        - Reason for the appointment (e.g., cleaning, cavity, braces, etc.).
        - Preferred date and time for the appointment.
    - It will handle edge cases (e.g., rescheduling, cancellations) gracefully.
2. **Appointment Availability Check**:
    - The bot will check a predefined database (simulated initially) to verify if the requested time slot is available.
3. **Confirmation and Reminders**:
    - Once the appointment is booked, the bot will:
        - Send a confirmation message via WhatsApp.
        - Provide an "Add to Calendar" feature for reminders (google calendar for simulation).

## **Tools and Technologies**

1. **AI Framework**:
    - **Phidata AI Agent Framework**: For orchestrating agents and functions.
    - **Qwen 2.5 (32B)**: As the primary LLM for natural language understanding and generation.
    - **Groq API**: For hosting and running the LLM with high performance.
2. **Backend and Deployment**:
    - **FastAPI**: For creating RESTful endpoints to handle bot interactions.
    - **Lightning AI Platform**: For deployment and testing.
3. **Messaging and Notifications**:
    - **WhatsApp API**: For sending appointment confirmations and reminders.
    - **Calendar Integration**: For the "Add to Calendar" feature.
4. **Database**:
    - A simulated database (initially) to check appointment availability.
5. **Prompting Strategy**:
    - **ReAct (Reasoning and Acting) or chain of thought prompting**: To enable the bot to reason through tasks and take actions (e.g., checking availability, sending messages).
    - **Function Calling**: To integrate tools like database checks and WhatsApp notifications.

## **Deliverables**

1. **Functional AI Bot**:
    - A fully functional bot that can handle appointment scheduling, confirmation, and reminders.
2. **API Endpoints**:
    - FastAPI endpoints for bot interactions.
3. **Documentation**:
    - Technical documentation for the bot’s architecture, setup, and usage.
    - User guide for the client.
4. **Test Results**:
    - Performance metrics and user feedback from the testing phase.

## **Timeline**

| **Phase** | **Duration** | **Deliverables** |
| --- | --- | --- |
| Setup and Prototyping | Day 1 | Basic bot with conversational flow and tools. |
| Refinement and Testing | Day 2 | Refined bot with end points for testing. |
| Final Deployment | Day 3 | Fully deployed bot and documentation. |
```
