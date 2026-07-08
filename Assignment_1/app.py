import streamlit as st

st.set_page_config(
    page_title="Identity Echo Interface",
    layout="centered",
    initial_sidebar_state="expanded",
)

def main() -> None:
    """Entry point — render the full Identity Echo Interface."""

    # ── Title & description ──
    st.title("Identity Echo Interface")

    st.write(
        "Welcome to the **Identity Echo Interface** — a secure transmission portal. "
        "Enter your **name** and a **message** below, then click **Transmit** to send "
        "your signal. The system will echo your identity, confirm receipt, and run a "
        "quick token analysis on your message."
    )

    st.divider()

    # ── Input Section ──
    st.subheader("Transmission Console")

    # Both fields use st.text_input() as required by the assignment.
    name: str = st.text_input(
        label="Your Name",
        placeholder="e.g. Ada Lovelace",
        help="Enter the name you wish to transmit.",
    )

    message: str = st.text_input(
        label="Your Message",
        placeholder="e.g. Hello from the future!",
        help="Enter the message you wish to transmit.",
    )

    st.write("")  # Spacing

    transmit_clicked: bool = st.button("Transmit")

    st.divider()

    # ── Processing logic — runs ONLY after button click ──
    if transmit_clicked:
        # Strip leading/trailing whitespace before validation.
        clean_name: str = name.strip()
        clean_message: str = message.strip()

        # ── Validation: if / elif / else ──
        if not clean_name:
            st.error("Please provide your name.")

        elif not clean_message:
            st.warning("Please type a message to transmit.")

        else:
            # ── Successful transmission ──
            st.success(
                f"Transmission successful! Greetings, **{clean_name}**. "
                f"We received your message: *{clean_message}*"
            )

            # ── Advanced Challenge — Analytics ──
            char_count: int = len(clean_message)
            token_count: float = round(char_count / 4, 2)

            st.info(
                f"System Check: Your message will consume approximately "
                f"**{token_count}** tokens from our context window."
            )

            st.write("")  # Spacing

            # ── Metric Cards ──
            st.subheader("Transmission Analytics")
            col_left, col_right = st.columns(2)

            with col_left:
                st.metric(
                    label="Character Count",
                    value=char_count,
                    help="Total characters in your message (excluding leading/trailing spaces).",
                )

            with col_right:
                st.metric(
                    label="Estimated Tokens",
                    value=f"{token_count}",
                    help="Approximation: characters ÷ 4.",
                )

if __name__ == "__main__":
    main()

# ── Author ──
st.subheader("Author")
st.markdown(
    """
    **Name:** "Hemendra Sharma"<br>
    **Role:** "AI Builder Intern"<br>
    **Organization:** "Mirai Virtual Summer Internship 2026"
    """,
    unsafe_allow_html=True,
)
st.caption("© 2026 Identity Echo Interface")