export const baseURL = 'http://127.0.0.1:8000';

export const user = $state({ value: null });

export const selectedBookId = $state({ value: null });

export const ttsSpeed = $state({ value: 1.0 });

let _selectedLanguage = $state(null);

// Guard against server-side rendering (Node has no sessionStorage). If we're in a browser, sessionStorage exists; otherwise we skip.
if (typeof sessionStorage !== 'undefined') {
	const stored = sessionStorage.getItem('selectedLanguage');
	if (stored) _selectedLanguage = stored;
}

export const selectedLanguage = {
	get value() {
		return _selectedLanguage;
	},
	set value(v) {
		_selectedLanguage = v;
		if (typeof sessionStorage !== 'undefined') {
			if (v) {
				sessionStorage.setItem('selectedLanguage', v);
			} else {
				sessionStorage.removeItem('selectedLanguage');
			}
		}
	}
};
