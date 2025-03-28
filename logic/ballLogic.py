def update_ball(ball, launched):
    if launched:
        ball.accelerate()
        ball.move()
    ball.draw()