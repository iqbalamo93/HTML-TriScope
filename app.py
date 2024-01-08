import streamlit as st


def main():
    st.title("HTML Link Collector")

    # Sidebar for input fields
    with st.sidebar:
        st.header("Enter  Target URLs")
        # Initialize an empty array to store links
        links = []

        # Input fields for links
        link1 = st.text_input("Link 1")
        link2 = st.text_input("Link 2")
        link3 = st.text_input("Link 3")
        # Submit button
        submit_button = st.button("Submit")

        if submit_button:
            if link1:
                links.append(link1)
            if link2:
                links.append(link2)
            if link3:
                links.append(link3)

            # Display the collected links on the main page
    
    st.subheader("Collected Links")
    for index, link in enumerate(links):
        st.write(f"Link {index+1}: {link}")


if __name__ == "__main__":
    main()
