import React from 'react';
import { useOutletContext } from 'react-router-dom';
import { Container, Row, Col, Button } from 'react-bootstrap';

const TutorialPage = () => {
	const { user } = useOutletContext();
	return (
		<div className="container mt-5">
			<h1 className="mb-4">{user && ` ${user}`}</h1>
			<Container className="mt-5">
				<Row>
					<Col>
						<h2 className="mb-4">Embark on an Epic Pokémon Journey!</h2>
						<p className="lead">
							Are you ready to become a Pokémon Master? In this thrilling
							adventure, you'll assemble a team of mighty Pokémon to take on
							formidable bosses and conquer the toughest challenges!
						</p>
					</Col>
				</Row>
				<Row className="mt-4">
					<Col>
						<h3>Phase One: Choose Your Pokémon</h3>
						<p>
							It all begins in phase one, where you'll face the exciting task of
							selecting three Pokémon out of a pool of six. Your goal? To create
							the most powerful team imaginable! Each Pokémon brings unique
							strengths and abilities to the table, so choose wisely!
						</p>
					</Col>
				</Row>
				<Row className="mt-4">
					<Col>
						<h3>Phase Two: Battle in Ever-Changing Conditions</h3>
						<p>
							But the challenge doesn't end there! In phase two, the true test
							of your skills awaits. The strength of your Pokémon will be
							determined by a dynamic combination of weather conditions and game
							modifiers. Adapt to the ever-changing battlefield to emerge
							victorious!
						</p>
					</Col>
				</Row>
				<Row className="mt-4">
					<Col>
						<h3>Phase Three: Confront the Boss</h3>
						<p>
							As you navigate through the treacherous landscape, a formidable
							boss emerges to test your mettle. The Pokebattle Pokémon Battle
							Calculator springs into action, evaluating your team's composition
							to determine the outcome of the epic showdown. Will you emerge
							triumphant, or will the boss claim victory?
						</p>
					</Col>
				</Row>
				<Row className="mt-4">
					<Col>
						<h3>Victory or Defeat?</h3>
						<p>
							If you emerge victorious, the journey continues! Enter stage two,
							where even greater challenges await. But beware - failure is not
							an option! If defeat is your fate, fear not. You'll have the
							chance to learn from your mistakes and prepare for the next
							battle. Will you rise to the occasion and claim victory, or will
							defeat be your ultimate fate?
						</p>
					</Col>
				</Row>
				<Row className="mt-4">
					<Col>
						<h3>Are You Ready to Begin?</h3>
						<p>
							Prepare yourself, Trainer! The ultimate Pokémon adventure awaits.
							Will you seize glory and become a legend, or will your dreams be
							dashed against the rocks of defeat? The choice is yours. Are you
							ready to embark on this epic journey?
						</p>
					</Col>
				</Row>
				<Row className="mt-4">
					<Col>
						<Button variant="primary" href="/shop">
							Start Your Journey
						</Button>
					</Col>
				</Row>
			</Container>
		</div>
	);
};

export default TutorialPage;
