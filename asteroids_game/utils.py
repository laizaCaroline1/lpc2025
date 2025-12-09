import math

class Vec:
    """Uma classe simples para representar vetores 2D (posição e velocidade)."""
    
    def __init__(self, x, y=None):
        if isinstance(x, Vec):
            # Construtor de cópia: Vec(outro_vec)
            self.x = x.x
            self.y = x.y
        elif y is not None:
            # Construtor normal: Vec(10, 20)
            self.x = float(x)
            self.y = float(y)
        else:
            # Construtor com valor único: Vec(10) -> Vec(10, 10)
            self.x = float(x)
            self.y = float(x)
            
    #Operadores Aritméticos

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        # Multiplicação por escalar
        return Vec(self.x * scalar, self.y * scalar)

    __rmul__ = __mul__ 

    def __truediv__(self, scalar):
        # Divisão por escalar
        return Vec(self.x / scalar, self.y / scalar)
    
    #Métodos de Medição e Direção
    
    def length(self):
        """Calcula a magnitude (comprimento) do vetor."""
        return math.sqrt(self.x**2 + self.y**2)

    def magnitude_sqrd(self):
        """Calcula a magnitude ao quadrado (mais rápido, evita raiz quadrada)."""
        return self.x**2 + self.y**2
    
    def normalize(self):
        """Retorna um vetor com a mesma direção, mas magnitude 1."""
        l = self.length()
        if l == 0:
            return Vec(0, 0)
        return self / l
    
    def angle(self):
        """
        Retorna o ângulo do vetor em graus. 
        (0 graus aponta para a direita, aumenta no sentido anti-horário)
        """
        # math.atan2(y, x) retorna o ângulo em radianos.
        return math.degrees(math.atan2(self.y, self.x)) % 360
        
    def scale_to_length(self, length):
        """
        Altera o vetor para ter a magnitude especificada, mantendo a direção.
        (Altera o vetor IN-PLACE, como o Pygame Vec2)
        """
        # Necessário para limitar a velocidade no player.py
        self = self.normalize() * length
        self.x = self.x
        self.y = self.y
    
    #Métodos de Utilidade 
    
    def copy(self):
        """Retorna uma nova instância de Vec com os mesmos valores."""
        return Vec(self)

    def __repr__(self):
        return f"Vec({self.x:.2f}, {self.y:.2f})"
        
    def __eq__(self, other):
        """Verifica se dois vetores são iguais."""
        if not isinstance(other, Vec):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        """Verifica se dois vetores são diferentes."""
        return not self.__eq__(other)