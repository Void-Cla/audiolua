// Seleciona o campo de conteúdo
const content = document.querySelector('.content');

// Configuração de reconhecimento de fala
const ReconhecimentoFala = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!ReconhecimentoFala) {
    content.textContent = 'Desculpe, seu navegador não suporta reconhecimento de fala.';
} else {
    const reconhecimento = new ReconhecimentoFala();

    // Função para falar texto usando a síntese de voz
    function falar(texto) {
        const texto_falar = new SpeechSynthesisUtterance(texto);
        
        // Para o reconhecimento enquanto fala
        reconhecimento.stop();

        texto_falar.onend = () => {
            console.log('Fala concluída.');
            reconhecimento.start();  // Reinicia o reconhecimento após a fala
        };

        // Inicia a fala
        window.speechSynthesis.speak(texto_falar);
    }

    // Inicia o reconhecimento de fala quando a página carrega
    window.addEventListener('load', () => {
        content.textContent = "Ouvindo...";
        reconhecimento.start();  // Inicia o reconhecimento de fala
    });

    // Quando o reconhecimento de fala retorna um resultado
    reconhecimento.onresult = async (evento) => {
        const transcricao = evento.results[0][0].transcript;
        content.textContent = `Você disse: ${transcricao}`;

        // Envia a transcrição para o Flask e recebe a resposta
        try {
            const resposta = await consultarLua(transcricao);
            if (resposta) {
                falar(resposta);  // Fala a resposta recebida
                content.textContent = `Resposta: ${resposta}`;
            }
        } catch (erro) {
            console.error('Erro ao consultar a Lua:', erro);
            content.textContent = 'Erro ao consultar a Lua.';
        }
    };

    // Função para enviar a transcrição ao Flask e receber a resposta
    async function consultarLua(query) {
        const resposta = await fetch('/consultar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        if (!resposta.ok) {
            throw new Error(`Erro HTTP: ${resposta.status}`);
        }

        const dados = await resposta.json();
        return dados.resposta || 'Desculpe, não consegui encontrar uma resposta.';
    };

    // Reinicia o reconhecimento ao finalizar
    reconhecimento.onend = () => {
        console.log('Reconhecimento de fala finalizado.');
        reconhecimento.start();  // Reinicia automaticamente
    };
}
