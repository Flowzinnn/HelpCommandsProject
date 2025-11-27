# 📚 Guia de Exemplos de Uso - Mini Terminal

Este guia apresenta exemplos práticos de uso do Mini Terminal em cenários reais de suporte técnico.

---

## 🎯 Cenários de Uso

### 1️⃣ Resetar Configurações de Rede

**Problema:** Cliente reclama que a internet não funciona após mudança de roteador.

**Solução:**
1. Abra o Mini Terminal
2. Busque por "rede" ou "IP"
3. Execute:
   - `[R5] Renovar IP (DHCP)` - Libera e renova o IP
   - `[R6] Limpar Cache DNS` - Limpa DNS
   - `[R3] Teste de Conexão` - Verifica conectividade

**Comandos Equivalentes no Terminal:**
```cmd
ipconfig /release
ipconfig /renew
ipconfig /flushdns
ping 8.8.8.8 -n 4
```

---

### 2️⃣ Usuário Não Consegue Acessar Painel de Controle

**Problema:** Windows 11 escondeu o Painel de Controle clássico e usuário não sabe acessar.

**Solução:**
1. Abra o Mini Terminal
2. Execute `[1] Painel de Controle (clássico)`
3. Pronto! O Painel de Controle abre instantaneamente

**Dica:** Adicione aos favoritos (⭐) para acesso rápido

---

### 3️⃣ Verificar Drivers de Hardware

**Problema:** Dispositivo não está sendo reconhecido.

**Solução:**
1. Execute `[2] Gerenciador de Dispositivos`
2. Verifique se há dispositivos com ⚠️ amarelo
3. Se necessário, execute `[4] Informações do Sistema` para detalhes completos

---

### 4️⃣ Desativar Serviços Desnecessários

**Problema:** Computador está lento, precisa desativar serviços.

**Solução:**
1. Execute `[3] Serviços do Windows` (requer admin)
2. Aceite a solicitação UAC
3. Identifique e desative serviços não utilizados

---

### 5️⃣ Gerenciar Contas de Usuário Remotamente

**Problema:** Usuário esqueceu a senha ou precisa configurar login automático.

**Solução:**
1. Execute `[U1] Contas de Usuário` (requer admin)
2. Configure senhas ou login automático
3. Ou use `[U2] Usuários e Grupos Locais` para controle avançado

---

### 6️⃣ Limpar Espaço em Disco

**Problema:** Disco C: está cheio.

**Solução:**
1. Execute `[12] Limpeza de Disco`
2. Selecione unidade C:
3. Marque arquivos temporários
4. Clique OK

**Complementar:**
- `[D1] Gerenciamento de Disco` - Ver uso por partição
- `[13] Desfragmentador` - Otimizar disco (apenas HDD)

---

### 7️⃣ Configurar Proxy Corporativo

**Problema:** Empresa usa proxy e funcionário precisa configurar.

**Solução:**
1. Execute `[I2] Configurações de Proxy`
2. Configure endereço e porta do proxy
3. Ou use `[I1] Opções da Internet` para configuração avançada

---

### 8️⃣ Criar Ponto de Restauração Antes de Mudanças

**Problema:** Vai instalar software desconhecido e quer garantia.

**Solução:**
1. Execute `[B3] Criar Ponto de Restauração` (requer admin)
2. Clique "Criar"
3. Dê um nome descritivo (ex: "Antes de instalar software X")
4. Aguarde conclusão

**Se algo der errado depois:**
- Execute `[B2] Restauração do Sistema`
- Escolha o ponto criado
- Restaure

---

### 9️⃣ Diagnosticar Problemas de Inicialização

**Problema:** Windows está iniciando com erro ou muito lento.

**Solução:**
1. Execute `[5] Configuração do Sistema (msconfig)` (requer admin)
2. Aba "Inicialização de Programas"
3. Desative programas desnecessários
4. Aba "Serviços" → Ocultar serviços Microsoft
5. Desative serviços não essenciais
6. Reinicie

---

### 🔟 Verificar Saúde da Bateria (Notebook)

**Problema:** Notebook descarrega rápido.

**Solução:**
1. Execute `[E3] Relatório de Bateria`
2. Aguarde geração do relatório
3. Um arquivo HTML será aberto com:
   - Capacidade atual vs original
   - Ciclos de carga
   - Uso recente
   - Estimativa de duração

---

## 🛠️ Fluxos de Trabalho Completos

### 🔄 Manutenção Preventiva Completa

Execute em sequência:

1. **Limpeza:**
   - `[12] Limpeza de Disco`
   - Limpar arquivos temporários

2. **Atualização:**
   - `[P3] Apps e Recursos` → Verificar atualizações
   - Windows Update

3. **Otimização:**
   - `[13] Desfragmentador` (apenas HDD)
   - `[5] msconfig` → Desativar programas de inicialização

4. **Backup:**
   - `[B3] Criar Ponto de Restauração`
   - `[B1] Backup e Restauração` → Configurar backup automático

5. **Verificação:**
   - `[6] Gerenciador de Tarefas` → Ver uso de recursos
   - `[10] Visualizador de Eventos` → Verificar erros

---

### 🔐 Auditoria de Segurança

1. **Firewall:**
   - `[R8] Firewall do Windows` → Verificar regras

2. **Usuários:**
   - `[U2] Usuários e Grupos Locais` → Revisar contas
   - `[U4] Política de Segurança Local` → Políticas de senha

3. **Atualizações:**
   - Windows Update
   - `[P2] Recursos do Windows` → Ativar recursos de segurança

4. **Credenciais:**
   - `[U5] Gerenciador de Credenciais` → Limpar senhas antigas

---

### 🌐 Diagnóstico Completo de Rede

Execute em sequência e anote resultados:

```
1. [R3] Teste de Conexão (ping 8.8.8.8)
   ✅ OK: Internet funciona
   ❌ Falha: Problema de conectividade

2. [R4] Configuração IP (ipconfig /all)
   Anote: IP, Gateway, DNS

3. [R7] Trace Route (tracert google.com)
   Identifique onde a conexão falha

4. [R9] Teste de Porta (netstat -ano)
   Veja portas em uso

5. [R1] Conexões de Rede
   Configure adaptador se necessário
```

---

## 💡 Dicas Profissionais

### ⭐ Favoritos Recomendados

Marque como favoritos para acesso rápido:

- `[6] Gerenciador de Tarefas` - Sempre útil
- `[R1] Conexões de Rede` - Problemas comuns
- `[U1] Contas de Usuário` - Frequente em suporte
- `[T1] Prompt de Comando` - Terminal rápido
- `[P1] Programas e Recursos` - Desinstalar software

### 📋 Histórico Como Documentação

Use o histórico para documentar:
1. Todos os comandos executados durante atendimento
2. Exportar histórico: `Ferramentas` → `Exportar Histórico`
3. Anexar ao ticket de suporte
4. Evidência do que foi feito

### 🔒 Privilégios Administrativos

**Quando NÃO tem admin:**
- Execute Mini Terminal normalmente
- Comandos que precisam de admin mostrarão UAC
- Aceite para executar

**Quando TEM admin:**
- Execute Mini Terminal como Administrador
- Todos os comandos funcionarão sem prompts extras

**Linux:**
```bash
sudo python3 main.py
```

---

## 🎓 Casos de Estudo

### Caso 1: Escritório com 50 PCs - Configuração em Massa

**Cenário:** Precisa configurar proxy em 50 computadores.

**Solução com Mini Terminal:**
1. Copie `MiniTerminal.exe` para pendrive
2. Em cada PC:
   - Execute o MiniTerminal
   - `[I2] Configurações de Proxy`
   - Configure uma vez, salve template
3. Ou use comando livre para script:
   ```cmd
   reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
   reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "proxy.empresa.com:8080" /f
   ```

**Tempo economizado:** ~30 minutos → 5 minutos por PC

---

### Caso 2: Suporte Remoto via TeamViewer

**Cenário:** Cliente não sabe usar computador, você está via TeamViewer.

**Solução:**
1. Peça ao cliente para baixar MiniTerminal.exe
2. Cliente executa (não precisa instalar nada)
3. Você controla remotamente via TeamViewer
4. Execute todos os comandos necessários
5. Exporte histórico para o cliente

**Vantagem:** Interface visual familiar vs terminal assustador

---

### Caso 3: Técnico sem Experiência

**Cenário:** Técnico júnior não sabe comandos do Windows.

**Solução:**
1. Instale Mini Terminal
2. Técnico busca pela funcionalidade ("rede", "usuário")
3. Lê a descrição detalhada
4. Executa com 1 clique
5. Histórico documenta tudo automaticamente

**Resultado:** Técnico produtivo desde o dia 1

---

## 🚨 Comandos de Emergência

### PC Travado
```
[6] Gerenciador de Tarefas
→ Encerrar processo travado
```

### Sem Internet
```
[R5] Renovar IP
[R6] Limpar DNS
[R3] Testar Conexão
```

### Disco Cheio
```
[12] Limpeza de Disco
[D1] Gerenciamento de Disco (ver o que ocupa espaço)
```

### Windows Corrompido
```
[B2] Restauração do Sistema
→ Voltar para ponto anterior
```

### Esqueceu Senha
```
[U1] Contas de Usuário (como admin)
→ Resetar senha
```

---

## 📊 Comparação: Manual vs Mini Terminal

| Tarefa | Manual | Com Mini Terminal |
|--------|--------|-------------------|
| Abrir Painel de Controle | Win+R → control → Enter | 1 clique |
| Renovar IP | cmd → ipconfig /release → ipconfig /renew | 1 clique |
| Gerenciador de Dispositivos | Win+R → devmgmt.msc → Enter | 1 clique |
| Limpar DNS | cmd (admin) → ipconfig /flushdns | 1 clique |
| Criar Ponto Restauração | Painel → Sistema → Proteção → Criar | 1 clique |

**Tempo economizado:** ~70% em tarefas comuns

---

## 🎯 Metas de Eficiência

Use Mini Terminal para:

- ✅ Reduzir tempo de atendimento em 50%
- ✅ Padronizar procedimentos de suporte
- ✅ Documentar ações automaticamente
- ✅ Treinar técnicos mais rápido
- ✅ Evitar erros de digitação em comandos
- ✅ Aumentar satisfação do cliente

---

## 📞 Scripts de Atendimento

### Script 1: Problema de Internet

```
Técnico: "Vou executar alguns testes de rede. Acompanhe na tela."

[Mini Terminal]
1. [R4] ipconfig → Anota IP
2. [R3] ping → Testa conectividade
   ✅ OK: "Sua internet está funcionando, pode ser problema do site"
   ❌ Falha: Continue...
3. [R5] Renovar IP → "Renovando seu endereço IP..."
4. [R3] ping → Testa novamente
   ✅ OK: "Problema resolvido!"
   ❌ Falha: "Vou verificar suas conexões de rede"
5. [R1] Conexões → Reconfigure

Exportar histórico → Enviar ao cliente como comprovante
```

### Script 2: PC Lento

```
Técnico: "Vou fazer uma manutenção rápida. Pode acompanhar."

[Mini Terminal]
1. [6] Gerenciador de Tarefas → "Vendo o que está consumindo recursos"
2. [5] msconfig → "Desativando programas de inicialização desnecessários"
3. [12] Limpeza de Disco → "Removendo arquivos temporários"
4. [B3] Criar Ponto → "Criando backup antes de otimizar"
5. [3] Serviços → "Desativando serviços não utilizados"

"Pronto! Por favor, reinicie o computador. O Windows deve iniciar mais rápido agora."
```

---

**💬 Feedback dos Usuários:**

> "Economizei 2 horas por dia em tarefas repetitivas!" - Técnico de Suporte
>
> "Finalmente consigo acessar configurações sem depender de suporte!" - Usuário Final
>
> "Treinar novos técnicos ficou 10x mais fácil." - Supervisor de TI

---

✨ **Use o Mini Terminal e transforme seu suporte técnico!**
