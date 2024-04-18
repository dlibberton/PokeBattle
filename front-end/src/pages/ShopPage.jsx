import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { GenerateGame, updateUserDeck } from '../utilities';
import { Card, Button } from 'react-bootstrap';

const ShopPage = () => {
	const { user } = useOutletContext();
	const [gameData, setGameData] = useState(null);
	const [randomPokemon, setRandomPokemon] = useState([]);
	const [userDeck, setUserDeck] = useState([]);

	useEffect(() => {
		// Call the fetchGameData function when the component mounts
		const fetchData = async () => {
			try {
				const data = await GenerateGame();
				setGameData(data); // Store the fetched data in state
			} catch (error) {
				console.error('Error fetching game data:', error);
			}
		};

		fetchData();
	}, []);

	const getRandomNumber = (min, max) => {
		return Math.floor(Math.random() * (max - min + 1)) + min;
	};

	//random Pokémon from available Pokémon data
	useEffect(() => {
		if (gameData && gameData.available_pokemon) {
			const randomPokemonArray = [];
			for (let i = 0; i < 7; i++) {
				const randomIndex = getRandomNumber(
					0,
					gameData.available_pokemon.length - 1
				);
				randomPokemonArray.push(gameData.available_pokemon[randomIndex]);
			}
			setRandomPokemon(randomPokemonArray);
		}
	}, [gameData]);

	const addToDeck = (userID, pokemon) => {
		if (userDeck.length < 3) {
			const updatedDeck = [...userDeck, pokemon];
			setUserDeck(updatedDeck);
			updateUserDeck(userID, pokemon.id);
		}
	};

	if (!gameData) {
		return <div>Loading...</div>;
	}
	return (
		<div>
			<div className="row">
				{randomPokemon.map((pokemon, index) => (
					<div key={index} className="col-md-4 mb-4">
						<Card>
							<Card.Img
								variant="top"
								src={`path_to_your_pokemon_images/${pokemon.name}.png`}
								alt={pokemon.name}
							/>
							<Card.Body>
								<Card.Title>{pokemon.name}</Card.Title>
								<Card.Text>
									Attack: {pokemon.attack}, Defense: {pokemon.defense}, Type:{' '}
									{pokemon.type}
								</Card.Text>
								<Button
									variant="primary"
									onClick={() => addToDeck(gameData.user_id, pokemon)}
									disabled={userDeck.length >= 3 || userDeck.includes(pokemon)}
								>
									{userDeck.includes(pokemon) ? 'Added to Deck' : 'Add to Deck'}
								</Button>
							</Card.Body>
						</Card>
					</div>
				))}
			</div>
		</div>
	);
};
export default ShopPage;