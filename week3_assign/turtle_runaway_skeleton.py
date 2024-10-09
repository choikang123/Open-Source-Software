import tkinter as tk
import turtle
import random
import time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius ** 2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

        self.start_time = None  # 게임 시작 시간
        self.elapsed_time = 0  # 경과 시간 저장
        self.is_running = False  # 게임 상태 확인

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx ** 2 + dy ** 2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # 게임 시작 시간 기록
        self.start_time = time.time()
        self.is_running = True  # 게임 시작 상태 업데이트

        # AI 타이머 시작
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        if not self.is_running:  # 게임이 종료된 경우 함수 종료
            return

        if self.is_catched():  # 잡혔는지 확인
            self.drawer.clear()
            self.drawer.write("Game Over!", font=("Arial", 24, "bold"))
            self.is_running = False  # 게임 종료 상태 업데이트
            return  # 더 이상 진행하지 않음

        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # 경과 시간 업데이트
        self.elapsed_time = int(time.time() - self.start_time)

        is_catched = self.is_catched()
        self.drawer.clear()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Is catched? {is_catched}', font=("Arial", 16, "normal"))

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # 타이머를 표시할 거북이 생성
    timer_display = turtle.RawTurtle(screen)
    timer_display.hideturtle()
    timer_display.penup()
    timer_display.setpos(200, 300)  # 타이머 표시 위치 조정

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner, chaser)

    # 타이머 표시 메소드를 RunawayGame 클래스에 추가
    def update_timer_display():
        if game.is_running:  # 게임이 진행 중일 때만 업데이트
            timer_display.clear()  # 이전 타이머 내용 삭제
            timer_display.write(f'Time: {game.elapsed_time}s', font=("Arial", 16, "normal"))  # 타이머 업데이트
            screen.ontimer(update_timer_display, 1000)  # 1초마다 타이머 업데이트

    game.start()
    update_timer_display()  # 타이머 표시 시작
    screen.mainloop()

# //점수 초기화: max_score를 100으로 설정하여 게임 시작 시 100점으로 초기화.
# 점수 차감 로직: step 메소드에서 경과 시간이 10초를 초과할 경우 10초마다 점수를 10점 차감.
# 게임 종료 시 점수 계산: 10초 안에 게임이 끝나면 100점으로 설정하고, 10초 초과 시에는 경과 시간에 따라 점수를 차감.