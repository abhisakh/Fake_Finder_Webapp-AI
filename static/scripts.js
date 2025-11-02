// --- State Management ---
let currentFacts = []; // Stores the facts and their truth status after generation
let fakeIndex = -1; // Stores the index of the fake statement in the currentFacts array
let selectedFactIndex = -1; // Stores the index of the fact the user has clicked

// --- DOM Elements ---
const configForm = document.getElementById('config-form');
const generateButton = document.getElementById('generate-button');
const loadingIndicator = document.getElementById('loading');
const gameArea = document.getElementById('game-area');
const factList = document.getElementById('fact-list');
const submitGuessButton = document.getElementById('submit-guess');
const feedbackModal = document.getElementById('feedback-modal');
const closeModalButton = document.getElementById('close-modal');
const feedbackTitle = document.getElementById('feedback-title');
const feedbackMessage = document.getElementById('feedback-message');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');

// --- Utility Functions ---

/**
 * Shows an error message in the UI.
 * @param {string} message
 */
function showError(message) {
    loadingIndicator.classList.add('hidden');
    gameArea.classList.add('hidden');
    configForm.classList.remove('hidden');
    errorMessage.classList.remove('hidden');
    errorText.textContent = message;
    generateButton.classList.remove('disabled');
}

/**
 * Displays the facts as clickable buttons.
 * @param {Array<Object>} facts - Array of fact objects {text, is_true}.
 */
function renderFacts(facts) {
    factList.innerHTML = ''; // Clear previous facts
    selectedFactIndex = -1; // Reset selection

    facts.forEach((fact, index) => {
        const li = document.createElement('li');
        const button = document.createElement('button');
        button.className = 'fact-button';
        button.textContent = fact.text;
        button.setAttribute('data-index', index);

        // --- Selection Logic ---
        button.addEventListener('click', (e) => {
            handleFactSelection(index, e.target);
        });

        li.appendChild(button);
        factList.appendChild(li);
    });

    submitGuessButton.classList.add('disabled');
}

/**
 * Handles the click event on a fact button, managing selection state.
 * @param {number} index - The index of the clicked fact.
 * @param {HTMLElement} clickedButton - The button element clicked.
 */
function handleFactSelection(index, clickedButton) {
    // Deselect any currently selected button
    const previouslySelected = factList.querySelector('.fact-button.selected');
    if (previouslySelected) {
        previouslySelected.classList.remove('selected');
    }

    // Select the new button
    clickedButton.classList.add('selected');
    selectedFactIndex = index;

    // Enable the submit button
    submitGuessButton.classList.remove('disabled');
}

/**
 * Handles the logic after a successful API call and rendering.
 * @param {Object} responseData - The data received from the /generate endpoint.
 */
function startGame(responseData) {
    errorMessage.classList.add('hidden');
    configForm.classList.add('hidden');
    loadingIndicator.classList.add('hidden');
    gameArea.classList.remove('hidden');

    document.getElementById('game-topic').textContent = responseData.topic;
    document.getElementById('game-level').textContent = responseData.level.toUpperCase();

    // Store global state
    currentFacts = responseData.facts;
    fakeIndex = responseData.fake_index;

    // Render and make facts clickable
    renderFacts(responseData.facts);
}

/**
 * Handles the submission of the user's guess.
 */
function handleSubmitGuess() {
    if (selectedFactIndex === -1 || submitGuessButton.classList.contains('disabled')) {
        return; // No guess made or button is disabled
    }

    // Disable all buttons after guess
    const buttons = factList.querySelectorAll('.fact-button');
    buttons.forEach(btn => btn.classList.add('disabled'));
    submitGuessButton.classList.add('disabled');

    // Check if the selected index matches the fake index
    const isCorrect = (selectedFactIndex === fakeIndex);
    const selectedButton = factList.querySelector(`[data-index="${selectedFactIndex}"]`);

    let title, message;

    if (isCorrect) {
        title = "🥳 Correct!";
        message = "You successfully identified the fake statement. Great work!";
        selectedButton.classList.add('correct-result');
    } else {
        title = "😔 Incorrect";
        // Highlight the user's wrong guess
        message = "That was a true statement. Better luck next time!";
        selectedButton.classList.add('wrong-result');

        // Highlight the correct fake statement
        const correctButton = factList.querySelector(`[data-index="${fakeIndex}"]`);
        if (correctButton) {
             correctButton.classList.add('correct-result');
        }
    }

    feedbackTitle.textContent = title;
    feedbackMessage.textContent = message;
    feedbackModal.classList.remove('hidden');
}


// --- Event Listeners ---

// 1. Handle Form Submission (Generate Facts)
configForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const topic = document.getElementById('topic').value.trim();
    const level = document.getElementById('level').value;

    if (!topic) return;

    // Reset UI and show loading
    generateButton.classList.add('disabled');
    errorMessage.classList.add('hidden');
    gameArea.classList.add('hidden');
    loadingIndicator.classList.remove('hidden');

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic, level }),
        });

        const data = await response.json();

        if (response.ok) {
            startGame(data);
        } else {
            showError(`Error generating facts: ${data.error || 'Unknown API error.'}`);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        showError('A network error occurred. Please check your server connection.');
    } finally {
        generateButton.classList.remove('disabled');
    }
});

// 2. Handle Guess Submission
submitGuessButton.addEventListener('click', handleSubmitGuess);

// 3. Handle Modal Closing (Play Again)
closeModalButton.addEventListener('click', () => {
    feedbackModal.classList.add('hidden');
    // Go back to the configuration form to start a new game
    gameArea.classList.add('hidden');
    configForm.classList.remove('hidden');
    // Ensure input fields are enabled for next game
    generateButton.classList.remove('disabled');
});
