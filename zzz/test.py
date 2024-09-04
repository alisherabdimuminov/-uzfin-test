import random
import requests


def templ(file: str, correct: str = "*", spec: int = 1):
    with open(f"{file}.txt", "r") as file:
        text = file.read().strip().split("\n\n")
    i = 1
    for question in text:
        cor = "a"
        question = question.split("\n")
        a = question.pop(-4).strip()
        b = question.pop(-3).strip()
        c = question.pop(-2).strip()
        d = question.pop(-1).strip()
        content = "\n".join(question).strip()
        answers = [a, b, c, d]
        answers = random.sample(answers, 4)
        answers = random.sample(answers, 4)
        answers = random.sample(answers, 4)
        answers = random.sample(answers, 4)
        a = answers[0]
        b = answers[1]
        c = answers[2]
        d = answers[3]

        if a[0] == correct:
            cor = "a"
        elif b[0] == correct:
            cor = "b"
        elif c[0] == correct:
            cor = "c"
        else:
            cor = "d"
    
        a = a.replace(correct, "", 1).strip()
        b = b.replace(correct, "", 1).strip()
        c = c.replace(correct, "", 1).strip()
        d = d.replace(correct, "", 1).strip()

        print(i, ".", content)
        print("a)", a)
        print("b)", b)
        print("c)", c)
        print("d)", d)
        i += 1

        data = {
            "spec": spec,
            "content": content,
            "answer_a": a,
            "answer_b": b,
            "answer_c": c,
            "answer_d": d,
            "correct": cor
        }
        url = "https://test.uzfi.uz/create/question/"
        res = requests.post(url=url, data=data)
        print(res.text)
        print()


templ("pis_uzb", "*", 17)

def cu(url: str = "https://test.uzfi.uz/create/user/"):
    with open("users.txt", "r") as f:
        users = f.read()
    users = users.split("\n")
    d = ""
    for user in users:
        data = {}
        user = user.strip().split(" ")
        if len(user) == 3 and user[2] == "*":
            data = {
                "first_name": user[0].strip(),
                "last_name": user[1].strip(),
                "state": "received",
            }
        else:
            data = {
                "first_name": user[0].strip(),
                "last_name": user[1].strip(),
                "state": "optional"
            }
        res = requests.post(url=url, data=data)
        print(res.text)

# cu()

# import requests

# data = {
#     "first_name": "Lukoluka",
#     "last_name": "Kua",
#     "state": "recieved",
# }

# url = "https://test.uzfi.uz/create/user/"
# res = requests.post(url=url, data=data)
# print(res.text)