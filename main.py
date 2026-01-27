from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select

# =======================
# 1. 数据库模型 (Models)
# =======================

class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    level: int
    is_locked: bool = Field(default=True)

class LoveNote(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    content: str
    audio_url: Optional[str] = None

# --- 新增：题目表 ---
class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: int
    text: str           # 题目内容，例如 "1, 3, 5, ? 下一个数是多少"
    options: str        # 选项 (我们暂时用逗号分隔的字符串存，例如 "6,7,8,9")
    correct_answer: str # 正确答案，例如 "7"
    hint: str           # 你的爱心提示，例如 "宝宝你看，每次都加了2哦"

# =======================
# 2. 数据库设置
# =======================
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False) # echo=False 让控制台清爽点

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# =======================
# 3. 初始化 App
# =======================
app = FastAPI(title="Her Math API", version="1.1.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# =======================
# 4. 接口编写
# =======================

@app.get("/")
def read_root():
    return {"Message": "API 升级完毕！包含题目功能。"}

# --- Topic 相关 ---
@app.post("/topics/", response_model=Topic)
def create_topic(topic: Topic, session: Session = Depends(get_session)):
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return topic

@app.get("/topics/", response_model=List[Topic])
def read_topics(session: Session = Depends(get_session)):
    topics = session.exec(select(Topic)).all()
    return topics

# --- Question 相关 (新增) ---

# 添加题目
@app.post("/questions/", response_model=Question)
def create_question(question: Question, session: Session = Depends(get_session)):
    session.add(question)
    session.commit()
    session.refresh(question)
    return question

# 获取某个知识点下的所有题目
@app.get("/topics/{topic_id}/questions", response_model=List[Question])
def read_questions(topic_id: int, session: Session = Depends(get_session)):
    # 查询 topic_id 匹配的所有题目
    questions = session.exec(select(Question).where(Question.topic_id == topic_id)).all()
    return questions

# =======================
# 笔记接口 (LoveNote)
# =======================

@app.post("/notes/", response_model=LoveNote)
def create_note(note: LoveNote, session: Session = Depends(get_session)):
    session.add(note)
    session.commit()
    session.refresh(note)
    return note

@app.get("/topics/{topic_id}/notes", response_model=List[LoveNote])
def read_notes(topic_id: int, session: Session = Depends(get_session)):
    # 从数据库里找对应 topic_id 的笔记
    notes = session.exec(select(LoveNote).where(LoveNote.topic_id == topic_id)).all()
    return notes

    # =======================
# 6. 删除笔记接口 (Delete Note)
# =======================

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: Session = Depends(get_session)):
    # 1. 在数据库里找这条笔记
    note = session.get(LoveNote, note_id)
    
    # 2. 如果没找到，报错
    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")
        
    # 3. 找到了，删除！
    session.delete(note)
    session.commit()
    return {"ok": True}