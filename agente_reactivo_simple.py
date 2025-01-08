import gymnasium as gym
import numpy as np
import pygame
import time

# Crear el entorno del horno
class FurnaceEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.observation_space = gym.spaces.Box(low=0, high=300, shape=(1,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(2)

        self.temperature = 150.0
        self.heat_rate = 5.0
        self.cool_rate = 3.0

        self.target_range = (180, 220)
        self.max_steps = 200
        self.current_step = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.temperature = 150.0
        self.current_step = 0
        return np.array([self.temperature], dtype=np.float32), {}

    def step(self, action):
        if action == 0:
            self.temperature += self.heat_rate
        elif action == 1:
            self.temperature -= self.cool_rate

        self.current_step += 1

        reward = 1.0 if self.target_range[0] <= self.temperature <= self.target_range[1] else -1.0
        done = self.current_step >= self.max_steps
        return np.array([self.temperature], dtype=np.float32), reward, done, False, {}

    def render(self):
        pass


# Clase para visualizar con pygame
class FurnaceVisualizer:
    def __init__(self, env):
        pygame.init()
        self.env = env
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Simulación de Horno con Agente Inteligente")
        self.clock = pygame.time.Clock()

    def get_temperature_color(self, temperature):
        if temperature < 150:
            return (255, 255, 255)  # Blanco: apagado
        elif temperature < 180:
            return (255, 0, 0)  # Rojo: baja temperatura
        elif temperature <= 220:
            return (255, 255, 0)  # Amarillo: temperatura media
        else:
            return (0, 0, 255)  # Azul: alta temperatura

    def draw(self, temperature, action):
        self.screen.fill((30, 30, 30))  # Fondo negro

        # Dibujar el horno
        pygame.draw.rect(self.screen, (200, 200, 200), (550, 200, 150, 150))  # Contorno del horno
        caldera_color = self.get_temperature_color(temperature)
        pygame.draw.rect(self.screen, caldera_color, (560, 210, 130, 130))  # Interior del horno
        font = pygame.font.Font(None, 24)
        horno_text = font.render("Horno", True, (255, 255, 255))
        self.screen.blit(horno_text, (580, 180))

        # Dibujar el agente (robot)
        pygame.draw.rect(self.screen, (100, 150, 255), (100, 250, 80, 100))  # Cuerpo del robot
        pygame.draw.circle(self.screen, (255, 255, 255), (140, 240), 20)  # Cabeza del robot
        pygame.draw.line(self.screen, (100, 150, 255), (110, 350), (100, 380), 5)  # Pierna izquierda
        pygame.draw.line(self.screen, (100, 150, 255), (170, 350), (180, 380), 5)  # Pierna derecha
        pygame.draw.line(self.screen, (100, 150, 255), (90, 280), (70, 310), 5)  # Brazo izquierdo
        pygame.draw.line(self.screen, (100, 150, 255), (190, 280), (210, 310), 5)  # Brazo derecho

        agent_text = font.render("Agente", True, (255, 255, 255))
        self.screen.blit(agent_text, (120, 200))  # Texto encima del agente

        # Dibujar el sensor conectado al agente
        pygame.draw.rect(self.screen, (180, 180, 180), (220, 260, 50, 30))  # Sensor
        sensor_text = font.render("Sensor", True, (255, 255, 255))
        self.screen.blit(sensor_text, (220, 240))
        pygame.draw.line(self.screen, (255, 255, 255), (180, 280), (220, 275), 3)  # Conexión al agente

        # Dibujar el actuador conectado al agente y al horno
        pygame.draw.rect(self.screen, (0, 255, 0) if action == 1 else (255, 0, 0), (300, 300, 50, 30))  # Actuador
        actuator_text = font.render("Actuador", True, (255, 255, 255))
        self.screen.blit(actuator_text, (300, 270))
        pygame.draw.line(self.screen, (255, 255, 255), (180, 300), (300, 315), 3)  # Conexión al agente
        pygame.draw.line(self.screen, (255, 255, 255), (350, 315), (550, 275), 3)  # Conexión al horno

        # Mostrar estado del actuador
        action_text = font.render("Estado: " + ("Cerrando válvula" if action == 1 else "Abriendo válvula"), True, (255, 255, 255))
        self.screen.blit(action_text, (300, 340))

        # Mostrar temperatura actual
        temp_text = font.render(f"Temperatura: {temperature:.1f}°C", True, (255, 255, 255))
        self.screen.blit(temp_text, (10, 10))

        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        pygame.quit()


# Agente basado en reglas
class RuleBasedAgent:
    def __init__(self, target_range):
        self.target_range = target_range

    def act(self, observation):
        temperature = observation[0]
        if temperature < self.target_range[0]:
            return 0  # Abrir válvula para calentar
        elif temperature > self.target_range[1]:
            return 1  # Cerrar válvula para enfriar
        else:
            return 0  # Mantener abierta


# Bucle principal de la simulación
env = FurnaceEnv()
visualizer = FurnaceVisualizer(env)
agent = RuleBasedAgent(target_range=(180, 220))

try:
    obs, _ = env.reset()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        action = agent.act(obs)
        obs, reward, done, truncated, info = env.step(action)

        visualizer.draw(obs[0], action)

        time.sleep(0.1)  # Controlar la velocidad del simulador

finally:
    visualizer.close()
    env.close()
