from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)
CORS(app)


# ==========================================
# MYSQL CONNECTION
# ==========================================

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pallavi@2006",
        database="gapmind"
    )


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return "GapMind Backend is Running!"


# ==========================================
# TEST DATABASE
# ==========================================

@app.route("/test-db")
def test_db():

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute("SELECT DATABASE()")

        database = cursor.fetchone()[0]

        return jsonify({
            "status": "success",
            "database": database
        })

    except mysql.connector.Error as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# CREATE STUDENT
# ==========================================

@app.route("/api/students", methods=["POST"])
def create_student():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No student data received."
        }), 400


    # --------------------------------------
    # STUDENT INFORMATION
    # --------------------------------------

    name = data.get(
        "name",
        ""
    ).strip()

    email = data.get(
        "email",
        ""
    ).strip()

    college = data.get(
        "college",
        ""
    ).strip()

    degree = data.get(
        "degree",
        ""
    ).strip()

    branch = data.get(
        "branch",
        ""
    ).strip()

    graduation_year = data.get(
        "graduation_year"
    )

    cgpa = data.get(
        "cgpa"
    )

    skills = data.get(
        "skills",
        ""
    ).strip()

    target_role = data.get(
        "target_role",
        ""
    ).strip()

    preparation_level = data.get(
        "preparation_level",
        ""
    ).strip()


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if not name:

        return jsonify({
            "error": "Please enter your name."
        }), 400


    if not email:

        return jsonify({
            "error": "Please enter your email."
        }), 400


    if not college:

        return jsonify({
            "error": "Please enter your college."
        }), 400


    if not degree:

        return jsonify({
            "error": "Please select your degree."
        }), 400


    if not branch:

        return jsonify({
            "error": "Please enter your branch."
        }), 400


    if not graduation_year:

        return jsonify({
            "error": "Please enter your graduation year."
        }), 400


    if not cgpa:

        return jsonify({
            "error": "Please enter your CGPA."
        }), 400


    if not target_role:

        return jsonify({
            "error": "Please select your target role."
        }), 400


    if not preparation_level:

        return jsonify({
            "error": "Please select your preparation level."
        }), 400


    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor()


        query = """
        INSERT INTO students
        (
            name,
            email,
            college,
            degree,
            branch,
            graduation_year,
            cgpa,
            skills,
            target_role,
            preparation_level
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """


        values = (
            name,
            email,
            college,
            degree,
            branch,
            int(graduation_year),
            float(cgpa),
            skills,
            target_role,
            preparation_level
        )


        cursor.execute(
            query,
            values
        )

        connection.commit()

        student_id = cursor.lastrowid


        return jsonify({
            "success": True,
            "message": "Profile created successfully!",
            "student_id": student_id
        }), 201


    except mysql.connector.IntegrityError:

        if connection:
            connection.rollback()

        return jsonify({
            "success": False,
            "error": "An account with this email already exists."
        }), 409


    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        print(
            "MYSQL ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


    except Exception as error:

        if connection:
            connection.rollback()

        print(
            "SERVER ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# LOGIN
# ==========================================

@app.route("/api/login", methods=["POST"])
def login_student():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "error": "No login data received."
        }), 400


    email = data.get(
        "email",
        ""
    ).strip()


    if not email:

        return jsonify({
            "success": False,
            "error": "Please enter your email."
        }), 400


    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT
                student_id,
                name,
                email
            FROM students
            WHERE email = %s
            """,
            (email,)
        )


        student = cursor.fetchone()


        if not student:

            return jsonify({
                "success": False,
                "error": "No account found with this email."
            }), 404


        return jsonify({

            "success": True,

            "message":
                "Login successful!",

            "student_id":
                student["student_id"],

            "name":
                student["name"],

            "email":
                student["email"]

        }), 200


    except mysql.connector.Error as error:

        print(
            "LOGIN MYSQL ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


    except Exception as error:

        print(
            "LOGIN SERVER ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# GET STUDENT
# ==========================================

@app.route(
    "/api/students/<int:student_id>",
    methods=["GET"]
)
def get_student(student_id):

    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM students
            WHERE student_id = %s
            """,
            (student_id,)
        )


        student = cursor.fetchone()


        if not student:

            return jsonify({
                "error": "Student not found."
            }), 404


        return jsonify(student)


    except mysql.connector.Error as error:

        return jsonify({
            "error": str(error)
        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# SAVE ASSESSMENT RESULT
# ==========================================

@app.route(
    "/api/assessment-results",
    methods=["POST"]
)
def create_assessment_result():

    data = request.get_json()


    if not data:

        return jsonify({
            "success": False,
            "error": "No assessment data received."
        }), 400


    student_id = data.get(
        "student_id"
    )

    score = data.get(
        "score"
    )

    total_questions = data.get(
        "total_questions"
    )

    correct_answers = data.get(
        "correct_answers"
    )

    skills_assessed = data.get(
        "skills_assessed",
        ""
    )

    skill_performance = data.get(
        "skill_performance",
        {}
    )


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if student_id is None:

        return jsonify({
            "success": False,
            "error": "Student ID is required."
        }), 400


    if score is None:

        return jsonify({
            "success": False,
            "error": "Score is required."
        }), 400


    if total_questions is None:

        return jsonify({
            "success": False,
            "error": "Total questions is required."
        }), 400


    if correct_answers is None:

        return jsonify({
            "success": False,
            "error": "Correct answers are required."
        }), 400


    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor()


        # --------------------------------------
        # VERIFY STUDENT
        # --------------------------------------

        cursor.execute(
            """
            SELECT student_id
            FROM students
            WHERE student_id = %s
            """,
            (int(student_id),)
        )


        student = cursor.fetchone()


        if not student:

            return jsonify({
                "success": False,
                "error": "Student does not exist."
            }), 404


        # --------------------------------------
        # INSERT ASSESSMENT RESULT
        # --------------------------------------

        query = """
        INSERT INTO assessment_results
        (
            student_id,
            score,
            total_questions,
            correct_answers,
            skills_assessed
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """


        values = (
            int(student_id),
            int(score),
            int(total_questions),
            int(correct_answers),
            skills_assessed
        )


        cursor.execute(
            query,
            values
        )


        connection.commit()


        assessment_id = cursor.lastrowid


        # --------------------------------------
        # SAVE SKILL-WISE GAPS
        # --------------------------------------

        if isinstance(skill_performance, dict):

            gap_query = """
            INSERT INTO skill_gaps
            (
                student_id,
                skill_name,
                questions_attempted,
                correct_answers,
                accuracy,
                gap_level
            )
            VALUES
            (%s, %s, %s, %s, %s, %s)
            """

            gap_values = []

            for skill_name, performance in skill_performance.items():

                if not isinstance(performance, dict):
                    continue

                attempted = int(
                    performance.get(
                        "questions_attempted",
                        0
                    )
                )

                correct = int(
                    performance.get(
                        "correct_answers",
                        0
                    )
                )

                if attempted <= 0:
                    continue

                # Calculate on the server so the stored value
                # cannot depend only on the browser calculation.
                accuracy = round(
                    (correct / attempted) * 100,
                    2
                )

                if accuracy < 50:
                    gap_level = "High"
                elif accuracy < 75:
                    gap_level = "Moderate"
                else:
                    gap_level = "Low"

                gap_values.append(
                    (
                        int(student_id),
                        str(skill_name)[:100],
                        attempted,
                        correct,
                        accuracy,
                        gap_level
                    )
                )

            if gap_values:
                cursor.executemany(
                    gap_query,
                    gap_values
                )

        connection.commit()

        print(
            "ASSESSMENT SAVED:",
            assessment_id
        )


        return jsonify({

            "success": True,

            "message":
                "Assessment result saved successfully!",

            "assessment_id":
                assessment_id,

            "student_id":
                int(student_id)

        }), 201


    except mysql.connector.Error as error:

        if connection:
            connection.rollback()

        print(
            "MYSQL ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


    except Exception as error:

        if connection:
            connection.rollback()

        print(
            "SERVER ERROR:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# GET ASSESSMENT RESULTS
# ==========================================

@app.route(
    "/api/assessment-results/<int:student_id>",
    methods=["GET"]
)
def get_assessment_results(student_id):

    connection = None
    cursor = None


    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT *
            FROM assessment_results
            WHERE student_id = %s
            ORDER BY completed_at DESC
            """,
            (student_id,)
        )


        results = cursor.fetchall()


        return jsonify({

            "success": True,

            "student_id":
                student_id,

            "results":
                results

        })


    except mysql.connector.Error as error:

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# GET SKILL GAPS
# ==========================================

@app.route(
    "/api/skill-gaps/<int:student_id>",
    methods=["GET"]
)
def get_skill_gaps(student_id):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                gap_id,
                student_id,
                skill_name,
                questions_attempted,
                correct_answers,
                accuracy,
                gap_level,
                created_at
            FROM skill_gaps
            WHERE student_id = %s
            ORDER BY created_at DESC, gap_id DESC
            """,
            (student_id,)
        )

        gaps = cursor.fetchall()

        return jsonify({
            "success": True,
            "student_id": student_id,
            "gaps": gaps
        }), 200

    except mysql.connector.Error as error:

        print(
            "SKILL GAPS MYSQL ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

    except Exception as error:

        print(
            "SKILL GAPS SERVER ERROR:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )



# ============================================================
# GAPMIND - RANDOMIZED PLACEMENT ASSESSMENT QUESTION BANK
# ============================================================
# This section adds a backend-controlled assessment generator.
# Existing routes and database logic remain unchanged.

import random
from flask import jsonify, request

ASSESSMENT_QUESTION_BANK = {
    "Programming": [
        {"id":"prog_01","type":"concept","difficulty":"easy","question":"Which data structure follows LIFO order?","options":["Stack","Queue","Heap","Graph"],"answer":0},
        {"id":"prog_02","type":"code","difficulty":"easy","question":"What is printed by: int x = 5; cout << ++x;","options":["5","6","4","Compilation error"],"answer":1},
        {"id":"prog_03","type":"complexity","difficulty":"medium","question":"What is the time complexity of binary search on a sorted array?","options":["O(n)","O(log n)","O(n log n)","O(n²)"],"answer":1},
        {"id":"prog_04","type":"scenario","difficulty":"medium","question":"A program repeatedly needs the smallest item from a changing set. Which structure is the best fit?","options":["Priority queue","Stack","Plain array only","String"],"answer":0},
        {"id":"prog_05","type":"algorithm","difficulty":"medium","question":"Which algorithm finds the maximum contiguous subarray sum in linear time?","options":["Kadane's algorithm","Dijkstra","Kruskal","Floyd-Warshall"],"answer":0},
        {"id":"prog_06","type":"concept","difficulty":"medium","question":"Which OOP feature allows the same interface to have different implementations?","options":["Polymorphism","Compilation","Indexing","Iteration"],"answer":0},
        {"id":"prog_07","type":"code","difficulty":"easy","question":"What is the value of sum after: int sum=0; for(int i=1;i<=3;i++) sum+=i;","options":["3","5","6","9"],"answer":2},
        {"id":"prog_08","type":"scenario","difficulty":"medium","question":"Which principle protects an object's internal state by controlling access to its data?","options":["Encapsulation","Recursion","Hashing","Traversal"],"answer":0},
    ],
    "DBMS": [
        {"id":"db_01","type":"concept","difficulty":"medium","question":"Which normal form removes partial dependency on a composite key?","options":["1NF","2NF","3NF","BCNF"],"answer":1},
        {"id":"db_02","type":"concept","difficulty":"easy","question":"Which SQL clause filters rows before grouping?","options":["WHERE","HAVING","ORDER BY","GROUP BY"],"answer":0},
        {"id":"db_03","type":"code","difficulty":"easy","question":"SELECT COUNT(*) FROM Student WHERE marks >= 90; What does it return?","options":["Sum of marks","Number of matching rows","Highest mark","All student rows"],"answer":1},
        {"id":"db_04","type":"scenario","difficulty":"medium","question":"Two transactions must safely update the same data without interfering. Which area handles this?","options":["Concurrency control","Normalization","DDL","Views"],"answer":0},
        {"id":"db_05","type":"concept","difficulty":"easy","question":"Which ACID property means a transaction happens completely or not at all?","options":["Atomicity","Consistency","Isolation","Durability"],"answer":0},
        {"id":"db_06","type":"algorithm","difficulty":"medium","question":"Which index structure is especially useful for ordered indexes and range queries?","options":["B+ tree","Stack","Queue","Linked list"],"answer":0},
        {"id":"db_07","type":"concept","difficulty":"easy","question":"Which SQL command removes a table definition?","options":["DELETE","DROP","UPDATE","SELECT"],"answer":1},
        {"id":"db_08","type":"scenario","difficulty":"medium","question":"What provides a reusable virtual table based on a query without storing a separate copy of its rows?","options":["View","Trigger","Index","Bucket"],"answer":0},
    ],
    "Operating Systems": [
        {"id":"os_01","type":"concept","difficulty":"medium","question":"Which scheduling algorithm can cause starvation if priorities are never adjusted?","options":["Priority scheduling","Round Robin","FCFS only","FIFO page replacement"],"answer":0},
        {"id":"os_02","type":"scenario","difficulty":"medium","question":"A process waits indefinitely because other processes keep receiving CPU time. What is this called?","options":["Starvation","Thrashing","Deadlock","Paging"],"answer":0},
        {"id":"os_03","type":"concept","difficulty":"medium","question":"Which page replacement algorithm removes the page that has not been used for the longest time?","options":["LRU","FIFO","FCFS","SJF"],"answer":0},
        {"id":"os_04","type":"concept","difficulty":"easy","question":"A process has arrived and is waiting for CPU allocation. Which state is it in?","options":["Ready","Running","Terminated","New"],"answer":0},
        {"id":"os_05","type":"concept","difficulty":"medium","question":"Which is one of the necessary conditions for deadlock?","options":["Circular wait","Compilation","Indexing","Sorting"],"answer":0},
        {"id":"os_06","type":"scenario","difficulty":"medium","question":"A system spends most of its time swapping pages instead of doing useful work. This is:","options":["Thrashing","Spooling","Starvation","Fragmentation"],"answer":0},
        {"id":"os_07","type":"concept","difficulty":"easy","question":"Round Robin scheduling is primarily designed for:","options":["Time-sharing systems","Database indexing","File compression","Deadlock prevention only"],"answer":0},
        {"id":"os_08","type":"concept","difficulty":"medium","question":"What does a context switch primarily do?","options":["Switches CPU execution from one process/thread to another","Deletes a process","Formats memory","Sorts the ready queue"],"answer":0},
    ],
    "OOP": [
        {"id":"oop_01","type":"concept","difficulty":"easy","question":"Which concept hides implementation details and exposes a necessary interface?","options":["Abstraction","Inheritance","Overloading","Iteration"],"answer":0},
        {"id":"oop_02","type":"concept","difficulty":"easy","question":"Same method name with different parameter lists is called:","options":["Method overloading","Method overriding","Encapsulation","Aggregation"],"answer":0},
        {"id":"oop_03","type":"code","difficulty":"easy","question":"If class B extends class A, B is the:","options":["Base class","Derived class","Compiler","Interface only"],"answer":1},
        {"id":"oop_04","type":"scenario","difficulty":"medium","question":"A subclass provides its own implementation of a parent method with the same signature. This is:","options":["Overriding","Overloading","Constructor chaining","Indexing"],"answer":0},
        {"id":"oop_05","type":"concept","difficulty":"easy","question":"Which OOP principle bundles data and methods together?","options":["Encapsulation","Recursion","Searching","Normalization"],"answer":0},
        {"id":"oop_06","type":"concept","difficulty":"easy","question":"Which relationship represents an 'is-a' relationship?","options":["Inheritance","Composition only","Indexing","Aggregation only"],"answer":0},
        {"id":"oop_07","type":"code","difficulty":"easy","question":"A constructor is mainly called when:","options":["An object is created","A loop ends","A source file is deleted","A method is overridden"],"answer":0},
        {"id":"oop_08","type":"scenario","difficulty":"medium","question":"Multiple subclasses respond differently to the same method call. Which feature enables this?","options":["Polymorphism","Primary key","Paging","Hashing"],"answer":0},
    ],
    "DSA": [
        {"id":"dsa_01","type":"concept","difficulty":"easy","question":"Which data structure follows FIFO order?","options":["Queue","Stack","Tree","Hash map"],"answer":0},
        {"id":"dsa_02","type":"complexity","difficulty":"medium","question":"What is average hash-table lookup time?","options":["O(1)","O(log n)","O(n log n)","O(n²)"],"answer":0},
        {"id":"dsa_03","type":"algorithm","difficulty":"medium","question":"Which traversal is commonly used for shortest paths in an unweighted graph?","options":["BFS","DFS","Inorder","Postorder"],"answer":0},
        {"id":"dsa_04","type":"concept","difficulty":"medium","question":"Which traversal of a standard BST gives values in sorted order?","options":["Inorder","Preorder","Postorder","Level order"],"answer":0},
        {"id":"dsa_05","type":"scenario","difficulty":"medium","question":"You repeatedly need the highest-priority item from a dynamic set. Which structure fits best?","options":["Heap/Priority Queue","Stack only","Array index only","String"],"answer":0},
        {"id":"dsa_06","type":"algorithm","difficulty":"medium","question":"Which technique solves many maximum-subarray problems in linear time?","options":["Kadane's algorithm","Tree rotation","Dijkstra","BFS"],"answer":0},
        {"id":"dsa_07","type":"concept","difficulty":"medium","question":"Which technique uses a left and right boundary to process a contiguous range efficiently?","options":["Sliding window","Deadlock","Normalization","Inheritance"],"answer":0},
        {"id":"dsa_08","type":"concept","difficulty":"medium","question":"What is the purpose of a visited array in graph traversal?","options":["Avoid repeated processing","Sort vertices","Remove edges","Reduce graph size"],"answer":0},
    ],
    "Cloud": [
        {"id":"cloud_01","type":"concept","difficulty":"easy","question":"Which cloud service model provides virtual machines, storage and networking?","options":["IaaS","PaaS","SaaS","DBMS"],"answer":0},
        {"id":"cloud_02","type":"concept","difficulty":"medium","question":"Which cloud property automatically adds or removes resources based on demand?","options":["Elasticity","Normalization","Inheritance","Compilation"],"answer":0},
        {"id":"cloud_03","type":"scenario","difficulty":"medium","question":"A developer deploys an application without managing the underlying OS. Which model fits best?","options":["PaaS","IaaS","Bare metal only","Assembly"],"answer":0},
        {"id":"cloud_04","type":"concept","difficulty":"easy","question":"Which technology packages an application and dependencies into an isolated unit?","options":["Containerization","Indexing","Deadlock","Normalization"],"answer":0},
        {"id":"cloud_05","type":"concept","difficulty":"easy","question":"Which tool is commonly used for container orchestration?","options":["Kubernetes","MySQL","JDBC","Git"],"answer":0},
        {"id":"cloud_06","type":"scenario","difficulty":"medium","question":"Choosing a smaller cloud instance that still meets workload needs is called:","options":["Rightsizing","Overprovisioning","Replication","Compilation"],"answer":0},
        {"id":"cloud_07","type":"concept","difficulty":"easy","question":"TCO stands for:","options":["Total Cost of Ownership","Technical Cloud Operation","Transfer Cost Output","Total Compute Object"],"answer":0},
        {"id":"cloud_08","type":"concept","difficulty":"medium","question":"Which deployment model is dedicated to a single organization?","options":["Private cloud","Public cloud","Community internet","Hybrid only"],"answer":0},
    ],
}


def _assessment_history_key(student_id):
    return f"gapmind_assessment_history_{student_id}"


def _get_recent_question_ids(student_id):
    """Read recent IDs from the Flask session without affecting DB tables."""
    try:
        from flask import session
        history = session.get(_assessment_history_key(student_id), [])
        return set(history[-10:])
    except Exception:
        return set()


def _save_recent_question_ids(student_id, question_ids):
    try:
        from flask import session
        key = _assessment_history_key(student_id)
        history = session.get(key, [])
        history.extend(question_ids)
        session[key] = history[-50:]
        session.modified = True
    except Exception:
        pass


def generate_random_assessment(student_id=None, questions_per_assessment=10):
    """
    Generate a balanced assessment:
      - different questions on successive attempts where possible
      - multiple topics
      - mix of concept/code/algorithm/complexity/scenario
      - difficulty mix
    Correct answers are intentionally NOT sent to the frontend.
    """
    recent = _get_recent_question_ids(student_id) if student_id is not None else set()

    fresh_by_topic = {}
    for topic, questions in ASSESSMENT_QUESTION_BANK.items():
        fresh = [q for q in questions if q["id"] not in recent]
        # If a topic has been exhausted, allow rotation back through its bank.
        fresh_by_topic[topic] = fresh or list(questions)

    topics = list(ASSESSMENT_QUESTION_BANK.keys())
    random.shuffle(topics)

    selected = []

    # First pass: one question from each topic.
    for topic in topics:
        pool = fresh_by_topic[topic][:]
        random.shuffle(pool)
        if pool:
            selected.append(pool.pop())

    # Fill remaining slots from the global fresh pool.
    remaining = []
    for topic in topics:
        remaining.extend(fresh_by_topic[topic])
    random.shuffle(remaining)

    used = {q["id"] for q in selected}
    for q in remaining:
        if len(selected) >= questions_per_assessment:
            break
        if q["id"] not in used:
            selected.append(q)
            used.add(q["id"])

    random.shuffle(selected)
    selected = selected[:questions_per_assessment]

    if student_id is not None:
        _save_recent_question_ids(student_id, [q["id"] for q in selected])

    # Never expose the correct answer.
    public_questions = []
    for number, q in enumerate(selected, start=1):
        public_questions.append({
            "number": number,
            "id": q["id"],
            "topic": q["topic"] if "topic" in q else next(
                topic for topic, qs in ASSESSMENT_QUESTION_BANK.items() if any(x["id"] == q["id"] for x in qs)
            ),
            "type": q["type"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "options": q["options"],
        })

    return public_questions


# New endpoint. It is safe to call from your assessment page.
@app.route("/api/assessment/questions", methods=["GET"])
def assessment_questions():
    try:
        student_id = request.args.get("student_id", type=int)
        count = request.args.get("count", default=10, type=int)
        count = max(5, min(count, 15))

        questions = generate_random_assessment(
            student_id=student_id,
            questions_per_assessment=count
        )

        return jsonify({
            "success": True,
            "count": len(questions),
            "questions": questions
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

