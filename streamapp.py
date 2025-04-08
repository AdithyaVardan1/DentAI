import streamlit as st
from agno.agent import Agent
from agno.models.groq import Groq
from agno.storage.agent.sqlite import SqliteAgentStorage
from dotenv import load_dotenv
import time
import datetime

load_dotenv()

def create_agent(session_id=None):
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        storage=SqliteAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db"),
        add_history_to_messages=True,
        num_history_responses=3,
        description=f"""You are a friendly and professional virtual receptionist for 'Cavity Dental Clinic'. 
                        Start every response with the most relevant answer, followed by concise bullet points using emojis. Follow the Minto Pyramid Principle: 
                        → Lead with the main message.
                        → Group related details.
                        → Be brief and structured.

                        Your responsibilities:
                        • 📅 Book appointments (Ask for name, contact number, preferred date & time)
                        • 🦷 Share dental services in grouped, easy-to-scan bullets:
                        - 🧼 Preventive: Cleaning, checkups, fluoride
                        - 😁 Cosmetic: Whitening, veneers, smile design
                        - 🦷 Orthodontic: Braces, aligners
                        • 🙋 Answer FAQs with clear, short answers

                        Avoid long paragraphs. Use friendly emojis. Confirm bookings with exact dates.
                        Today's date: {datetime.datetime.now().strftime('%Y-%m-%d')}.""",
        session_id=session_id
    )

def main():
    st.set_page_config(page_title="Cavity Dental Clinic Receptionist", page_icon="🦷")
    
    st.title("🦷 Cavity Dental Clinic")
    st.subheader("Virtual Receptionist Chat")
    
    # Initialize session state
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'available_sessions' not in st.session_state:
        st.session_state.available_sessions = []
    if 'selected_session' not in st.session_state:
        st.session_state.selected_session = None
    
    # Sidebar controls
    with st.sidebar:
        st.header("Session Management")
        
        # Session selection
        st.session_state.available_sessions = get_all_session_ids()
        selected_session = st.selectbox(
            "Available Sessions",
            options=[""] + st.session_state.available_sessions,
            format_func=lambda x: "Select a session..." if x == "" else x
        )
        
        if selected_session:
            st.session_state.selected_session = selected_session
        
        if st.button("Load Selected Session"):
            if st.session_state.selected_session:
                load_session(st.session_state.selected_session)
        
        if st.button("New Session"):
            new_session()
        
        st.markdown("---")
        st.markdown("### Instructions:")
        st.markdown("1. Select a session to resume")
        st.markdown("2. Or create a new session")
        st.markdown("3. Type your message in the chat box")
        st.markdown("4. Type 'exit', 'quit', or 'bye' to end")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if st.session_state.agent and (prompt := st.chat_input("Type your message...")):
        if prompt.lower() in ["exit", "quit", "bye"]:
            st.session_state.messages.append({"role": "assistant", "content": "Thank you for visiting Cavity Dental Clinic. Have a great day!"})
            st.rerun()
        else:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get agent response
            with st.chat_message("assistant"):
                run_response = st.session_state.agent.run(prompt)
                response_content = run_response.content
                
                # Simulate streaming effect
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response_content.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

def get_all_session_ids():
    """Get all available session IDs from storage"""
    storage = SqliteAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db")
    return storage.get_all_session_ids()

def load_session(session_id):
    """Load an existing session with proper AgentSession handling"""
    try:
        st.session_state.agent = create_agent(session_id)
        st.session_state.messages = []
        
        storage = SqliteAgentStorage(table_name="agent_sessions", db_file="tmp/agent_storage.db")
        session_data = storage.read(session_id)
        
        if not session_data:
            st.warning(f"No session data found for ID: {session_id}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Welcome to Cavity Dental Clinic! How can I assist you today?"
            })
            return
        
        messages = []
        
        if session_data.memory and 'runs' in session_data.memory:
            for run in session_data.memory['runs']:
                # Add user message
                if 'message' in run:
                    messages.append({
                        "role": run['message']['role'],
                        "content": run['message']['content']
                    })
                # Add assistant response
                if 'response' in run and 'content' in run['response']:
                    messages.append({
                        "role": "assistant",
                        "content": run['response']['content']
                    })
        
        for msg in messages:
            st.session_state.messages.append({
                "role": "user" if msg['role'].lower() == "user" else "assistant",
                "content": msg['content']
            })
        
        if not st.session_state.messages:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Welcome to Cavity Dental Clinic! How can I assist you today?"
            })
        
        st.success(f"Session loaded successfully! Found {len(messages)} previous messages")
        
    except Exception as e:
        st.error(f"Error loading session: {str(e)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Welcome to Cavity Dental Clinic! How can I assist you today?"
        })

def new_session():
    """Create a new session"""
    st.session_state.agent = create_agent()
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to Cavity Dental Clinic! How can I assist you today?"}
    ]
    st.session_state.selected_session = st.session_state.agent.session_id
    st.success("New session created!")

if __name__ == "__main__":
    main()