import { createBrowserRouter } from 'react-router-dom';
import App from './App';
import LogIn from './pages/LogIn';
import NotFoundPage from './pages/NotFoundPage';
import HomePage from './pages/HomePage';
import ErrorPage from './pages/ErrorPage';
import { userConfirmation } from './utilities';

const router = createBrowserRouter([
	{
		path: '/',
		element: <App />,
		loader: userConfirmation,
		errorElement: <ErrorPage />,
		children: [
			{
				index: true,
				element: <LogIn />,
			},
			{
				path: '/home/',
				element: <HomePage />,
			},
			{
				path: '*',
				element: <NotFoundPage />,
			},
		],
	},
]);

export default router;
