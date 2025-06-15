# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    Lida com valores None para os campos de entrada.
    """
    output_final = []

    # Tabela de mapeamento para os códigos 319 e seus excedentes
    # Os nomes das chaves (PASSEIO, RUA, ASPHALTIC) devem estar em MAIÚSCULAS
    tabela_319 = {
        'PASSEIO': {
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3810',
                    (1.25, 2.00): '3811',
                    (2.00, 3.00): '3812',
                    (3.00, 5.00): '3813'
                },
                'codigo_excedente_mts': '3811'
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
                    (0.0, 1.25): '3850',
                    (1.25, 2.00): '3851',
                    (2.00, 3.00): '3852',
                    (3.00, 5.00): '3853'
                },
                'codigo_excedente_mts': '3851'
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
        'ASPHALTIC': { # Supondo que "Asfaltico" do HTML mapeia para "ASPHALTIC" na tabela
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3880',
                    (1.25, 2.00): '3881',
                    (2.00, 3.00): '3882',
                    (3.00, 5.00): '3883'
                },
                'codigo_excedente_mts': '3881'
            },
            'TROCA PARCIAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3890',
                    (1.25, 2.00): '3891',
                    (2.00, 3.00): '3892',
                    (3.00, 5.00): '3893'
                },
                'codigo_excedente_mts': '3891'
            },
            'TROCA TOTAL': {
                'profundidades_base': {
                    (0.0, 1.25): '3900',
                    (1.25, 2.00): '3901',
                    (2.00, 3.00): '3902',
                    (3.00, 5.00): '3903'
                },
                'codigo_excedente_mts': '3901'
            }
        }
    }

    for item in lista_itens_adicionados:
        codigo_original = item.get('codigo')
        pavimento_input = item.get('pavimento')
        troca_input = item.get('troca')
        profundidade_input = item.get('profundidade')
        mts_tubo_batido_input = item.get('mts_tubo_batido')
        diametro_input = item.get('diametro')

        linha_formatada = ""

        # --- Processamento para '313 codigos' ---
        if codigo_original == '313 codigos':
            pavimento_str = ""
            if pavimento_input: # Verifica se não é None ou string vazia
                pavimento_str = str(pavimento_input)[0].upper() # Pega a primeira letra e garante maiúscula
            
            troca_str = ""
            if troca_input == "Sem Troca":
                troca_str = "ST"
            elif troca_input == "Troca Parcial":
                troca_str = "TP"
            elif troca_input == "Troca Total":
                troca_str = "TT"
            linha_formatada = f"313;{pavimento_str};{troca_str}"
            
        # --- Processamento para '320 (rec) codigos' ---
        elif codigo_original == '320 (rec) codigos':
            pavimento_str = ""
            if pavimento_input: # Verifica se não é None ou string vazia
                pavimento_str = str(pavimento_input)[0].upper()
            
            troca_str = ""
            if troca_input == "Sem Troca":
                troca_str = "ST"
            elif troca_input == "Troca Parcial":
                troca_str = "TP"
            elif troca_input == "Troca Total":
                troca_str = "TT"
            
            profundidade_val = None
            if profundidade_input: # Verifica se não é None ou string vazia
                try:
                    profundidade_val = float(str(profundidade_input).replace(',', '.'))
                except ValueError:
                    profundidade_val = 0.0 # Valor padrão em caso de erro de conversão
            
            # Formata a profundidade com 2 casas decimais, usando vírgula
            profundidade_formatada = f"{profundidade_val:.2f}".replace('.', ',') if profundidade_val is not None else ""
            linha_formatada = f"320 (rec);{pavimento_str};{troca_str};{profundidade_formatada}"

        # --- Processamento para '319 codigos' ---
        elif codigo_original == '319 codigos':
            pavimento_norm = None
            if pavimento_input: # Apenas tenta strip/upper se houver valor
                pavimento_norm = str(pavimento_input).strip().upper()

            troca_norm = None
            if troca_input: # Apenas tenta strip/upper se houver valor
                troca_norm = str(troca_input).strip().upper()
            
            profundidade_val = None
            if profundidade_input:
                try:
                    profundidade_val = float(str(profundidade_input).replace(',', '.'))
                except ValueError:
                    pass # Deixa como None se não puder converter
            
            mts_tubo_batido_val = None
            if mts_tubo_batido_input:
                try:
                    mts_tubo_batido_val = float(str(mts_tubo_batido_input).replace(',', '.'))
                except ValueError:
                    pass # Deixa como None se não puder converter

            codigo_base = None
            codigo_excedente = None
            
            # --- Mapeamento de nomes de pavimento do HTML para a tabela ---
            if pavimento_norm == "ASFALTICO":
                pavimento_norm = "ASPHALTIC" 

            # Garante que temos dados válidos antes de tentar buscar na tabela
            if pavimento_norm and troca_norm and profundidade_val is not None:
                if pavimento_norm in tabela_319 and troca_norm in tabela_319[pavimento_norm]:
                    prof_info = tabela_319[pavimento_norm][troca_norm]['profundidades_base']
                    
                    # Encontrar o código base pela profundidade
                    for (min_prof, max_prof), cod in prof_info.items():
                        if min_prof <= profundidade_val <= max_prof:
                            codigo_base = cod
                            break
                    
                    # Se profundidade_val > 5.00m, usar o código da última faixa (3.00, 5.00)
                    if codigo_base is None and profundidade_val > 5.00:
                        # Encontra o último código na ordem dos intervalos
                        last_range_code = None
                        sorted_ranges = sorted(prof_info.keys())
                        if sorted_ranges:
                            last_range_code = prof_info[sorted_ranges[-1]] # Pega o código da última faixa
                        if last_range_code:
                            codigo_base = last_range_code
                        
                    codigo_excedente = tabela_319[pavimento_norm][troca_norm]['codigo_excedente_mts']
                else:
                    linha_formatada = f"319;ERRO: Combinação de Pavimento '{pavimento_input}' / Troca '{troca_input}' inválida para código 319."
            else:
                linha_formatada = f"319;ERRO: Dados de Pavimento, Troca ou Profundidade incompletos para o código 319. (Pav: {pavimento_input}, Troca: {troca_input}, Prof: {profundidade_input})"


            if codigo_base: # Se o código base foi encontrado, monta a linha
                linha_formatada = f"319;{codigo_base}"
                if mts_tubo_batido_val is not None and mts_tubo_batido_val > 0:
                    linha_formatada += f";{codigo_excedente};{mts_tubo_batido_val:.2f}".replace('.', ',')
            # Se codigo_base não foi encontrado, a linha_formatada já terá a mensagem de erro da lógica acima.
        
        else: # Para outros códigos que não exigem lógica específica (como 300, 343, 329, etc.)
            linha_formatada = codigo_original # Apenas o código como está na lista

        output_final.append(linha_formatada)

    return output_final

# Exemplo de uso (para testes)
if __name__ == '__main__':
    print("--- Teste de processamento de códigos 313, 320(rec), 319 e outros ---")
    
    test_data = [
        # Testes para 313
        {'codigo': '313 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '', 'mts_tubo_batido': '', 'diametro': ''}, # Esperado: 313;P;ST
        {'codigo': '313 codigos', 'pavimento': 'Rua', 'troca': 'Troca Parcial', 'profundidade': '', 'mts_tubo_batido': '', 'diametro': ''},  # Esperado: 313;R;TP
        {'codigo': '313 codigos', 'pavimento': 'Asfaltico', 'troca': 'Troca Total', 'profundidade': '', 'mts_tubo_batido': '', 'diametro': ''},# Esperado: 313;A;TT
        {'codigo': '313 codigos', 'pavimento': None, 'troca': None, 'profundidade': '', 'mts_tubo_batido': '', 'diametro': ''}, # Esperado: 313;;
        
        # Testes para 320 (rec)
        {'codigo': '320 (rec) codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1,23', 'mts_tubo_batido': '', 'diametro': ''}, # Esperado: 320 (rec);P;ST;1,23
        {'codigo': '320 (rec) codigos', 'pavimento': 'Rua', 'troca': 'Troca Parcial', 'profundidade': '0.5', 'mts_tubo_batido': '', 'diametro': ''},  # Esperado: 320 (rec);R;TP;0,50
        {'codigo': '320 (rec) codigos', 'pavimento': 'Asfaltico', 'troca': 'Troca Total', 'profundidade': '4.8', 'mts_tubo_batido': '', 'diametro': ''},# Esperado: 320 (rec);A;TT;4,80
        {'codigo': '320 (rec) codigos', 'pavimento': None, 'troca': None, 'profundidade': None, 'mts_tubo_batido': '', 'diametro': ''}, # Esperado: 320 (rec);;;
        
        # Testes para 319 (com Pavimento, Troca, Profundidade e MTS Tubo Batido)
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '1.5', 'mts_tubo_batido': '2.0', 'diametro': '100'}, # Esperado: 319;3811;3811;2,00
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Troca Total', 'profundidade': '4,25', 'mts_tubo_batido': '1.0', 'diametro': '200'},   # Esperado: 319;3873;3871;1,00
        {'codigo': '319 codigos', 'pavimento': 'Asfaltico', 'troca': 'Troca Parcial', 'profundidade': '0.8', 'mts_tubo_batido': '0.5', 'diametro': ''},# Esperado: 319;3890;3891;0,50
        
        # Testes 319 - Profundidade > 5.00m (deve pegar o último código base da faixa 3.00-5.00)
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': '6.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: 319;3813;3811;1,50
        
        # Testes 319 - Com valores incompletos/inválidos
        {'codigo': '319 codigos', 'pavimento': None, 'troca': 'Sem Troca', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': None, 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Sem Troca', 'profundidade': None, 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Passeio', 'troca': 'Invalida', 'profundidade': '1.0', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO
        {'codigo': '319 codigos', 'pavimento': 'Rua', 'troca': 'Sem Troca', 'profundidade': 'abc', 'mts_tubo_batido': '1.5', 'diametro': ''}, # Esperado: ERRO (profundidade inválida)
        
        # Testes para outros códigos (que não precisam de lógica específica)
        {'codigo': '300 codigos', 'pavimento': None, 'troca': None, 'profundidade': None, 'mts_tubo_batido': None, 'diametro': None}, # Esperado: 300 codigos
        {'codigo': '329 codigos', 'pavimento': '', 'troca': '', 'profundidade': '', 'mts_tubo_batido': '', 'diametro': ''}, # Esperado: 329 codigos
        {'codigo': '343 codigos', 'pavimento': 'Qualquer', 'troca': 'Coisa', 'profundidade': '10', 'mts_tubo_batido': '5', 'diametro': '300'}, # Esperado: 343 codigos
    ]

    resultados = processar_codigos(test_data)
    for r in resultados:
        print(r)