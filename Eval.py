from abc import ABC, abstractmethod


# ============================================================================
# QUESTION VERSION 2: Quel problème constatez-vous ?
# ============================================================================
# RÉPONSE:
# Le problème principal est le MANQUE DE FLEXIBILITÉ et la VIOLATION du
# principe Ouvert/Fermé. Avec l'approche monolithique initiale:
# - Chaque nouvel état nécessite de modifier la classe GiftBall directement
# - Les conditions if/else deviennent de plus en plus complexes
# - L'ajout du nouvel état (2 balles) impacte tous les autres états
# - C'est difficile à tester et à maintenir
# 
# SOLUTION: Utiliser le Pattern d'État (State Pattern) pour déléguer
# le comportement à des classes concrètes, permettant l'extension sans
# modification des code existant.
# ============================================================================


class StateInterface(ABC):
    """Interface définissant les actions possibles pour chaque état."""
    
    @abstractmethod
    def insert_token(self, machine: 'GiftBall') -> bool:
        """Insère un jeton dans la machine."""
        pass
    
    @abstractmethod
    def eject_token(self, machine: 'GiftBall') -> bool:
        """Éjecte le jeton de la machine."""
        pass
    
    @abstractmethod
    def turn_handle(self, machine: 'GiftBall') -> bool:
        """Tourne la manivelle pour distribuer une boule surprise."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retourne le nom de l'état."""
        pass


class NoTokenState(StateInterface):
    """État: Machine sans jeton."""
    
    def insert_token(self, machine: 'GiftBall') -> bool:
        """Transition: NO_TOKEN -> ONE_TOKEN"""
        machine.set_state(OneTokenState())
        return True
    
    def eject_token(self, machine: 'GiftBall') -> bool:
        """Impossible d'éjecter sans jeton."""
        return False
    
    def turn_handle(self, machine: 'GiftBall') -> bool:
        """Impossible de tourner la manivelle sans jeton."""
        return False
    
    def get_name(self) -> str:
        return "NO_TOKEN"


class OneTokenState(StateInterface):
    """État: Machine avec un jeton."""
    
    def insert_token(self, machine: 'GiftBall') -> bool:
        """Impossible d'insérer un jeton si on en a déjà un."""
        return False
    
    def eject_token(self, machine: 'GiftBall') -> bool:
        """Transition: ONE_TOKEN -> NO_TOKEN"""
        machine.set_state(NoTokenState())
        return True
    
    def turn_handle(self, machine: 'GiftBall') -> bool:
        """Transition: ONE_TOKEN -> SOLD si des balles existent."""
        if machine.get_balls_remaining() > 0:
            machine.set_state(SoldState())
            return True
        return False
    
    def get_name(self) -> str:
        return "ONE_TOKEN"


class SoldState(StateInterface):
    """État: Boule surprise vendue (transition)."""
    
    def insert_token(self, machine: 'GiftBall') -> bool:
        """Impossible d'insérer un jeton lors d'une vente."""
        return False
    
    def eject_token(self, machine: 'GiftBall') -> bool:
        """Impossible d'éjecter un jeton lors d'une vente."""
        return False
    
    def turn_handle(self, machine: 'GiftBall') -> bool:
        """Impossible de tourner la manivelle lors d'une vente."""
        return False
    
    def finalize_sale(self, machine: 'GiftBall') -> None:
        """Finalise la vente et passe à l'état suivant."""
        machine.balls_remaining -= 1
        
        if machine.get_balls_remaining() > 0:
            machine.set_state(NoTokenState())
        else:
            machine.set_state(NoBallsLeftState())
    
    def get_name(self) -> str:
        return "SOLD"


class NoBallsLeftState(StateInterface):
    """État: Plus de balles surprise disponibles."""
    
    def insert_token(self, machine: 'GiftBall') -> bool:
        """Impossible d'insérer un jeton, machine vide."""
        return False
    
    def eject_token(self, machine: 'GiftBall') -> bool:
        """Impossible d'éjecter un jeton, machine vide."""
        return False
    
    def turn_handle(self, machine: 'GiftBall') -> bool:
        """Impossible de tourner la manivelle, machine vide."""
        return False
    
    def get_name(self) -> str:
        return "NO_BALLS_LEFT"


class GiftBall:
    """Distributeur de balles surprise - machine à états avec Pattern State."""
    
    def __init__(self, initial_balls: int = 10):
        """
        Initialise le distributeur avec un nombre initial de balles.
        
        Args:
            initial_balls: Nombre initial de balles surprise disponibles
        """
        self.current_state: StateInterface = NoTokenState()
        self.balls_remaining = initial_balls
    
    def set_state(self, state: StateInterface) -> None:
        """
        Change l'état interne du distributeur.
        
        Args:
            state: Nouvel état du distributeur
        """
        self.current_state = state
    
    def insert_token(self) -> bool:
        """Délègue l'action à l'état courant."""
        return self.current_state.insert_token(self)
    
    def eject_token(self) -> bool:
        """Délègue l'action à l'état courant."""
        return self.current_state.eject_token(self)
    
    def turn_handle(self) -> bool:
        """Délègue l'action à l'état courant."""
        return self.current_state.turn_handle(self)
    
    def finalize_sale(self) -> None:
        """Finalise une vente si on est en état SOLD."""
        if isinstance(self.current_state, SoldState):
            self.current_state.finalize_sale(self)
    
    def get_state(self) -> StateInterface:
        """Retourne l'état actuel du distributeur."""
        return self.current_state
    
    def get_balls_remaining(self) -> int:
        """Retourne le nombre de balles restantes."""
        return self.balls_remaining
    
    def __str__(self) -> str:
        """Représentation textuelle de l'état du distributeur."""
        return f"GiftBall(state={self.current_state.get_name()}, balls={self.balls_remaining})"
