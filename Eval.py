from enum import Enum, auto


class State(Enum):
    """Énumération des états possibles du distributeur de balles surprise."""
    NO_TOKEN = auto()
    ONE_TOKEN = auto()
    SOLD = auto()
    NO_BALLS_LEFT = auto()


class GiftBall:
    """Distributeur de balles surprise - machine à états."""
    
    def __init__(self, initial_balls: int = 10):
        """
        Initialise le distributeur avec un nombre initial de balles.
        
        Args:
            initial_balls: Nombre initial de balles surprise disponibles
        """
        self.current_state = State.NO_TOKEN
        self.balls_remaining = initial_balls
    
    def insert_token(self) -> bool:
        """
        Insère un jeton dans la machine.
        
        Transition: NO_TOKEN -> ONE_TOKEN
        
        Returns:
            True si l'opération a réussi, False sinon
        """
        if self.current_state == State.NO_TOKEN:
            self.current_state = State.ONE_TOKEN
            return True
        return False
    
    def eject_token(self) -> bool:
        """
        Éjecte le jeton de la machine.
        
        Transition: ONE_TOKEN -> NO_TOKEN
        
        Returns:
            True si l'opération a réussi, False sinon
        """
        if self.current_state == State.ONE_TOKEN:
            self.current_state = State.NO_TOKEN
            return True
        return False
    
    def turn_handle(self) -> bool:
        """
        Tourne la manivelle pour distribuer une boule surprise.
        
        Transitions:
        - ONE_TOKEN -> SOLD si des balles sont disponibles
        - ONE_TOKEN -> NO_BALLS_LEFT si c'est la dernière balle
        
        Returns:
            True si l'opération a réussi, False sinon
        """
        if self.current_state == State.ONE_TOKEN:
            if self.balls_remaining > 0:
                self.current_state = State.SOLD
                return True
        return False
    
    def handle_sold_transition(self) -> bool:
        """
        Gère la transition après la vente d'une boule.
        
        Transitions:
        - SOLD -> NO_TOKEN si des balles restent (balls_remaining > 0)
        - SOLD -> NO_BALLS_LEFT si c'est la dernière balle distribuée
        
        Returns:
            True si l'opération a réussi, False sinon
        """
        if self.current_state == State.SOLD:
            self.balls_remaining -= 1
            
            if self.balls_remaining > 0:
                self.current_state = State.NO_TOKEN
            else:
                self.current_state = State.NO_BALLS_LEFT
            return True
        return False
    
    def get_state(self) -> State:
        """
        Retourne l'état actuel du distributeur.
        
        Returns:
            L'état courant du distributeur
        """
        return self.current_state
    
    def get_balls_remaining(self) -> int:
        """
        Retourne le nombre de balles restantes.
        
        Returns:
            Nombre de balles surprise disponibles
        """
        return self.balls_remaining
    
    def __str__(self) -> str:
        """Représentation textuelle de l'état du distributeur."""
        return f"GiftBall(state={self.current_state.name}, balls={self.balls_remaining})"
