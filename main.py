import streamlit as st
from openai import OpenAI
client = OpenAI(api_key='YOUR API KEY')

assistant = client.beta.assistants.retrieve(assistant_id='asst_jof6eifkF6XAZiYW5OcGrZGQ')

st.title("Wendy's Drive Thru Assistant")
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = None

# Display chat history

for message in st.session_state['messages']:
    st.write(f"**{message['role']}:** {message['content']}")

prompt = st.text_input("Order Here")

if st.button("Send") and prompt:
    if st.session_state['thread_id'] is None:
        # Create a new thread if it doesn't exist
        thread = client.beta.threads.create(
            messages=[{
                'role': 'user',
                'content': prompt
            }]
        )
        st.session_state['thread_id'] = thread.id
    else:
        # Reuse the existing thread_id
        thread_id = st.session_state['thread_id']
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role='user',
            content=prompt
        )

    # Add user message to the session state
    st.session_state['messages'].append({'role': 'Customer', 'content': prompt})
    
    # Create a run using the existing thread_id
    run = client.beta.threads.runs.create_and_poll(
        thread_id=st.session_state['thread_id'],
        assistant_id=assistant.id
    )
    
    messages = list(client.beta.threads.messages.list(
        thread_id=st.session_state['thread_id'],
        run_id=run.id
    ))
    message_content = messages[0].content[0].text
    
    # Add bot message to the session state
    st.session_state['messages'].append({'role': 'Bot', 'content': message_content.value})
    
    #Display bot response.
    st.write(f"**Bot:** {message_content.value}")
