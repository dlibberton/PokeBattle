import notFound from '../assets/404.png';

const NotFoundPage = () => {
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
			<img src={notFound} style={{ height: '90vh', width: '90vw' }} />
		</div>
	);
};

export default NotFoundPage;
