export const baseURL = import.meta.env.PROD
	? 'https://api.readablock.com'
	: 'http://127.0.0.1:8000';

export const user = $state({ value: null });

export const selectedBookId = $state({ value: null });

export const ttsSpeed = $state({ value: 1.0 });

let _lastReadBookId = $state(null);

if (typeof sessionStorage !== 'undefined') {
	const stored = sessionStorage.getItem('lastReadBookId');
	if (stored) _lastReadBookId = Number(stored);
}

export const lastReadBookId = {
	get value() {
		return _lastReadBookId;
	},
	set value(v) {
		_lastReadBookId = v;
		if (typeof sessionStorage !== 'undefined') {
			if (v != null) {
				sessionStorage.setItem('lastReadBookId', String(v));
			} else {
				sessionStorage.removeItem('lastReadBookId');
			}
		}
	}
};

let _selectedLanguage = $state(null);

// Guard against server-side rendering (Node has no localStorage). If we're in a browser, localStorage exists; otherwise we skip.
if (typeof localStorage !== 'undefined') {
	const stored = localStorage.getItem('selectedLanguage');
	if (stored) _selectedLanguage = stored;
}

export const selectedLanguage = {
	get value() {
		return _selectedLanguage;
	},
	set value(v) {
		_selectedLanguage = v;
		if (typeof localStorage !== 'undefined') {
			if (v) {
				localStorage.setItem('selectedLanguage', v);
			} else {
				localStorage.removeItem('selectedLanguage');
			}
		}
	}
};
