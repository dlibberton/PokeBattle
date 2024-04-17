import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/esm/Button';
import { userLogOut } from '../utilities';

function NavBar({ setUser, user }) {
	return (
		<Navbar expand="lg" className="bg-body-tertiary">
			<Container>
				<Navbar.Brand as={Link} to="/">
					Pokebattle!
				</Navbar.Brand>
				<Navbar.Toggle aria-controls="basic-navbar-nav" />
				<Navbar.Collapse id="basic-navbar-nav">
					<Nav className="me-auto">
						{!user ? (
							<>
								<Nav.Link as={Link} to="/">
									Sign Up or Log In to Play!
								</Nav.Link>
							</>
						) : (
							<>
								<Nav.Link as={Link} to="/home/">
									Home
								</Nav.Link>
								<Button
									variant="outline-danger"
									onClick={async () => setUser(await userLogOut())}
								>
									Log Out
								</Button>
							</>
						)}
					</Nav>
				</Navbar.Collapse>
			</Container>
		</Navbar>
	);
}

export default NavBar;
