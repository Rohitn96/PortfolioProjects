from langchain_helper import get_few_shot_db_chain
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Shirt Happens: Inventory Management", page_icon="📦")

# Add a title and description for the in-house team
st.title("📦 Shirt Happens: Inventory Management Q&A")
st.write("Use this tool to get quick answers about the T-shirt inventory. Enter your questions below.")

# User input section with a text input and submit button
question = st.text_input("Enter your question about the inventory:", placeholder="e.g., How many red T-shirts are in stock?")

# Submit button
if st.button("Submit"):
    if question:
        chain = get_few_shot_db_chain()
        response = chain.run(question)

        # Display the answer in a clear format
        st.header("Answer")
        st.write(response)
    else:
        st.error("Please enter a question before submitting.")


# Optional: Add a footer with contact information for support
st.markdown("---")
st.write("For further assistance, please contact the inventory management team.")