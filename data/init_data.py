from sqlmodel import Session, create_engine, select
from main import Topic, Question, LoveNote, sqlite_url # 引入我们刚才写的类

# 连接数据库
engine = create_engine(sqlite_url)

def init_db():
    with Session(engine) as session:
        # 1. 检查是否已经有数据，防止重复添加
        existing = session.exec(select(Topic)).first()
        if existing:
            print("数据库里已经有数据了，跳过初始化。")
            return

        # 2. 创建第一个知识点：等差数列
        topic1 = Topic(title="第一章：高斯的糖果 (等差数列)", level=1, is_locked=False)
        session.add(topic1)
        session.commit()
        session.refresh(topic1)
        
        print(f"创建知识点: {topic1.title}")

        # 3. 创建你的“爱心笔记”
        note = LoveNote(
            topic_id=topic1.id,
            content="宝宝，等差数列其实就是排排坐分果果，每个人比前一个人多拿固定的数量。别怕，我们先从找规律开始！"
        )
        session.add(note)

        # 4. 创建拆解式题目 (3道题，由浅入深)
        
        # 第1题：找规律 (建立信心)
        q1 = Question(
            topic_id=topic1.id,
            text="观察这组数字：1, 3, 5, 7... 请问下一个数字是谁？",
            options="8,9,10,11",
            correct_answer="9",
            hint="看看前一个数和后一个数之间，都差了多少呀？(是+2哦)"
        )
        
        # 第2题：识别关键要素
        q2 = Question(
            topic_id=topic1.id,
            text="对于数列 2, 4, 6, 8, 10。首项(第一个数)和末项(最后一个数)分别是多少？",
            options="2和10, 2和8, 1和10, 2和12",
            correct_answer="2和10",
            hint="首项就是排第一的，末项就是排最后的，别想复杂啦。"
        )

        # 第3题：图形化思维
        q3 = Question(
            topic_id=topic1.id,
            text="如果我们要算 1+2+3+4+5+6，首尾配对的话，1和谁配对？2和谁配对？",
            options="1配6 / 2配5, 1配5 / 2配4, 1配2 / 3配4",
            correct_answer="1配6 / 2配5",
            hint="我们要凑成一样大的数，1+6=7，2+5=7... 就像搭桥一样！"
        )

        session.add(q1)
        session.add(q2)
        session.add(q3)
        
        session.commit()
        print("题目数据注入完成！")

if __name__ == "__main__":
    init_db()