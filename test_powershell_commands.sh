#!/bin/bash
# Test de comandos PowerShell extraídos del BAT

echo "═══════════════════════════════════════════════════════════════"
echo "🧪 PRUEBA DE COMANDOS POWERSHELL"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Extraer un comando PowerShell de ejemplo del BAT
COMANDO=$(grep -m 1 'powershell -Command' InstaladorUnico_SistemaGestionCasos.bat)

echo "📋 Comando extraído:"
echo "$COMANDO"
echo ""

# Verificar que las comillas estén escapadas
if echo "$COMANDO" | grep -q '\\"'; then
    echo "✅ Comillas correctamente escapadas con \\\""
else
    echo "❌ Comillas NO están escapadas"
fi

# Contar comillas escapadas
ESCAPED_QUOTES=$(echo "$COMANDO" | grep -o '\\"' | wc -l)
echo "✅ Encontradas $ESCAPED_QUOTES comillas escapadas"

# Verificar estructura del comando
if echo "$COMANDO" | grep -q 'FromBase64String'; then
    echo "✅ Comando contiene FromBase64String"
fi

if echo "$COMANDO" | grep -q 'WriteAllBytes'; then
    echo "✅ Comando contiene WriteAllBytes"
fi

if echo "$COMANDO" | grep -q 'Get-Content'; then
    echo "✅ Comando contiene Get-Content"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📊 ANÁLISIS COMPLETO"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Contar todos los comandos PowerShell
TOTAL_CMDS=$(grep -c 'powershell -Command' InstaladorUnico_SistemaGestionCasos.bat)
echo "✅ Total de comandos PowerShell: $TOTAL_CMDS"

# Contar comandos con comillas escapadas
CMDS_WITH_ESCAPED=$(grep 'powershell -Command' InstaladorUnico_SistemaGestionCasos.bat | grep -c '\\"')
echo "✅ Comandos con comillas escapadas: $CMDS_WITH_ESCAPED"

# Verificar que todos los comandos de Base64 tengan comillas escapadas
BASE64_CMDS=$(grep 'powershell -Command.*FromBase64String' InstaladorUnico_SistemaGestionCasos.bat | wc -l)
BASE64_ESCAPED=$(grep 'powershell -Command.*FromBase64String.*\\"' InstaladorUnico_SistemaGestionCasos.bat | wc -l)

echo "✅ Comandos Base64: $BASE64_CMDS"
echo "✅ Comandos Base64 con escape: $BASE64_ESCAPED"

if [ "$BASE64_CMDS" -eq "$BASE64_ESCAPED" ]; then
    echo ""
    echo "🎉 ¡TODOS LOS COMANDOS BASE64 TIENEN COMILLAS ESCAPADAS!"
else
    echo ""
    echo "⚠️  Algunos comandos Base64 podrían tener problemas"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ VERIFICACIÓN COMPLETADA"
echo "═══════════════════════════════════════════════════════════════"
