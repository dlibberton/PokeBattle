import React, { useState, useEffect } from 'react';
import { useOutletContext } from 'react-router-dom';
import { GenerateGame, updateUserDeck } from '../utilities';
import { Card, Button } from 'react-bootstrap';

const ShopPage = () => {
	const { user } = useOutletContext();
	const [gameData, setGameData] = useState(null);
	const [randomPokemon, setRandomPokemon] = useState([]);
	const [userDeck, setUserDeck] = useState([]);
	const [deckPokemon, setDeckPokemon] = useState([]);

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
			setDeckPokemon([...deckPokemon, pokemon]);
			updateUserDeck(userID, pokemon.id);
		}
	};

	if (!gameData) {
		return <div>Loading...</div>;
	}
	return (
		<div>
			{/* Weather card */}
			<Card style={{ width: '18rem', margin: '15px' }}>
				<Card.Body>
					<Card.Title>Weather Information</Card.Title>
					<Card.Text>Location: {gameData.weather.location}</Card.Text>
					<Card.Text>
						Weather Conditions: {gameData.weather.weather_conditions}
					</Card.Text>
					<Card.Img
						variant="bottom"
						src={`https://example.com/weather_images/${gameData.weather.weather_conditions}.png`}
						alt={gameData.weather.weather_conditions}
					/>
				</Card.Body>
			</Card>

			{/*Pokemon Card*/}
			<div className="row">
				{randomPokemon.map((pokemon, index) => (
					<div key={index} className="col-md-4 mb-4">
						<Card
							border={deckPokemon.includes(pokemon) ? 'success' : 'primary'}
							style={{ marginBottom: '15px' }}
						>
							<Card.Img
								variant="top"
								src={
									deckPokemon.includes(pokemon)
										? `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/${pokemon.id}.gif`
										: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.id}.png`
								}
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
