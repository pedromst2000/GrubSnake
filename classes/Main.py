from classes.Snake.Snake import Snake

class Main:
    def __init__(self):
        """
        Initialize the main game class.
        """
        self.snake = Snake()   


    def update_snake(self):
        """
        Update the snake's position and state.
        """
        self.snake.move()
    
    def draw_snake(self, screen):
        """
        Draw the snake on the given screen.
        """
        self.snake.draw(screen)
