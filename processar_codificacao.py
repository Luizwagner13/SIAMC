# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    """
    output_final = []

    # Tabela de mapeamento para os códigos 319 e seus excedentes
    tabela_319 = {
        'PASSEIO': {
            'SEM TROCA': {
                'profundidades_base': {
                    (0.0, 1.25): '3810',
                    (1.25, 2.00): '3811', # Código base para esta faixa E código de excedente
                    (2.00, 3.00): '3812',
                    (3.00, 5.00): '3813'
                },
                'codigo_excedente_mts': '3811' # O código para o excedente de MTS (conforme discutido)
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
                    (0.0, 1.25): '3075',
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


    print(f"DEBUG: Processando {len(lista_itens_adicionados)} itens.")
    for item in lista_itens_adicionados:
        print(f"DEBUG: Processando item: {item}")
        codigo_input = item.get('codigo')
        
        # --- Lógica para o código 313 ---
        if codigo_input == '313':
            pavimento_input = item.get('pavimento', '').strip().upper()
            try:
                profundidade_input = float(item.get('profundidade', '').replace(',', '.') or 0.0)
            except ValueError:
                profundidade_input = 0.0 

            codigo_gerado = None
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
                print(f"DEBUG: 313 - Código gerado: {codigo_gerado}")
            else:
                error_msg = f'313 - Erro: Não foi possível determinar o código para Pavimento: {item.get("pavimento")}, Profundidade: {item.get("profundidade")}. Verifique os valores.')
                output_final.append(error_msg)
                print(f"DEBUG: 313 - ERRO: {error_msg}")
        
        # --- Lógica para o código 319 ---
        elif codigo_input == '319':
            pavimento_input = item.get('pavimento', '').strip().upper()
            troca_input = item.get('troca', '').strip().upper()
            
            try:
                profundidade_input = float(item.get('profundidade', '').replace(',', '.') or 0.0)
            except ValueError:
                profundidade_input = 0.0 
                print(f"DEBUG: 319 - Profundidade inválida: {item.get('profundidade')}, usando 0.0")

            try:
                mts_tubo_batido_input = float(item.get('mts_tubo_batido', '').replace(',', '.') or 0.0)
            except ValueError:
                mts_tubo_batido_input = 0.0 
                print(f"DEBUG: 319 - MTS Tubo Batido inválido: {item.get('mts_tubo_batido')}, usando 0.0")

            if pavimento_input in tabela_319 and troca_input in tabela_319[pavimento_input]:
                regras = tabela_319[pavimento_input][troca_input]
                
                codigo_base = None
                for (min_prof, max_prof), cod in regras['profundidades_base'].items():
                    if min_prof <= profundidade_input <= max_prof:
                        codigo_base = cod
                        break
                
                if not codigo_base:
                    if profundidade_input > 5.00:
                        codigo_base = list(regras['profundidades_base'].values())[-1] 
                        output_final.append(f'{codigo_base} - 1 UNIDADE (Profundidade > 5.00m)')
                        print(f"DEBUG: 319 - Profundidade > 5.00m, usando código base: {codigo_base}")
                    else:
                        error_msg = f'319 - Erro: Profundidade "{item.get("profundidade")}" fora das faixas para Pavimento: {item.get("pavimento")}, Troca: {item.get("troca")}'
                        output_final.append(error_msg)
                        print(f"DEBUG: 319 - ERRO: {error_msg}")
                else:
                    output_final.append(f'{codigo_base} - 1 UNIDADE')
                    print(f"DEBUG: 319 - Código base determinado: {codigo_base}")

                if mts_tubo_batido_input > 2.00:
                    codigo_excedente = regras['codigo_excedente_mts']
                    quantidade_excedente = mts_tubo_batido_input - 2.00
                    output_final.append(f'{codigo_excedente} - {quantidade_excedente:.2f} MTS')
                    print(f"DEBUG: 319 - Excedente gerado: {codigo_excedente} - {quantidade_excedente:.2f} MTS")

            else:
                error_msg = f'319 - Erro: Combinação Pavimento "{item.get("pavimento")}" / Troca "{item.get("troca")}" não encontrada na tabela.'
                output_final.append(error_msg)
                print(f"DEBUG: 319 - ERRO: {error_msg}")

        # --- Lógica para outros códigos (ainda não implementada) ---
        else:
            output_final.append(f'{codigo_input} - Lógica de codificação pendente.')
            print(f"DEBUG: Código {codigo_input} - Lógica pendente.")
            
    if not output_final:
        output_final.append("Nenhum código válido foi gerado. Verifique os inputs.")
        print("DEBUG: Nenhum código válido foi gerado.")
            
    print(f"DEBUG: Final output_final antes do retorno: {output_final}")
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