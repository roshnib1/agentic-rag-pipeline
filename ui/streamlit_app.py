import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.loader import load_pdfs
from vectorstore.indexer import create_index, load_index
from core.graph import run_agent
from agents.quiz_generator import generate_quiz
from agents.quiz_state import init_quiz_state

st.set_page_config(
    page_title="Doc Research Agent",
    page_icon="🔍",
    layout="wide"
)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "indexed" not in st.session_state:
    st.session_state.indexed = False
if "mode" not in st.session_state:
    st.session_state.mode = "Chat"
if "quiz" not in st.session_state:
    st.session_state.quiz = init_quiz_state()
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

# Sidebar
with st.sidebar:
    st.header("📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Index Documents", type="primary"):
            with st.spinner("Loading and indexing PDFs..."):
                docs = load_pdfs(uploaded_files)
                create_index(docs)
                st.session_state.indexed = True
                st.success(f"Indexed {len(docs)} chunks from {len(uploaded_files)} PDF(s)!")

    st.divider()

    if st.session_state.indexed:
        st.success("✅ Documents ready")
    else:
        st.warning("⚠️ No documents indexed yet")

    st.divider()

    # Mode selector
    st.header("🔀 Mode")
    mode = st.radio("Select mode", ["Chat", "Quiz", "Evaluate"], 
                    index=["Chat", "Quiz", "Evaluate"].index(st.session_state.mode))
    st.session_state.mode = mode

    if mode == "Chat":
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    if mode == "Quiz":
        st.divider()
        st.header("⚙️ Quiz Settings")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        num_questions = st.selectbox("Number of questions", [5, 10, 15])

        if st.button("Generate Quiz", type="primary"):
            if not st.session_state.indexed:
                st.error("Please index documents first!")
            else:
                with st.spinner("Generating quiz..."):
                    vectorstore = load_index()
                    docs = vectorstore.similarity_search(
                        "key concepts and important information", k=8
                    )
                    context = [doc.page_content for doc in docs]
                    questions = generate_quiz(
                        context, difficulty, num_questions, "mixed"
                    )
                    if questions:
                        st.session_state.quiz = init_quiz_state()
                        st.session_state.quiz["questions"] = questions
                        st.session_state.quiz_started = True
                        st.success(f"Generated {len(questions)} questions!")
                        st.rerun()
                    else:
                        st.error("Failed to generate quiz. Try again!")

        if st.session_state.quiz_started:
            if st.button("Reset Quiz"):
                st.session_state.quiz = init_quiz_state()
                st.session_state.quiz_started = False
                st.rerun()

# ─── CHAT MODE ───
if st.session_state.mode == "Chat":
    st.title("🔍 Agentic Document Research Assistant")
    st.caption("Upload multiple PDFs and ask complex questions across all of them")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "sources" in message and message["sources"]:
                with st.expander("📚 Sources"):
                    for source in set(message["sources"]):
                        st.write(f"• {source}")

    question = st.chat_input("Ask a question about your documents...")

    if question:
        if not st.session_state.indexed:
            st.error("Please upload and index documents first!")
        else:
            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = run_agent(question, st.session_state.chat_history)
                    answer = result["answer"]
                    sources = list(set(result["sources"]))
                st.write(answer)
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            st.write(f"• {source}")

            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.chat_history.append({
                "role": "assistant", "content": answer, "sources": sources
            })

# ─── QUIZ MODE ───
elif st.session_state.mode == "Quiz":
    st.title("🧠 Quiz Mode")

    if not st.session_state.quiz_started:
        st.info("👈 Configure your quiz settings in the sidebar and click 'Generate Quiz'")

    else:
        quiz = st.session_state.quiz
        questions = quiz["questions"]
        current = quiz["current_index"]
        total = len(questions)

        # ── Completed ──
        if quiz["completed"]:
            score = quiz["score"]
            st.balloons()
            st.title("🎉 Quiz Complete!")

            # Score card
            percentage = (score / total) * 100
            col1, col2, col3 = st.columns(3)
            col1.metric("Score", f"{score}/{total}")
            col2.metric("Percentage", f"{percentage:.0f}%")
            if percentage >= 80:
                col3.metric("Grade", "🏆 Excellent")
            elif percentage >= 60:
                col3.metric("Grade", "👍 Good")
            else:
                col3.metric("Grade", "📚 Keep Studying")

            st.divider()

            # Review all answers
            st.subheader("📝 Review Answers")
            for i, (q, user_ans) in enumerate(zip(questions, quiz["answers"])):
                correct = q["answer"]
                is_correct = str(user_ans).strip().upper() == str(correct).strip().upper()
                icon = "✅" if is_correct else "❌"

                with st.expander(f"{icon} Q{i+1}: {q['question'][:80]}..."):
                    st.write(f"**Question:** {q['question']}")
                    if q["type"] == "mcq":
                        for key, val in q["options"].items():
                            if key == correct:
                                st.markdown(f"**{key}. {val} ✅ (Correct)**")
                            elif key == user_ans:
                                st.markdown(f"~~{key}. {val}~~ ❌ (Your answer)")
                            else:
                                st.write(f"{key}. {val}")
                    else:
                        st.write(f"**Your answer:** {user_ans}")
                        st.write(f"**Correct answer:** {correct}")
                    st.info(f"💡 {q['explanation']}")

        # ── Active Quiz ──
        else:
            # Progress bar
            progress = current / total
            st.progress(progress, text=f"Question {current + 1} of {total}")

            q = questions[current]
            st.subheader(f"Q{current + 1}: {q['question']}")

            # MCQ
            if q["type"] == "mcq":
                options = [f"{k}. {v}" for k, v in q["options"].items()]
                selected = st.radio("Choose your answer:", options, key=f"q_{current}")
                selected_key = selected[0] if selected else None

                if st.button("Submit Answer", key=f"submit_{current}"):
                    quiz["answers"].append(selected_key)
                    if selected_key == q["answer"]:
                        quiz["score"] += 1
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Wrong! Correct answer: {q['answer']}. {q['options'][q['answer']]}")
                    st.info(f"💡 {q['explanation']}")

                    if current + 1 >= total:
                        quiz["completed"] = True
                    else:
                        quiz["current_index"] += 1

                    st.session_state.quiz = quiz
                    import time
                    time.sleep(1.5)
                    st.rerun()

            # True/False
            elif q["type"] == "truefalse":
                selected = st.radio("Choose your answer:", ["True", "False"], key=f"q_{current}")

                if st.button("Submit Answer", key=f"submit_{current}"):
                    quiz["answers"].append(selected)
                    if selected == q["answer"]:
                        quiz["score"] += 1
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Wrong! Correct answer: {q['answer']}")
                    st.info(f"💡 {q['explanation']}")

                    if current + 1 >= total:
                        quiz["completed"] = True
                    else:
                        quiz["current_index"] += 1

                    st.session_state.quiz = quiz
                    import time
                    time.sleep(1.5)
                    st.rerun()

# ─── EVALUATE MODE ───
elif st.session_state.mode == "Evaluate":
    st.title("📊 RAGAS Evaluation")
    st.caption("Evaluate your RAG pipeline quality")

    eval_q1 = st.text_input("Test question 1", placeholder="e.g. What is the main topic?")
    eval_q2 = st.text_input("Test question 2", placeholder="e.g. What are the key findings?")
    eval_q3 = st.text_input("Test question 3", placeholder="Optional")

    if st.button("Run RAGAS Evaluation", type="primary"):
        if not st.session_state.indexed:
            st.error("Please index documents first!")
        elif not eval_q1:
            st.error("Please enter at least 1 test question!")
        else:
            test_questions = [q for q in [eval_q1, eval_q2, eval_q3] if q.strip()]
            with st.spinner(f"Evaluating {len(test_questions)} question(s)... this may take a minute"):
                from evaluation.evaluator import run_evaluation
                df = run_evaluation(test_questions)
                st.success("Evaluation complete!")
                st.dataframe(df)
                cols = df.columns.tolist()
                if "faithfulness" in cols:
                    col1, col2 = st.columns(2)
                    faith_val = df["faithfulness"].mean()
                    col1.metric("Avg Faithfulness", f"{faith_val:.2f}")
                    if "answer_relevancy" in cols:
                        rel_val = df["answer_relevancy"].mean()
                        if pd.isna(rel_val):
                            col2.metric("Avg Answer Relevancy", "N/A")
                        else:
                            col2.metric("Avg Answer Relevancy", f"{rel_val:.2f}")