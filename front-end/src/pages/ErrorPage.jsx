import errImg from '../assets/error.jpg';

const ErrorPage = () => {
	return (
		<div
			style={{
				height: '100%',
				width: '100%',
				display: 'flex',
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			<img src={errImg} style={{ height: '90vh', width: '90vw' }} />
		</div>
	);
};

export default ErrorPage;
