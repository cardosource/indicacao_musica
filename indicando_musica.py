import numpy as np
import skfuzzy as fuzz
from skfuzzy import control

mais_tocadas = dict()
mais_tocadas[1] =  "Musica 1 - cantor a"
mais_tocadas[2] =  "Musica 2 - cantor b"
mais_tocadas[3] =  "Musica 3 - cantor c"
mais_tocadas[4] =  "Musica 4 - cantor d"
mais_tocadas[5] =  "Musica 5 - cantor e"
mais_tocadas[6] =  "Musica 6 - cantor f"
mais_tocadas[7] =  "Musica 7 - cantor g"
mais_tocadas[8] =  "Musica 8 - cantor h"
mais_tocadas[9] =  "Musica 9 - cantor i"
mais_tocadas[10] = "Musica 10 - cantor j"
mais_tocadas[11] = "Musica 11 - cantor l"
mais_tocadas[12] = "Musica 12 - cantor m"
mais_tocadas[13] = "Musica 13 - cantor n"
mais_tocadas[14] = "Musica 14 - cantor o"
mais_tocadas[15] = "Musica 15 - cantor A"
mais_tocadas[16] = "Musica 16 - cantor B"
mais_tocadas[17] = "Musica 17 - cantor C"
mais_tocadas[18] = "Musica 18 - cantor D"
mais_tocadas[19] = "Musica 19 - cantor E"
mais_tocadas[20] = "Musica 20 - cantor F"


minha_play_list = control.Antecedent(np.arange(0,11,1),'minha play list')
as_mais_ouvidas = control.Antecedent(np.arange(0,11,1), 'as mais ouvidas')
sugestao = control.Consequent(np.arange(0,len(mais_tocadas)+1,1),'sugestao')


minha_play_list.automf(number=3,names=['ruim','boa','gostei'])
as_mais_ouvidas.automf(number=3,names=['ruim','gostei','boa'])

sugestao['baixa'] = fuzz.trimf(sugestao.universe, [0, 0, 7])
sugestao['media'] = fuzz.trimf(sugestao.universe, [6, 10, 12])
sugestao['alta'] = fuzz.trimf(sugestao.universe, [5, 20, 20])

regra1 = control.Rule(minha_play_list['ruim'] | as_mais_ouvidas['ruim'], sugestao['baixa'])
regra2 = control.Rule(as_mais_ouvidas['boa'],sugestao['media'])
regra3 = control.Rule(as_mais_ouvidas['gostei'] | minha_play_list['gostei'],sugestao['alta'])

sistema_controle = control.ControlSystem( [regra1,regra2,regra3])
sistema = control.ControlSystemSimulation(sistema_controle)

sistema.input['minha play list'] = 10 # Avaliação pessoal
sistema.input['as mais ouvidas'] = 2 #Avalização de mais tocada

sistema.compute()
resultado = sistema.output['sugestao']

arredondamento_para_menos = round(resultado-0.5)
arredondamento_para_mais = round(resultado+0.5)

print(f'valor puro : {resultado}\n'
      f'Arredondamento para mais : {arredondamento_para_mais}\n'
      f'Arredondamento para menos : {arredondamento_para_menos}')
print("-"*50)
print(f'Musica sugerida  : {mais_tocadas[arredondamento_para_mais]}\n'
      f'Musica sugerida  : {mais_tocadas[arredondamento_para_menos]}')
sugestao.view(sim=sistema)