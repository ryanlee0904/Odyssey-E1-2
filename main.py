import json
import os


class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int):
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    def display(self):
        print(f"\n{self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")


# -----------------------------------------------------------------

class QuizGame:
    def __init__(self):
        self.filepath = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_data()  # 프로그램 시작 시 자동으로 데이터 불러오기

    def load_data(self):
        """파일에서 데이터를 불러옵니다. 파일이 없거나 손상되었으면 기본값을 사용합니다."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)

                    # JSON 데이터를 다시 Quiz 객체로 변환하여 리스트에 추가
                    for q_data in data.get("quizzes", []):
                        quiz = Quiz(q_data["question"], q_data["choices"], q_data["answer"])
                        self.quizzes.append(quiz)
                print(f"📂 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
                return
            except (json.JSONDecodeError, IOError):
                print("⚠️ 데이터 파일이 손상되었습니다. 기본 퀴즈로 초기화합니다.")

        # 파일이 없거나(첫 실행) 오류가 난 경우 기본 퀴즈 로드
        self._load_default_quizzes()

    def save_data(self):
        """현재 퀴즈 목록과 최고 점수를 JSON 파일에 저장합니다."""
        try:
            data = {
                "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score
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

    def display_menu(self):
        print("\n========================================")
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("========================================")

    def run(self):
        """메인 게임 루프"""
        while True:
            self.display_menu()
            choice = self.get_int_input("선택: ", 1, 5)

            if choice == 1:
                print("\n🚧 퀴즈 풀기 기능은 개발 중입니다!")
            elif choice == 2:
                print("\n🚧 퀴즈 추가 기능은 개발 중입니다!")
            elif choice == 3:
                print("\n🚧 퀴즈 목록 기능은 개발 중입니다!")
            elif choice == 4:
                print("\n🚧 점수 확인 기능은 개발 중입니다!")
            elif choice == 5:
                print("\n게임을 종료합니다. 안녕히 가세요!")
                self.save_data()
                break

if __name__ == "__main__":
    game = QuizGame()
    game.run()




