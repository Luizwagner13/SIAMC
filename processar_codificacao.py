# processar_codificacao.py

def processar_codigos(lista_itens_adicionados):
    """
    Processa uma lista de dicionários contendo os dados dos códigos adicionados
    e retorna uma lista de strings formatadas para exibição.
    """
    output_final = []

    for item in lista_itens_adicionados:
        codigo_input = item.get('codigo')
        
        # --- Lógica para o código 313 ---
        if codigo_input == '313':
            pavimento_input = item.get('pavimento', '').strip().upper()
            try:
                # Substitui vírgula por ponto para garantir conversão correta para float
                profundidade_input = float(item.get('profundidade', '').replace(',', '.') or 0.0)
            except ValueError:
                # Em caso de erro na conversão (ex: texto inválido), usa 0.0
                profundidade_input = 0.0 

            codigo_gerado = None
            if pavimento_input == 'CIMENTO':
                if 0.0 <= profundidade_input <= 1.25:
                    codigo_gerado = '3078'
                elif 1.25 < profundidade_input <= 2.00:
                    codigo_gerado = '3412'
                elif 2.00 < profundidade_input <= 3.00:
                    codigo_gerado = '3413'
            elif pavimento_input == 'TERRA':
                if 0.0 <= profundidade_input <= 1.25:
                    codigo_gerado = '3075'
                elif 1.25 < profundidade_input <= 2.00:
                    codigo_gerado = '3409'
                elif 2.00 < profundidade_input <= 3.00:
                    codigo_gerado = '3410'
            
            if codigo_gerado:
                output_final.append(f'{codigo_gerado} - 1 unidade')
            else:
                # Mensagem de erro mais descritiva
                output_final.append(f'313 - Erro: Não foi possível determinar o código para Pavimento: {item.get("pavimento")}, Profundidade: {item.get("profundidade")}. Verifique os valores.')
        
        # --- Lógica para outros códigos (ainda não implementada) ---
        # Exemplo:
        # elif codigo_input == '319':
        #     # Implemente a lógica para o 319 aqui, usando item.get('pavimento'), item.get('troca'), etc.
        #     output_final.append(f'319 - Lógica a ser implementada com: Pavimento: {item.get("pavimento")}, Troca: {item.get("troca")}, Profundidade: {item.get("profundidade")}')
        
        # Para códigos ainda não processados com lógica específica
        else:
            output_final.append(f'{codigo_input} - Lógica de codificação pendente ou não encontrada.')
            
    return output_final

if __name__ == '__main__':
    # Bloco para testes manuais do script
    print("--- Testes para processar_codificacao.py ---")
    test_data = [
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '1.0', 'troca': '', 'diametro': ''},
        {'codigo': '313', 'pavimento': 'Terra', 'profundidade': '2.5', 'troca': '', 'diametro': ''},
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '1.25', 'troca': '', 'diametro': ''}, # Limite superior
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '1.26', 'troca': '', 'diametro': ''}, # Logo acima do limite
        {'codigo': '313', 'pavimento': 'Cimento', 'profundidade': '4.0', 'troca': '', 'diametro': ''}, # Fora do range
        {'codigo': '319', 'pavimento': 'ASFALTICO', 'profundidade': '0.8', 'troca': 'sem troca', 'diametro': ''},
        {'codigo': '320 (rec)', 'pavimento': 'ASFALTICO', 'profundidade': '0.8', 'troca': '', 'diametro': '600'},
    ]
    resultados = processar_codigos(test_data)
    for res in resultados:
        print(res)