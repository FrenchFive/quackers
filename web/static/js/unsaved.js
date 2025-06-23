document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.card');
  cards.forEach(card => {
    const saveButton = card.querySelector('button.button');
    if (!saveButton) return;

    const inputs = card.querySelectorAll('input, select, textarea');
    const initialState = new Map();

    inputs.forEach(el => {
      initialState.set(el, getValue(el));
      el.addEventListener('input', updateState);
      el.addEventListener('change', updateState);
    });

    function getValue(el) {
      if (el.type === 'checkbox' || el.type === 'radio') {
        return el.checked;
      }
      return el.value;
    }

    function updateState() {
      let changed = false;
      inputs.forEach(el => {
        if (getValue(el) !== initialState.get(el)) {
          changed = true;
        }
      });
      if (changed) {
        saveButton.classList.add('unsaved');
      } else {
        saveButton.classList.remove('unsaved');
      }
    }

    saveButton.updateInitial = function() {
      inputs.forEach(el => initialState.set(el, getValue(el)));
      saveButton.classList.remove('unsaved');
    };
  });

  window.addEventListener('beforeunload', function(e) {
    if (document.querySelector('.unsaved')) {
      e.preventDefault();
      e.returnValue = '';
    }
  });
});

