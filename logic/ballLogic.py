def update_ball(ball, launched, screen):
    if launched:
        ball.accelerate()
        ball.move()
    ball.draw(screen)
