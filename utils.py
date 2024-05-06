import random
import pandas as pd

class AntColony:
    def __init__(self, num_ants, num_nodes, distances, pheromone_evaporation_rate=0.5, alpha=1, beta=2):
        """
        Inicializa a colônia de formigas com os parâmetros especificados.

        :param num_ants: Número de formigas na colônia
        :param num_nodes: Número de nós na rede
        :param distances: Matriz de distâncias entre os nós
        :param pheromone_evaporation_rate: Taxa de evaporação de feromônios
        :param alpha: Exponente da função de influência da feromônio
        :param beta: Exponente da função de influência da distância
        """
        self.num_ants = num_ants
        self.num_nodes = num_nodes
        self.distances = distances
        self.pheromone_evaporation_rate = pheromone_evaporation_rate
        self.alpha = alpha
        self.beta = beta
        
        # Inicializa a matriz de feromônios
        self.pheromones = [[1 / (num_nodes * num_nodes)] * num_nodes for _ in range(num_nodes)]
        
        # Inicializa o melhor caminho encontrado e seu comprimento
        self.best_path = []
        self.best_path_length = float('inf')


    def calculate_probability(self, current_node, next_node):
        # Calcula a probabilidade de uma formiga ir para o próximo nó
        pheromone = self.pheromones[current_node][next_node]
        distance = self.distances[current_node][next_node]
        probability = pow(pheromone, self.alpha) * pow(1 / distance, self.beta)
        return probability
    
    def calculate_path_length(self, path):
        # Calcula o comprimento de um caminho
        length = 0
        for i in range(len(path) - 1):
            length += self.distances[path[i]][path[i + 1]]
        return length

    def select_next_node(self, path):
        # Seleciona o próximo nó para uma formiga dado o caminho atual
        current_node = path[-1]
        remaining_nodes = [node for node in range(self.num_nodes) if node not in path]
        probabilities = [self.calculate_probability(current_node, node) for node in remaining_nodes]
        total_probability = sum(probabilities)
        probabilities = [prob / total_probability for prob in probabilities]
        next_node = random.choices(remaining_nodes, weights=probabilities)[0]
        return next_node

    def generate_path(self):
        # Gera um caminho para uma formiga
        path = [random.randint(0, self.num_nodes - 1)]
        while len(path) < self.num_nodes:
            next_node = self.select_next_node(path)
            path.append(next_node)
        path.append(path[0])
        return path

    def generate_paths(self):
        # Gera os caminhos para cada formiga
        paths = []
        for _ in range(self.num_ants):
            path = self.generate_path()
            path_length = self.calculate_path_length(path)
            paths.append((path, path_length))
        return paths


    def update_pheromones(self, paths):
        # Atualiza os feromônios com base nos caminhos percorridos pelas formigas
        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                self.pheromones[i][j] *= (1 - self.pheromone_evaporation_rate)
        for path, path_length in paths:
            for i in range(self.num_nodes - 1):
                current_node = path[i]
                next_node = path[i + 1]
                self.pheromones[current_node][next_node] += 1 / path_length



    def run(self, num_iterations):
        # Executa o algoritmo por um número especificado de iterações
        dict_paths = {}
        for i in range(num_iterations):
            # Gera os caminhos para cada formiga
            paths = self.generate_paths()
            dict_paths[f'iter_{i}'] = [len_path for _, len_path in paths]
            # Atualiza os feromônios com base nos caminhos gerados
            self.update_pheromones(paths)
            # Encontra o menor caminho e seu comprimento entre os caminhos gerados
            shortest_path, shortest_path_length = min(paths, key=lambda x: x[1])
            # Atualiza o melhor caminho encontrado se um caminho mais curto foi encontrado
            if shortest_path_length < self.best_path_length:
                self.best_path = shortest_path
                self.best_path_length = shortest_path_length
        df_paths = pd.DataFrame(dict_paths).T
        df_paths.rename(columns={col: f'Ant_{col+1}' for col in df_paths.columns}, inplace=True)
        return df_paths
    
mapeamento_estados = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}