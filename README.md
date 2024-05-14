# Byte-compiled / optimized Python files
__pycache__/
*.py[cod]

# Dependency directories
venv/
env/
ENV/
.venv/

# Distribution directories
build/
dist/

# Compiled files
*.exe
*.dll
*.so
*.dylib

# Miscellaneous
.DS_Store

# Late at Night - Documentação do Jogo em Pygame

## Visão Geral

Late at Night é um jogo simples baseado em Pygame, onde o jogador navega por um quarto escuro, evitando obstáculos e coletando itens para progredir através dos níveis. O objetivo é alcançar o interruptor localizado em posições aleatórias ao longo das bordas do quarto.

## Instalação

Antes de executar o jogo, certifique-se de ter o Python e o Pygame instalados em seu sistema.

1. Clone o repositório para sua máquina local:
   ```bash
   git clone https://github.com/seu-nome-de-usuário/LateAtNight.git

# Navegue até o diretório do projeto:

```bash
cd LateAtNight
```

# Instale o Pygame usando o pip:

```bash
pip install pygame
```

## Utilização
Para iniciar o jogo, execute o seguinte comando em seu terminal:

```bash
python late_at_night.py
```

# Controles
Use as teclas de seta para mover o personagem do jogador.
Evite obstáculos e colete itens espalhados pelo quarto.
Alcance o interruptor localizado ao longo das bordas do quarto para avançar para o próximo nível.

# Jogabilidade
O jogador começa em uma posição aleatória dentro do quarto.
Brinquedos estão espalhados pelo quarto, que o jogador pode coletar.
Pisar em um brinquedo incrementa o contador de brinquedos para o nível atual.
Após coletar todos os brinquedos, o jogador deve navegar até o interruptor para completar o nível e avançar para o próximo.
Cada nível aumenta em dificuldade, com mais brinquedos para coletar e obstáculos para evitar.

## Contribuições
Contribuições para Late at Night são bem-vindas! Se você gostaria de contribuir com o projeto, siga estas etapas:

 1. Faça um fork do repositório no GitHub.

 2. Crie um novo branch para sua funcionalidade ou correção de bug:
```bash
git checkout -b nome-da-funcionalidade
```
 3. Faça suas alterações e as envie com mensagens de commit descritivas:
```bash
git add .
git commit -m "Adicionar funcionalidade ou corrigir bug"
```
 4. Envie suas alterações para o seu fork:
``` bash
git push origin nome-da-funcionalidade
```

 5. Abra um pull request no GitHub, descrevendo suas alterações e seu impacto.

## Licença
Este projeto está licenciado sob a Licença GNU. Consulte o arquivo LICENSE para obter mais detalhes