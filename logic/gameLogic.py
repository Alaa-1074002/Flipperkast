def update_game_state(ball, constants, sounds, plunger, font, ball_launched, ball_lost, score, screen):
    if ball_launched and ball.y - ball.r > constants.gameH:
        ball_lost = True
        ball_launched = False
        sounds["destroyed"].play()

    if ball_lost:
        ball.x = plunger.x + plunger.w // 2
        ball.y = plunger.y - 10
        ball.spd = [0, 0]
        ball_lost = False
        sounds["spawn"].play()

    if not ball_launched:
        msg = font.render("Press SPACE to launch!", True, (255, 255, 0))
        screen.blit(msg, (constants.gameW // 2 - 150, 40))

    return ball_launched, ball_lost, score
