import axios from 'axios';

export const api = axios.create({
	baseURL: 'http://127.0.0.1:8000/',
});

export const userLogIn = async (email, password) => {
	let response = await api.post('login/', {
		email: email,
		password: password,
	});
	if (response.status === 200) {
		let { user, token } = response.data;
		localStorage.setItem('token', token);
		api.defaults.headers.common['Authorization'] = `Token ${token}`;
		return user;
	}
	alert(JSON.stringify(response.data));
	return null;
};

export const userConfirmation = async () => {
	let token = localStorage.getItem('token');
	if (token) {
		api.defaults.headers.common['Authorization'] = `Token ${token}`;
		let response = await api.get('login/');
		if (response.status === 200) {
			return response.data.user;
		}
		delete api.defaults.headers.common['Authorization'];
	}
	return null;
};

export const userLogOut = async () => {
	let response = await api.post('login/users/logout/');
	if (response.status === 204) {
		localStorage.removeItem('token');
		delete api.defaults.headers.common['Authorization'];
		return null;
	}
	alert('Something went wrong and logout failed');
};

export const GenerateGame = async () => {
	try {
		const response = await api.get('game/shop');
		// Return the response data
		return response.data;
	} catch (error) {
		// Handle errors
		console.error('Error fetching game data:', error);
		throw error;
	}
};

export const updateUserDeck = async (userID, pokemonId) => {
	try {
		const requestData = {
			pokemon_id: pokemonId,
			user_id: userID,
			deck_id: 1,
		};
		const response = await api.put('game/shop/', requestData);
		if (response.status === 200) {
			console.log('Pokemon added to deck successfully');
		} else {
			console.error('Unexpected status code:', response.status);
		}
	} catch (error) {
		// Handle errors
		console.error('Error updating user deck:', error);
		throw error;
	}
};
