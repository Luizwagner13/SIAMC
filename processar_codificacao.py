# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    Lida com valores None para os campos de entrada.
    """
    output_final = []

    # Tabela de mapeamento para os códigos 319 e seus excedentes
    # Os nomes das chaves (PASSEIO, RUA, TERRA) devem estar em MAIÚSCULAS
    # NOTA: Embora a tabela contenha 'profundidades_base' e 'codigo_excedente_mts',
    # para o código 319 com 'mts_tubo_batido', os códigos '3850' e '3851'
    # serão usados diretamente conforme a solicitação do usuário para a saída.
    # Esta tabela ainda é útil para validação e outros códigos.
    tabela_319 = {
        'PASSEIO': {
            'SEM TROCA': {
                'profundidades_base': { (0.0, 1.25): '3810', (1.25, 2.00): '3811', (2.00, 3.00): '3812', (3.00, 5.00): '3813' },
                'codigo_excedente_mts': '3811'
            },
            'TROCA PARCIAL': {
                'profundidades_base': { (0.0, 1.25): '3830', (1.25, 2.00): '3831', (2.00, 3.00): '3832', (3.00, 5.00): '3833' },
                'codigo_excedente_mts': '3831'
            },
            'TROCA TOTAL': {
                'profundidades_base': { (0.0, 1.25): '3850', (1.25, 2.00): '3851', (2.00, 3.00): '3852', (3.00, 5.00): '3853' },
                'codigo_excedente_mts': '3851'
            }
        },
        'RUA': {
            'SEM TROCA': {
                'profundidades_base': { (0.0, 1.25): '3814', (1.25, 2.00): '3815', (2.00, 3.00): '3816', (3.00, 5.00): '3817' },
                'codigo_excedente_mts': '3815'
            },
            'TROCA PARCIAL': {
                'profundidades_base': { (0.0, 1.25): '3834', (1.25, 2.00): '3835', (2.00, 3.00): '3836', (3.00, 5.00): '3837' },
                'codigo_excedente_mts': '3835'
            },
            'TROCA TOTAL': {
                'profundidades_base': { (0.0, 1.25): '3854', (1.25, 2.00): '3855', (2.00, 3.00): '3856', (3.00, 5.00): '3857' },
                'codigo_excedente_mts': '3855'
            }
        },
        'TERRA': {
            'SEM TROCA': {
                'profundidades_base': { (0.0, 1.25): '3818', (1.25, 2.00): '3819', (2.00, 3.00): '3820', (3.00, 5.00): '3821' },
                'codigo_excedente_mts': '3819'
            },
            'TROCA PARCIAL': {
                'profundidades_base': { (0.0, 1.25): '3838', (1.25, 2.00): '3839', (2.00, 3.00): '3840', (3.00, 5.00): '3841' },
                'codigo_excedente_mts': '3839'
            },
            'TROCA TOTAL': {
                'profundidades_base': { (0.0, 1.25): '3858', (1.25, 2.00): '3859', (2.00, 3.00): '3860', (3.00, 5.00): '3861' },
                'codigo_excedente_mts': '3859'
            }
        }
    }


    for item in lista_itens_adicionados:
        codigo = item.get('codigo')
        pavimento = item.get('pavimento')
        troca = item.get('troca')
        profundidade = item.get('profundidade')
        mts_tubo_batido = item.get('mts_tubo_batido')
        diametro = item.get('diametro') 

        if codigo == '319':
            # Validações básicas (mantidas)
            if not all([pavimento, troca, profundidade, mts_tubo_batido]):
                output_final.append(f"{codigo};ERRO: Dados de Pavimento, Troca ou Profundidade/MTS incompletos para o código 319. (Pav: {pavimento}, Troca: {troca}, Prof: {profundidade}, MTS: {mts_tubo_batido})")
                continue

            try:
                profundidade_float = float(profundidade.replace(',', '.'))
                mts_tubo_batido_float = float(mts_tubo_batido.replace(',', '.'))
            except ValueError:
                output_final.append(f"{codigo};ERRO: Profundidade ou MTS de Tubo Batido inválidos para o código 319. (Prof: {profundidade}, MTS Tubo: {mts_tubo_batido})")
                continue

            pavimento_upper = (pavimento or '').upper()
            troca_upper = (troca or '').upper()

            # Validação do pavimento e troca com base na tabela
            if pavimento_upper not in tabela_319 or troca_upper not in tabela_319[pavimento_upper]:
                output_final.append(f"{codigo};ERRO: Dados de Pavimento ou Troca inválidos para o código 319. (Pav: {pavimento}, Troca: {troca})")
                continue

            # A lógica para o código 319 é específica conforme solicitação do usuário:
            # - Sempre retorna "3850 - 1 UNIDADE" para a unidade base do tubo batido (assumindo 2 metros).
            # - Se houver excedente de tubo batido (> 2 metros), retorna "3851 - X METROS".
            
            # Adiciona o código base do tubo batido
            output_final.append(f"3850 - 1 UNIDADE")

            # Calcula e adiciona o excedente de MTS de Tubo Batido
            if mts_tubo_batido_float > 2.0:
                excedente_mts = mts_tubo_batido_float - 2.0
                excedente_mts_formatado = f"{excedente_mts:.2f}".replace('.', ',')
                output_final.append(f"3851 - {excedente_mts_formatado} METROS")
            
            # NOTA IMPORTANTE: Com esta implementação, o código base da profundidade
            # (e.g., 3831 para 1.40m de profundidade em 'TROCA PARCIAL') NÃO está
            # sendo diretamente outputado para o código 319. A regra de saída para
            # 'mts_tubo_batido' está sobrepondo a saída principal para o 319.
            # Se o código da profundidade também precisar ser exibido em uma linha separada,
            # a lógica deverá ser revisada e precisaremos definir se ele vem antes, depois, etc.
            # No momento, a saída para 319 está focada estritamente no `3850` e `3851` conforme pedido.


        # --- Lógica para Outros Códigos (mantida como estava) ---
        elif codigo == '313':
            if not all([pavimento, profundidade]):
                output_final.append(f"{codigo};ERRO: Dados de Pavimento ou Profundidade incompletos para o código 313. (Pav: {pavimento}, Prof: {profundidade})")
                continue
            
            try:
                profundidade_float = float(profundidade.replace(',', '.'))
            except ValueError:
                output_final.append(f"{codigo};ERRO: Profundidade inválida para o código 313. (Prof: {profundidade})")
                continue

            pavimento_upper = (pavimento or '').upper()

            tabela_313 = {
                'CIMENTO': { (0.0, 1.00): '3611', (1.00, 2.00): '3612', (2.00, 5.00): '3613' },
                'TERRA': { (0.0, 1.00): '3614', (1.00, 2.00): '3615', (2.00, 5.00): '3616' }
            }
            if pavimento_upper not in tabela_313:
                 output_final.append(f"{codigo};ERRO: Pavimento inválido para o código 313. (Pav: {pavimento})")
                 continue
            
            codigo_base_313 = None
            for (min_p, max_p), base_code in tabela_313[pavimento_upper].items():
                if min_p <= profundidade_float <= max_p:
                    codigo_base_313 = base_code
                    break
            
            if codigo_base_313 is None and profundidade_float > max(k[1] for k in tabela_313[pavimento_upper].keys()):
                codigo_base_313 = list(tabela_313[pavimento_upper].values())[-1]

            if codigo_base_313 is None:
                output_final.append(f"{codigo};ERRO: Profundidade fora da faixa para o código 313. (Prof: {profundidade})")
                continue
            
            output_final.append(f"{codigo_base_313} - 1 UNIDADE")

        elif codigo == '320':
            if not all([diametro, pavimento, profundidade]):
                output_final.append(f"{codigo};ERRO: Dados de Diâmetro, Pavimento ou Profundidade incompletos para o código 320. (Diam: {diametro}, Pav: {pavimento}, Prof: {profundidade})")
                continue
            
            try:
                diametro_int = int(diametro)
                profundidade_float = float(profundidade.replace(',', '.'))
            except ValueError:
                output_final.append(f"{codigo};ERRO: Diâmetro ou Profundidade inválidos para o código 320. (Diam: {diametro}, Prof: {profundidade})")
                continue

            pavimento_upper = (pavimento or '').upper()

            tabela_320 = {
                'REVESTIDO': {
                    'diametros_base': { (0, 100): '3900', (101, 150): '3901', (151, 200): '3902', (201, 300): '3903' },
                    'profundidades_excedente': { (0.0, 1.0): '3910', (1.0, 2.0): '3911', (2.0, 5.0): '3912' },
                    'prof_excedente_code': '3911'
                },
                'SEM REVESTIMENTO': {
                    'diametros_base': { (0, 100): '3920', (101, 150): '3921', (151, 200): '3922', (201, 300): '3923' },
                    'profundidades_excedente': { (0.0, 1.0): '3930', (1.0, 2.0): '3931', (2.0, 5.0): '3932' },
                    'prof_excedente_code': '3931'
                }
            }

            if pavimento_upper not in tabela_320:
                output_final.append(f"{codigo};ERRO: Pavimento inválido para o código 320. (Pav: {pavimento})")
                continue

            config_320 = tabela_320[pavimento_upper]
            
            codigo_base_diametro = None
            for (min_d, max_d), base_code in config_320['diametros_base'].items():
                if min_d <= diametro_int <= max_d:
                    codigo_base_diametro = base_code
                    break
            
            if codigo_base_diametro is None:
                output_final.append(f"{codigo};ERRO: Diâmetro fora da faixa para o código 320. (Diam: {diametro})")
                continue
            
            output_final.append(f"{codigo_base_diametro} - 1 UNIDADE")

            codigo_prof_base = None
            for (min_p, max_p), prof_code in config_320['profundidades_excedente'].items():
                if min_p <= profundidade_float <= max_p:
                    codigo_prof_base = prof_code
                    break

            if codigo_prof_base is None and profundidade_float > max(k[1] for k in config_320['profundidades_excedente'].keys()):
                codigo_prof_base = list(config_320['profundidades_excedente'].values())[-1]
            
            if codigo_prof_base is None:
                output_final.append(f"{codigo};ERRO: Profundidade fora da faixa para o código 320. (Prof: {profundidade})")
                continue
            
            # Aqui vamos adicionar o código de profundidade, que pode ser o base ou o excedente
            # A unidade base de profundidade para o código 320 é de 1.0 metro.
            # Se a profundidade for maior que 1.0, cada metro excedente tem um código.

            if profundidade_float <= 1.0: # Se a profundidade for até 1.0 metro
                output_final.append(f"{codigo_prof_base} - {profundidade.replace('.', ',')} METROS")
            else: # Se a profundidade for maior que 1.0 metro
                # A primeira unidade é coberta pelo código base de profundidade (o que a profundidade_float se encaixa na faixa)
                # O excedente é profundidade_float - 1.0
                excedente_profundidade = profundidade_float - 1.0
                codigo_excedente_prof = config_320['prof_excedente_code']
                
                output_final.append(f"{codigo_prof_base} - 1,00 METRO") # Código para o primeiro metro
                output_final.append(f"{codigo_excedente_prof} - {f'{excedente_profundidade:.2f}'.replace('.', ',')} METROS")
        
        elif codigo == '321':
            if not all([pavimento, troca, profundidade, mts_tubo_batido]):
                output_final.append(f"{codigo};ERRO: Dados de Pavimento, Troca, Profundidade ou MTS de Tubo Batido incompletos para o código 321. (Pav: {pavimento}, Troca: {troca}, Prof: {profundidade}, MTS: {mts_tubo_batido})")
                continue
            
            try:
                profundidade_float = float(profundidade.replace(',', '.'))
                mts_tubo_batido_float = float(mts_tubo_batido.replace(',', '.'))
            except ValueError:
                output_final.append(f"{codigo};ERRO: Profundidade ou MTS de Tubo Batido inválidos para o código 321. (Prof: {profundidade}, MTS Tubo: {mts_tubo_batido})")
                continue

            pavimento_upper = (pavimento or '').upper()
            troca_upper = (troca or '').upper()

            tabela_321 = {
                'PISTA COM PAVIMENTO': {
                    'SEM TROCA': { 'profundidades_base': { (0.0, 1.25): '4000', (1.25, 2.00): '4001', (2.00, 3.00): '4002', (3.00, 5.00): '4003' }, 'codigo_excedente_mts': '4001' },
                    'TROCA PARCIAL': { 'profundidades_base': { (0.0, 1.25): '4020', (1.25, 2.00): '4021', (2.00, 3.00): '4022', (3.00, 5.00): '4023' }, 'codigo_excedente_mts': '4021' },
                    'TROCA TOTAL': { 'profundidades_base': { (0.0, 1.25): '4040', (1.25, 2.00): '4041', (2.00, 3.00): '4042', (3.00, 5.00): '4043' }, 'codigo_excedente_mts': '4041' }
                },
                'PASSEIO REVESTIDO': {
                    'SEM TROCA': { 'profundidades_base': { (0.0, 1.25): '4004', (1.25, 2.00): '4005', (2.00, 3.00): '4006', (3.00, 5.00): '4007' }, 'codigo_excedente_mts': '4005' },
                    'TROCA PARCIAL': { 'profundidades_base': { (0.0, 1.25): '4024', (1.25, 2.00): '4025', (2.00, 3.00): '4026', (3.00, 5.00): '4027' }, 'codigo_excedente_mts': '4025' },
                    'TROCA TOTAL': { 'profundidades_base': { (0.0, 1.25): '4044', (1.25, 2.00): '4045', (2.00, 3.00): '4046', (3.00, 5.00): '4047' }, 'codigo_excedente_mts': '4045' }
                },
                'SEM PAVIMENTO': {
                    'SEM TROCA': { 'profundidades_base': { (0.0, 1.25): '4008', (1.25, 2.00): '4009', (2.00, 3.00): '4010', (3.00, 5.00): '4011' }, 'codigo_excedente_mts': '4009' },
                    'TROCA PARCIAL': { 'profundidades_base': { (0.0, 1.25): '4028', (1.25, 2.00): '4029', (2.00, 3.00): '4030', (3.00, 5.00): '4031' }, 'codigo_excedente_mts': '4029' },
                    'TROCA TOTAL': { 'profundidades_base': { (0.0, 1.25): '4048', (1.25, 2.00): '4049', (2.00, 3.00): '4050', (3.00, 5.00): '4051' }, 'codigo_excedente_mts': '4049' }
                }
            }
            if pavimento_upper not in tabela_321 or troca_upper not in tabela_321[pavimento_upper]:
                 output_final.append(f"{codigo};ERRO: Dados de Pavimento ou Troca inválidos para o código 321. (Pav: {pavimento}, Troca: {troca})")
                 continue
            
            config_321 = tabela_321[pavimento_upper][troca_upper]
            codigo_base_321 = None
            for (min_p, max_p), base_code in config_321['profundidades_base'].items():
                if min_p <= profundidade_float <= max_p:
                    codigo_base_321 = base_code
                    break
            
            if codigo_base_321 is None and profundidade_float > max(k[1] for k in config_321['profundidades_base'].keys()):
                codigo_base_321 = list(config_321['profundidades_base'].values())[-1]

            if codigo_base_321 is None:
                output_final.append(f"{codigo};ERRO: Profundidade fora da faixa para o código 321. (Prof: {profundidade})")
                continue
            
            output_final.append(f"{codigo_base_321} - 1 UNIDADE") # Adiciona o código base da profundidade

            # Verifica e adiciona o código de excedente para MTS de Tubo Batido (similar ao 319)
            codigo_excedente_mts_321 = config_321.get('codigo_excedente_mts')
            
            if mts_tubo_batido_float > 2.0 and codigo_excedente_mts_321:
                excedente_mts = mts_tubo_batido_float - 2.0
                excedente_mts_formatado = f"{excedente_mts:.2f}".replace('.', ',')
                output_final.append(f"{codigo_excedente_mts_321} - {excedente_mts_formatado} METROS")

        elif codigo == '343':
            if not all([diametro, pavimento, profundidade]):
                output_final.append(f"{codigo};ERRO: Dados de Diâmetro, Pavimento ou Profundidade incompletos para o código 343. (Diam: {diametro}, Pav: {pavimento}, Prof: {profundidade})")
                continue
            
            try:
                diametro_int = int(diametro)
                profundidade_float = float(profundidade.replace(',', '.'))
            except ValueError:
                output_final.append(f"{codigo};ERRO: Diâmetro ou Profundidade inválidos para o código 343. (Diam: {diametro}, Prof: {profundidade})")
                continue

            pavimento_upper = (pavimento or '').upper()

            tabela_343 = {
                'REVESTIDO': {
                    'diametros_base': { (0, 100): '4200', (101, 150): '4201', (151, 200): '4202', (201, 300): '4203' },
                    'profundidades_excedente': { (0.0, 1.0): '4210', (1.0, 2.0): '4211', (2.0, 5.0): '4212' },
                    'prof_excedente_code': '4211'
                },
                'SEM REVESTIMENTO': {
                    'diametros_base': { (0, 100): '4220', (101, 150): '4221', (151, 200): '4222', (201, 300): '4223' },
                    'profundidades_excedente': { (0.0, 1.0): '4230', (1.0, 2.0): '4231', (2.0, 5.0): '4232' },
                    'prof_excedente_code': '4231'
                }
            }
            if pavimento_upper not in tabela_343:
                output_final.append(f"{codigo};ERRO: Pavimento inválido para o código 343. (Pav: {pavimento})")
                continue
            
            config_343 = tabela_343[pavimento_upper]
            
            codigo_base_diametro = None
            for (min_d, max_d), base_code in config_343['diametros_base'].items():
                if min_d <= diametro_int <= max_d:
                    codigo_base_diametro = base_code
                    break
            
            if codigo_base_diametro is None:
                output_final.append(f"{codigo};ERRO: Diâmetro fora da faixa para o código 343. (Diam: {diametro})")
                continue
            
            output_final.append(f"{codigo_base_diametro} - 1 UNIDADE")

            codigo_prof_base = None
            for (min_p, max_p), prof_code in config_343['profundidades_excedente'].items():
                if min_p <= profundidade_float <= max_p:
                    codigo_prof_base = prof_code
                    break
            
            if codigo_prof_base is None and profundidade_float > max(k[1] for k in config_343['profundidades_excedente'].keys()):
                codigo_prof_base = list(config_343['profundidades_excedente'].values())[-1]

            if codigo_prof_base is None:
                output_final.append(f"{codigo};ERRO: Profundidade fora da faixa para o código 343. (Prof: {profundidade})")
                continue
            
            if profundidade_float <= 1.0:
                output_final.append(f"{codigo_prof_base} - {profundidade.replace('.', ',')} METROS")
            else:
                excedente_profundidade = profundidade_float - 1.0
                codigo_excedente_prof = config_343['prof_excedente_code']
                
                output_final.append(f"{codigo_prof_base} - 1,00 METRO")
                output_final.append(f"{codigo_excedente_prof} - {f'{excedente_profundidade:.2f}'.replace('.', ',')} METROS")

        else:
            # Para códigos que não exigem lógica específica, apenas retorna o código
            output_final.append(f"{codigo} - Código processado (sem extras ou lógica específica).")

    return output_final