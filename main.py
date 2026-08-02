import json
import os
import random  # 랜덤 출제를 위한 모듈
from datetime import datetime  # 히스토리 기록을 위한 시간 모듈

class Quiz:
    # hint 속성 추가 (기본값 설정)
    def __init__(self, question, choices, answer, hint="제공된 힌트가 없습니다."):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self):
        print(f"Q. {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint # 딕셔너리 변환 시 힌트 포함
        }

    @classmethod
    def from_dict(cls, data):
        # 기존 데이터에 hint가 없을 경우를 대비해 get() 사용
        return cls(data["question"], data["choices"], data["answer"], data.get("hint", "제공된 힌트가 없습니다."))


# -----------------------------------------------------------------
class QuizGame:

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.history = []  # 점수 기록 히스토리 리스트 추가
        self.filepath = "state.json"
        self.load_data()

    def load_data(self):
        """파일에서 데이터를 불러옵니다. 파일이 없거나 손상되었으면 기본값을 사용합니다."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)
                    # 보너스 기능: 히스토리 기록 불러오기 (기존 파일에 없으면 빈 리스트 리턴)
                    self.history = data.get("history", [])

                    # JSON 데이터를 다시 Quiz 객체로 변환하여 리스트에 추가
                    for q_data in data.get("quizzes", []):
                        # 보너스 기능: 힌트 데이터 가져오기 (기존 파일에 없으면 기본 메시지 설정)
                        hint = q_data.get("hint", "제공된 힌트가 없습니다.")
                        quiz = Quiz(q_data["question"], q_data["choices"], q_data["answer"], hint)
                        self.quizzes.append(quiz)

                print(f"📂 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
                return
            except (json.JSONDecodeError, IOError):
                print("⚠️ 데이터 파일이 손상되었습니다. 기본 퀴즈로 초기화합니다.")

        # 파일이 없거나(첫 실행) 오류가 난 경우 기본 퀴즈 로드
        self._load_default_quizzes()

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수, 플레이 히스토리를 JSON 파일에 저장합니다."""
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score,
                "history": self.history  # 보너스 기능: 히스토리 기록 저장 리스트 추가
            }
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError:
            print("⚠️ 데이터를 저장하는 중 오류가 발생했습니다.")



    def _load_default_quizzes(self):
        """기본 퀴즈 5개를 세팅합니다. (원하는 주제의 퀴즈로 수정해 보세요!)"""
        self.quizzes = [
            Quiz("Python의 창시자는?", ["Guido", "Linus", "Bjarne", "James"], 1),
            Quiz("HTML의 약자는?", ["Hyper Text", "Hyperlinks", "Home Tool", "Hyper Text Markup Language"], 4),
            Quiz("다음 중 파이썬의 기본 자료형이 아닌 것은?", ["int", "list", "array", "dict"], 3),
            Quiz("Git에서 변경사항을 임시 저장하는 공간은?",
                 ["Working Directory", "Staging Area", "Local Repository", "Remote Repository"], 2),
            Quiz("1 + 1 = ?", ["1", "2", "3", "4"], 2)
        ]
        self.save_data()  # 세팅 후 state.json 파일로 즉시 저장

    def get_int_input(self, prompt: str, min_val: int, max_val: int) -> int:
        """공통 입력 및 예외 처리 로직"""
        while True:
            try:
                user_input = input(prompt).strip()  # 앞뒤 공백 제거

                if not user_input:  # 빈 입력(Enter만 친 경우)
                    print("⚠️ 입력값이 없습니다. 다시 입력해 주세요.")
                    continue

                value = int(user_input)  # 숫자로 변환 시도

                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"⚠️ {min_val}~{max_val} 사이의 숫자를 입력해 주세요.")

            except ValueError:  # 문자를 입력한 경우
                print("⚠️ 잘못된 입력입니다. 숫자로 입력해 주세요.")
            except (KeyboardInterrupt, EOFError):  # Ctrl+C 등으로 강제 종료 시도 시
                print("\n\n프로그램을 안전하게 종료합니다. (데이터 저장 완료)")
                self.save_data()
                exit()

    def show_quiz_list(self):
        """저장된 퀴즈 목록을 보여줍니다."""
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
        else:
            for i, quiz in enumerate(self.quizzes, 1):
                print(f"[{i}] {quiz.question}")
        print("-" * 40)


    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("⚠️ 문제가 비어있습니다.")
            return

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if choice:
                    choices.append(choice)
                    break
                else:
                    print("⚠️ 선택지는 비워둘 수 없습니다.")

        answer = self.get_int_input("정답 번호 (1-4): ", 1, 4)

        # 힌트 입력 받기
        hint = input("힌트를 입력하세요 (없으면 엔터): ").strip()
        if not hint:
            hint = "제공된 힌트가 없습니다."

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        self.save_data()
        print("\n✅ 퀴즈가 성공적으로 추가되었습니다!")

    def delete_quiz(self):
        if not self.quizzes:
            print("\n⚠️ 삭제할 퀴즈가 없습니다.")
            return

        self.show_quiz_list()
        num = self.get_int_input("\n삭제할 퀴즈 번호를 입력하세요 (취소는 0): ", 0, len(self.quizzes))
        if num == 0:
            return

        deleted = self.quizzes.pop(num - 1)
        self.save_data()
        print(f"\n✅ '{deleted.question}' 퀴즈가 삭제되었습니다.")

    def show_best_score(self):
        print(f"\n🏆 역대 최고 점수: {self.best_score}점")
        print("-" * 40)
        print("📜 최근 플레이 기록")
        if not self.history:
            print("기록이 없습니다.")
        else:
            for record in self.history[-5:]:  # 최근 5개만 출력
                print(f"[{record['date']}] {record['total']}문제 중 {record['score']}점")
        print("-" * 40)


    def run(self):
        while True:
            print("\n========================================")
            print("        🎯 나만의 퀴즈 게임 🎯        ")
            print("========================================")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록")
            print("4. 퀴즈 삭제")
            print("5. 점수 확인")
            print("6. 종료")
            print("========================================")

            choice = self.get_int_input("선택: ", 1, 6)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.delete_quiz()  # 메서드 연결
            elif choice == 5:
                self.show_best_score()
            elif choice == 6:
                print("게임을 종료합니다. 수고하셨습니다!")
                break

    def play_quiz(self):
        if not self.quizzes:
            print("\n⚠️ 퀴즈가 없습니다.")
            return

        # 1. 문제 수 선택
        max_q = len(self.quizzes)
        num_q = self.get_int_input(f"\n몇 문제를 푸시겠습니까? (1~{max_q}): ", 1, max_q)

        # 2. 랜덤 출제 (선택한 개수만큼 무작위 추출)
        play_list = random.sample(self.quizzes, num_q)

        score = 0
        for i, quiz in enumerate(play_list, 1):
            print("\n" + "-" * 40)
            print(f"[문제 {i}]")
            quiz.display()

            # 3. 힌트 보기 옵션 추가
            user_answer = self.get_int_input("\n정답 입력 (0: 힌트 보기, 1-4: 정답): ", 0, 4)

            point = 1.0  # 기본 점수 1점
            if user_answer == 0:
                print(f"💡 힌트: {quiz.hint}")
                user_answer = self.get_int_input("다시 정답 입력 (1-4): ", 1, 4)
                point = 0.5  # 힌트 사용 시 0.5점 획득으로 차감

            if user_answer == quiz.answer:
                print(f"✅ 정답입니다! (+{point}점)")
                score += point
            else:
                print(f"❌ 오답입니다. (정답: {quiz.answer}번)")

        print("\n" + "=" * 40)
        print(f"🏆 최종 결과: {score}점 획득! (총 {num_q}문제)")

        if score > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = score

        # 4. 히스토리 저장
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history.append({"date": now, "total": num_q, "score": score})
        self.save_data()




if __name__ == "__main__":
    game = QuizGame()
    game.run()




