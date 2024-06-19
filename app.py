# app.py
import streamlit as st
from sqlalchemy.orm import Session
from db import SessionLocal, User, ToDo

def get_user(session, email):
    return session.query(User).filter(User.email == email).first()

def create_user(session, name, email, password):
    user = User(name=name, email=email, password=password)
    session.add(user)
    session.commit()
    return user

def get_todos(session, user):
    return session.query(ToDo).filter(ToDo.user_id == user.id).all()

def create_todo(session, title, description, user):
    todo = ToDo(title=title, description=description, user_id=user.id)
    session.add(todo)
    session.commit()
    return todo

def delete_todo(session, todo_id):
    todo = session.query(ToDo).filter(ToDo.id == todo_id).first()
    session.delete(todo)
    session.commit()

def main():
    st.title("ToDoアプリ")

    session = SessionLocal()

    menu = ["登録", "ログイン", "ダッシュボード"]
    choice = st.sidebar.selectbox("メニュー", menu)

    if choice == "登録":
        st.subheader("新規ユーザー登録")
        name = st.text_input("名前")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type='password')
        if st.button("登録"):
            create_user(session, name, email, password)
            st.success("ユーザー登録が完了しました。")

    elif choice == "ログイン":
        st.subheader("ログイン")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type='password')
        if st.button("ログイン"):
            user = get_user(session, email)
            if user and user.password == password:
                st.session_state["user"] = user
                st.success("ログイン成功")
            else:
                st.error("メールアドレスまたはパスワードが間違っています。")

    elif choice == "ダッシュボード":
        if "user" in st.session_state:
            user = st.session_state["user"]
            st.subheader(f"ようこそ、{user.name}さん")

            todos = get_todos(session, user)
            for todo in todos:
                st.write(f"{todo.title} - {todo.description}")
                if st.button(f"削除 {todo.title}", key=todo.id):
                    delete_todo(session, todo.id)
                    st.experimental_rerun()

            st.subheader("新しいToDoを追加")
            title = st.text_input("タイトル")
            description = st.text_area("詳細")
            if st.button("追加"):
                create_todo(session, title, description, user)
                st.experimental_rerun()
        else:
            st.warning("ログインしてください。")

if __name__ == '__main__':
    main()
