import { useOutletContext } from 'react-router-dom';

const HomePage = () => {
	const { user } = useOutletContext();
	return <h1>Welcome{user && ` ${user}`}</h1>;
};

export default HomePage;
