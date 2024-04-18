import React from 'react';
import { useOutletContext } from 'react-router-dom';
import { Button } from 'react-bootstrap';

const HomePage = () => {
	const { user } = useOutletContext();

	return (
		<div className="container mt-5">
			<h1 className="mb-4">Welcome to PokeBattle!{user && ` ${user}`}</h1>
			<p className="lead">
				PokeBattle is a tactical card game where users assemble their deck and
				modify their stats in order to take down increasingly strong bosses, do
				you have what it takes?
			</p>
			<div className="mt-4">
				<Button variant="primary" className="mr-3" href="/tutorial">
					Learn More
				</Button>
				<Button variant="success" href="/shop">
					Play!
				</Button>
			</div>
		</div>
	);
};

export default HomePage;
