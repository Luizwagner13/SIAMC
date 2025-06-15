# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    """
    output_final = []

    # Tabela de mapeamento para os códigos 319 e seus excedentes
    # Formato: { 'PAVIMENTO': { 'TROCA': { 'codigos_base_por_profundidade': { (min_prof, max_prof): 'CODIGO' }, 'codigo_excedente': 'CODIGO' } } }
    # Usamos float('inf') para profundidade máxima para a última faixa
    tabela_319 = {
        'PASSEIO': {
            'SEM TROCA': {
                'codigos_base_por_profundidade': {
                    (0.0, 1.25): '3810',  # ATÉ 1,25
                    (1.25, 2.00): '3811', # DE 1,25 A 2,00 (Este é o código para excedente na tabela? Revisei, na sua tabela 3811 parece ser para "EXCEDENTE" e para "1,25 A 2,00". Preciso de um esclarecimento aqui.)
                                         # Baseado na conversação anterior, 3811 era o EXCEDENTE.
                                         # Se 3811 é para 1.25-2.00 e para EXCEDENTE, preciso de mais clareza.
                                         # Vamos usar 3810 como base até 2.00 e 3811 como excedente, como no exemplo.
                                         # Para 1.25 A 2.00: 3811
                                         # Para 2.00 A 3.00: 3812
                                         # Para 3.00 A 5.00: 3813
                                         # O 3811 aparece em "PROFUNDIDADE" e "UNIDADE E EXCEDENTE".

                                         # Tentativa de interpretar a tabela (linha 3180/3810):
                                         # Se prof <= 1.25 => 3810 (1 UNIDADE)
                                         # Se 1.25 < prof <= 2.00 => 3811 (1 UNIDADE)
                                         # Se 2.00 < prof <= 3.00 => 3812 (1 UNIDADE)
                                         # Se 3.00 < prof <= 5.00 => 3813 (1 UNIDADE)
                                         # O "EXCEDENTE" 3811 na coluna UNIDADE E EXCEDENTE indica que ele é usado para o cálculo de metros excedentes.
                                         # OU seja, o 3811 tanto é um código base para uma faixa de profundidade, quanto o código para o excedente em metros.
                                         # Isso pode gerar confusão, mas vou seguir essa lógica por enquanto.

                                         # REVISÃO:
                                         # Baseando-me novamente no seu exemplo:
                                         # Ex: Profundidade 3.5m (PASSEIO, SEM TROCA) -> 3810 - 1 UNIDADE E 3811 - 1.5 MTS
                                         # Isso sugere que o 3810 é o "código base" para a parte inicial (até 2m de tubo batido),
                                         # e o 3811 é o "código de excedente".
                                         # A tabela mostra 3810 para até 1.25m, e 3811 para 1.25 a 2.00m.
                                         # Isso é um conflito.

                                         # **PRECISO QUE VOCÊ CONFIRME QUAL CÓDIGO É O "BASE" ATÉ 2 MTS DE TUBO BATIDO, E QUAL É O "EXCEDENTE"**
                                         # SEGUINDO SEU ÚLTIMO EXEMPLO:
                                         # "3177 - 1 UNIDADE" (para até 2.00mts de tubo batido)
                                         # "3178 - 1,5 MTS" (para o excedente)
                                         # Esses 3177 e 3178 NÃO ESTÃO NA TABELA QUE VOCÊ ME DEU.
                                         # A tabela tem:
                                         # PASSEIO / SEM TROCA: 3810 (até 1.25), 3811 (1.25 a 2.00), 3812 (2.00 a 3.00), 3813 (3.00 a 5.00)
                                         # E para "EXCEDENTE" na mesma linha do 3811 está "3811".

                                         # **VOU ASSUMIR A SEGUINTE REGRA COM BASE NOS CÓDIGOS DA TABELA E SEU ÚLTIMO EXEMPLO DE LÓGICA:**
                                         # 1. O código base para "1 UNIDADE" é determinado pela `profundidade` informada.
                                         # 2. O código para "EXCEDENTE" é **sempre o código da segunda faixa de profundidade da tabela (1,25 A 2,00)**.
                                         #    Ex: Para PASSEIO/SEM TROCA, o 3811 seria o código de excedente.
                                         #    Para PASSEIO/TROCA PARCIAL, o 3831 seria o código de excedente.
                                         #    Para PASSEIO/TROCA TOTAL, o 3841 seria o código de excedente.
                                         # ESTA É A INTERPRETAÇÃO MAIS LÓGICA COM BASE NA TABELA E SEUS EXEMPLOS.


                # Mapeamento dos códigos base do 319 por profundidade (até 5.00m)
                # O último código (por exemplo, 3813 para Passeio/Sem Troca) será o código base se a profundidade for > 3.00
                'profundidades_base': {
                    (0.0, 1.25): '3810',
                    (1.25, 2.00): '3811', # Este é um código base para 1.25 a 2.00
                    (2.00, 3.00): '3812',
                    (3.00, 5.00): '3813' # Máximo 5.00m de profundidade
                },
                'codigo_excedente_mts': '3811' # O código para o excedente de MTS
            },
            'TROCA PARCIAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3830',
                    (1.25, 2.00): '3831',
                    (2.00, 3.00): '3832',
                    (3.00, 5.00): '3833'
                },
                'codigo_excedente_mts': '3831'
            },
            'TROCA TOTAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3840',
                    (1.25, 2.00): '3841',
                    (2.00, 3.00): '3842',
                    (3.00, 5.00): '3843'
                },
                'codigo_excedente_mts': '3841'
            }
        },
        'RUA': {
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3446',
                    (1.25, 2.00): '3447',
                    (2.00, 3.00): '3448',
                    (3.00, 5.00): '3449'
                },
                'codigo_excedente_mts': '3447'
            },
            'TROCA PARCIAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3860',
                    (1.25, 2.00): '3861',
                    (2.00, 3.00): '3862',
                    (3.00, 5.00): '3863'
                },
                'codigo_excedente_mts': '3861'
            },
            'TROCA TOTAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3870',
                    (1.25, 2.00): '3871',
                    (2.00, 3.00): '3872',
                    (3.00, 5.00): '3873'
                },
                'codigo_excedente_mts': '3871'
            }
        },
        'TERRA': {
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3075', # Este já era usado no 313 (TERRA, <=1.25)
                    (1.25, 2.00): '3409',
                    (2.00, 3.00): '3410',
                    (3.00, 5.00): '3411'
                },
                'codigo_excedente_mts': '3409'
            },
            'TROCA PARCIAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3780',
                    (1.25, 2.00): '3781',
                    (2.00, 3.00): '3782',
                    (3.00, 5.00): '3783'
                },
                'codigo_excedente_mts': '3781'
            },
            'TROCA TOTAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3790',
                    (1.25, 2.00): '3791',
                    (2.00, 3.00): '3792',
                    (3.00, 5.00): '3793'
                },
                'codigo_excedente_mts': '3791'
            }
        }
    }


    for item in lista_itens_adicionados:
        codigo_input = item.get('codigo')
        
        # --- Lógica para o código 313 ---
        if codigo_input == '313':
            pavimento_input = item.get('pavimento', '').strip().upper()
            try:
                profundidade_input = float(item.get('profundidade', '').replace(',', '.') or 0.0)
            except ValueError:
                profundidade_input = 0.0 

            codigo_gerado = None
            # Mapeamento de 313: PAVIMENTO -> PROFUNDIDADE -> CODIGO
            mapa_313 = {
                'CIMENTO': {
                    (0.0, 1.25): '3078',
                    (1.25, 2.00): '3412',
                    (2.00, 3.00): '3413'
                },
                'TERRA': {
                    (0.0, 1.25): '3075',
                    (1.25, 2.00): '3409',
                    (2.00, 3.00): '3410'
                }
            }

            if pavimento_input in mapa_313:
                for (min_prof, max_prof), cod in mapa_313[pavimento_input].items():
                    if min_prof <= profundidade_input <= max_prof:
                        codigo_gerado = cod
                        break
            
            if codigo_gerado:
                output_final.append(f'{codigo_gerado} - 1 unidade')
            else:
                output_final.append(f'313 - Erro: Não foi possível determinar o código para Pavimento: {item.get("pavimento")}, Profundidade: {item.get("profundidade")}. Verifique os valores.')
        
        # --- Lógica para o código 319 ---
        elif codigo_input == '319':
            pavimento_input = item.get('pavimento', '').strip().upper()
            troca_input = item.get('troca', '').strip().upper()
            
            try:
                profundidade_input = float(item.get('profundidade', '').replace(',', '.') or 0.0)
            except ValueError:
                profundidade_input = 0.0 # Valor padrão para profundidade inválida

            try:
                # O novo campo mts_tubo_batido
                mts_tubo_batido_input = float(item.get('mts_tubo_batido', '').replace(',', '.') or 0.0)
            except ValueError:
                mts_tubo_batido_input = 0.0 # Valor padrão para mts_tubo_batido inválido

            # Validar se a combinação Pavimento/Troca existe na tabela
            if pavimento_input in tabela_319 and troca_input in tabela_319[pavimento_input]:
                regras = tabela_319[pavimento_input][troca_input]
                
                # 1. Determinar o CÓDIGO BASE pela profundidade
                codigo_base = None
                for (min_prof, max_prof), cod in regras['profundidades_base'].items():
                    if min_prof <= profundidade_input <= max_prof:
                        codigo_base = cod
                        break
                
                if not codigo_base:
                    # Se a profundidade for maior que a máxima definida (5.00m), ainda usa o último código da faixa
                    if profundidade_input > 5.00:
                        # Pega o último código base da faixa (ex: 3813 para Passeio/Sem Troca)
                        codigo_base = list(regras['profundidades_base'].values())[-1] 
                        output_final.append(f'{codigo_base} - 1 UNIDADE (Profundidade > 5.00m)')
                    else:
                        output_final.append(f'319 - Erro: Profundidade "{item.get("profundidade")}" fora das faixas para Pavimento: {item.get("pavimento")}, Troca: {item.get("troca")}')
                        continue # Pula para o próximo item
                else:
                    output_final.append(f'{codigo_base} - 1 UNIDADE')

                # 2. Lógica para o EXCEDENTE de MTS DE TUBO BATIDO
                if mts_tubo_batido_input > 2.00: # Se exceder 2.00mts
                    codigo_excedente = regras['codigo_excedente_mts']
                    quantidade_excedente = mts_tubo_batido_input - 2.00
                    # Formata o excedente para duas casas decimais
                    output_final.append(f'{codigo_excedente} - {quantidade_excedente:.2f} MTS')

            else:
                output_final.append(f'319 - Erro: Combinação Pavimento "{item.get("pavimento")}" / Troca "{item.get("troca")}" não encontrada na tabela.')

        # --- Lógica para outros códigos (ainda não implementada) ---
        else:
            output_final.append(f'{codigo_input} - Lógica de codificação pendente.')
            
    return output_final

if __name__ == '__main__':
    # --- Testes manuais para processar_codificacao.py ---
    print("\n--- Testes para processar_codificacao.py ---")

    # Testes para o código 313
    print("\n--- Testes para 313 ---")
    test_data_313 = [
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '1.0', 'troca': '', 'diametro': '', 'mts_tubo_batido': ''},
        {'codigo': '313', 'pavimento': 'Terra', 'profundidade': '2.5', 'troca': '', 'diametro': '', 'mts_tubo_batido': ''},
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '1.25', 'troca': '', 'diametro': '', 'mts_tubo_batido': ''},
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '1.26', 'troca': '', 'diametro': '', 'mts_tubo_batido': ''},
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '4.0', 'troca': '', 'diametro': '', 'mts_tubo_batido': ''}, # Fora do range (erro esperado)
    ]
    resultados_313 = processar_codigos(test_data_313)
    for res in resultados_313:
        print(res)

    # Testes para o código 319
    print("\n--- Testes para 319 ---")
    test_data_319 = [
        # Exemplo 1: Sem excedente de MTS (MTS_TUBO_BATIDO <= 2.00)
        {'codigo': '319', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''},
        {'codigo': '319', 'pavimento': 'Rua', 'troca': 'Troca Parcial', 'profundidade': '2.0', 'mts_tubo_batido': '2.0', 'diametro': ''},
        {'codigo': '319', 'pavimento': 'Terra', 'troca': 'Troca Total', 'profundidade': '0.5', 'mts_tubo_batido': '0.8', 'diametro': ''},

        # Exemplo 2: Com excedente de MTS (MTS_TUBO_BATIDO > 2.00)
        {'codigo': '319', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '3.5', 'mts_tubo_batido': '3.5', 'diametro': ''}, # Excedente de 1.5 MTS
        {'codigo': '319', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': '4.8', 'mts_tubo_batido': '5.25', 'diametro': ''}, # Excedente de 3.25 MTS
        {'codigo': '319', 'pavimento': 'Passeio', 'troca': 'Troca Parcial', 'profundidade': '2.8', 'mts_tubo_batido': '2.1', 'diametro': ''}, # Excedente de 0.1 MTS

        # Testes com valores inválidos/fora do esperado
        {'codigo': '319', 'pavimento': 'Asfaltico', 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Pavimento inválido
        {'codigo': '319', 'pavimento': 'Passeio', 'troca': 'Invalida', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Troca inválida
        {'codigo': '319', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '6.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Profundidade > 5.00m (deve pegar o último código base)
        {'codigo': '319', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': 'A', 'mts_tubo_batido': 'B', 'diametro': ''}, # Valores não numéricos
    ]
    resultados_319 = processar_codigos(test_data_319)
    for res in resultados_319:
        print(res)

    # Teste de código pendente
    print("\n--- Teste de código pendente ---")
    test_data_pendente = [
        {'codigo': '320', 'pavimento': '', 'profundidade': '', 'troca': '', 'diametro': '', 'mts_tubo_batido': ''}
    ]
    resultados_pendente = processar_codigos(test_data_pendente)
    for res in resultados_pendente:
        print(res)