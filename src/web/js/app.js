/**
 * JavaScript application logic for German training database management
 */

// Global variables
let bridge = null;
let currentEditingWord = null;

/**
 * Initialize the application when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function () {
    // Initialize Qt WebChannel
    new QWebChannel(qt.webChannelTransport, function (channel) {
        bridge = channel.objects.bridge;

        // Connect to signals
        bridge.dataUpdated.connect(function (jsonData) {
            const data = JSON.parse(jsonData);
            refreshUI(data);
        });

        bridge.errorOccurred.connect(function (errorMsg) {
            showAlert(errorMsg, 'error');
        });

        // Load initial data
        loadData();
    });
});

/**
 * Load all data from the database
 */
function loadData() {
    if (!bridge) {
        setTimeout(loadData, 100);
        return;
    }

    bridge.get_all_data(function (jsonData) {
        const data = JSON.parse(jsonData);
        if (data.error) {
            showAlert(data.error, 'error');
        } else {
            refreshUI(data);
        }
    });
}

/**
 * Refresh the UI with new data
 */
function refreshUI(data) {
    renderCharactersList(data.comparacao_de_frases_caracteres_descartados || []);
    renderPhrasesTable(data.frases_para_pronuncia_com_palavra_de_referencia || {});
}

/**
 * Render the list of discarded characters
 */
function renderCharactersList(characters) {
    const container = document.getElementById('charactersList');

    if (characters.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 1rem;">Nenhum caractere cadastrado.</p>';
        return;
    }

    const html = characters.map(char => `
        <div class="list-item">
            <span><strong>${escapeHtml(char)}</strong></span>
            <button class="btn btn-danger" onclick="removeCharacter('${escapeHtml(char)}')">Remover</button>
        </div>
    `).join('');

    container.innerHTML = html;
}

/**
 * Render the table of phrases
 */
function renderPhrasesTable(phrases) {
    const container = document.getElementById('phrasesTable');
    const entries = Object.entries(phrases);

    if (entries.length === 0) {
        container.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 1rem;">Nenhuma frase cadastrada.</p>';
        return;
    }

    const html = `
        <table>
            <thead>
                <tr>
                    <th>Palavra de Referência</th>
                    <th>Frase</th>
                    <th>Transcrição IPA</th>
                    <th style="width: 180px;">Ações</th>
                </tr>
            </thead>
            <tbody>
                ${entries.map(([palavra, data]) => `
                    <tr>
                        <td><strong>${escapeHtml(palavra)}</strong></td>
                        <td>${escapeHtml(data.frase)}</td>
                        <td style="font-family: 'Arial Unicode MS', sans-serif;">${escapeHtml(data.transcricao_ipa)}</td>
                        <td>
                            <button class="btn btn-primary" style="font-size: 0.75rem; padding: 0.4rem 0.8rem;" onclick="editPhrase('${escapeHtml(palavra)}')">Editar</button>
                            <button class="btn btn-danger" style="font-size: 0.75rem; padding: 0.4rem 0.8rem;" onclick="deletePhrase('${escapeHtml(palavra)}')">Excluir</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    container.innerHTML = html;
}

/**
 * Add a new character to the discarded list
 */
function addCharacter() {
    const input = document.getElementById('newCharacter');
    const char = input.value.trim();

    if (!char) {
        showAlert('Por favor, digite um caractere.', 'warning');
        return;
    }

    bridge.add_character(char, function (success) {
        if (success) {
            input.value = '';
            showAlert('Caractere adicionado com sucesso!', 'success');
        }
    });
}

/**
 * Remove a character from the discarded list
 */
function removeCharacter(char) {
    if (!confirm(`Deseja realmente remover o caractere "${char}"?`)) {
        return;
    }

    bridge.remove_character(char, function (success) {
        if (success) {
            showAlert('Caractere removido com sucesso!', 'success');
        }
    });
}

/**
 * Save phrase from form (add or update)
 */
function savePhraseForm(event) {
    event.preventDefault();

    const palavra = document.getElementById('palavraReferencia').value.trim();
    const frase = document.getElementById('frase').value.trim();
    const ipa = document.getElementById('transcricaoIpa').value.trim();

    if (!palavra || !frase || !ipa) {
        showAlert('Por favor, preencha todos os campos.', 'warning');
        return;
    }

    if (currentEditingWord) {
        // Update existing phrase
        bridge.update_phrase(currentEditingWord, frase, ipa, function (success) {
            if (success) {
                showAlert('Frase atualizada com sucesso!', 'success');
                cancelEdit();
            }
        });
    } else {
        // Add new phrase
        bridge.add_phrase(palavra, frase, ipa, function (success) {
            if (success) {
                showAlert('Frase adicionada com sucesso!', 'success');
                document.getElementById('phraseForm').reset();
            }
        });
    }
}

/**
 * Edit an existing phrase
 */
function editPhrase(palavra) {
    bridge.get_all_data(function (jsonData) {
        const data = JSON.parse(jsonData);
        const phrase = data.frases_para_pronuncia_com_palavra_de_referencia[palavra];

        if (phrase) {
            currentEditingWord = palavra;
            document.getElementById('palavraReferencia').value = palavra;
            document.getElementById('palavraReferencia').disabled = true;
            document.getElementById('frase').value = phrase.frase;
            document.getElementById('transcricaoIpa').value = phrase.transcricao_ipa;

            document.getElementById('formTitle').textContent = 'Editar Frase';
            document.getElementById('saveBtn').textContent = 'Atualizar';
            document.getElementById('cancelBtn').style.display = 'inline-flex';

            // Scroll to form
            document.getElementById('phraseForm').scrollIntoView({ behavior: 'smooth' });
        }
    });
}

/**
 * Delete a phrase
 */
function deletePhrase(palavra) {
    if (!confirm(`Deseja realmente excluir a frase com palavra de referência "${palavra}"?`)) {
        return;
    }

    bridge.delete_phrase(palavra, function (success) {
        if (success) {
            showAlert('Frase excluída com sucesso!', 'success');
            if (currentEditingWord === palavra) {
                cancelEdit();
            }
        }
    });
}

/**
 * Cancel edit mode
 */
function cancelEdit() {
    currentEditingWord = null;
    document.getElementById('phraseForm').reset();
    document.getElementById('palavraReferencia').disabled = false;
    document.getElementById('formTitle').textContent = 'Adicionar Nova Frase';
    document.getElementById('saveBtn').textContent = 'Salvar';
    document.getElementById('cancelBtn').style.display = 'none';
}

/**
 * Show alert message
 */
function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    const alertClass = type === 'error' ? 'alert-error' : type === 'warning' ? 'alert-warning' : 'alert-success';

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} fade-in`;
    alertDiv.textContent = message;

    container.appendChild(alertDiv);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 300);
    }, 5000);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
