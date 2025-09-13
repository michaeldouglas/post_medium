from typing import List
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Agent:
    def __init__(self, goal: str):
        self.goal = goal
        self.memory = []

    def think(self) -> str:
        """Decide o próximo passo baseado no goal + memória."""
        prompt = f"""
Você é um agente autônomo com objetivo: {self.goal}
Memória/Histórico: {self.memory}

Que próxima tarefa você deve fazer para progredir rumo ao objetivo?
Liste apenas uma tarefa de cada vez.
"""
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um agente inteligente."},
                {"role": "user", "content": prompt}
            ]
        )
        task = resp.choices[0].message.content.strip()
        return task

    def act(self, task: str) -> str:
        """Executa a tarefa com simulação de resultados reais."""
        task_lower = task.lower()

        if "distância" in task_lower or "marte" in task_lower:
            distance = "A distância atual aproximada da Terra até Marte é 225 milhões de km."
            return distance

        elif "observação" in task_lower or "céu noturno" in task_lower:
            suggestions = (
                "Para observar Marte, olhe para o céu sudoeste após o pôr do sol. "
                "Use binóculos ou telescópio para melhor visualização."
            )
            return suggestions

        elif "analisar" in task_lower or "recomendação" in task_lower:
            analysis = (
                "Com base na distância atual e condições do céu, a melhor hora para observar Marte "
                "é entre 19h e 22h nos próximos 3 dias. Prefira locais com pouca poluição luminosa."
            )
            return analysis

        else:
            return f"Não sei executar a tarefa '{task}' ainda"

    def update_memory(self, info: str):
        """Atualiza memória mantendo os últimos 5 registros."""
        self.memory.append(info)
        if len(self.memory) > 5:
            self.memory.pop(0)

    def run(self, steps: int = 3):
        """Executa o agente por N passos."""
        for i in range(steps):
            task = self.think()
            print(f"[AGENTE] Próxima tarefa: {task}")
            outcome = self.act(task)
            print(f"[AGENTE] Resultado: {outcome}")
            self.update_memory(f"Tarefa: {task} -> {outcome}")

if __name__ == "__main__":
    agente = Agent(
        goal="Obter informações sobre a distância da Terra até Marte e dar sugestões de observação astronômica"
    )
    agente.run(steps=4)
