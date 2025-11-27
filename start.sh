#!/bin/bash
# ============================================
#  Mini Terminal - Inicializador Linux
# ============================================

echo ""
echo "========================================"
echo "  MINI TERMINAL - PAINEL DE CONTROLE"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não está instalado"
    echo ""
    echo "Instale com: sudo apt-get install python3"
    echo ""
    exit 1
fi

echo "[OK] Python detectado"
python3 --version
echo ""

# Verificar Tkinter
if ! python3 -m tkinter &> /dev/null; then
    echo "[AVISO] Tkinter não está disponível"
    echo "Instale com: sudo apt-get install python3-tk"
    echo ""
    echo "Tentando executar mesmo assim..."
    echo ""
else
    echo "[OK] Tkinter disponível"
    echo ""
fi

# Perguntar modo de execução
echo "Como deseja executar?"
echo ""
echo "[1] Interface Gráfica (GUI) - Recomendado"
echo "[2] Modo Terminal (linha de comando)"
echo "[3] GUI com sudo (privilégios root)"
echo ""
read -p "Escolha (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Iniciando interface gráfica..."
        python3 main.py
        ;;
    2)
        echo ""
        echo "Iniciando modo terminal..."
        python3 main.py --terminal
        ;;
    3)
        echo ""
        echo "Solicitando privilégios sudo..."
        sudo python3 main.py
        ;;
    *)
        echo ""
        echo "Opção inválida! Executando GUI padrão..."
        python3 main.py
        ;;
esac

echo ""
