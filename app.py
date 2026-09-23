import streamlit as st
from assistant import create_assistant
from db_feedback import save_feedback
from db_save import save_conversation


# Cache the assistant instance so it persists across reruns without reloading models
@st.cache_resource
def get_assistant():
    return create_assistant()


assistant = get_assistant()

st.title("Course Assistant")

# Text input with explicit key
user_input = st.text_input("Enter your question:", key="user_question_input")

# Main action button with explicit key
if st.button("Ask", key="btn_ask_question"):
    if user_input.strip():
        with st.spinner("Processing..."):
            answer = assistant.rag(user_input)
            st.success("Completed!")
            st.write(answer)

            # Extract metrics from the last call
            record = assistant.last_call
            st.write(f"Response time: {record.response_time:.2f}s")
            st.write(f"Prompt tokens: {record.prompt_tokens}")
            st.write(f"Completion tokens: {record.completion_tokens}")
            st.write(f"Cost: ${record.cost:.4f}")

            # Save conversation to PostgreSQL and retain the ID in session state
            conversation_id = save_conversation(
                record, user_input, "llm-zoomcamp"
            )
            st.session_state["conversation_id"] = conversation_id
    else:
        st.warning("Please enter a question first.")

# Feedback section — checks session_state outside the button block so it stays visible
conversation_id = st.session_state.get("conversation_id")

if conversation_id is not None:
    st.write("---")
    st.write("Was this response helpful?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("+1", key=f"feedback_up_{conversation_id}"):
            save_feedback(conversation_id, "user", score=1)
            st.success("Thanks for the positive feedback!")

    with col2:
        if st.button("-1", key=f"feedback_down_{conversation_id}"):
            save_feedback(conversation_id, "user", score=-1)
            st.success("Thanks for the feedback!")