import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';

const useAuth = () => {
  const { accessToken } = useSelector((state) => state.auth);
  const navigate = useNavigate();

  if (!accessToken) {
    navigate('/login'); // Redirect to login if not authenticated
  }

  return { isAuthenticated: !!accessToken };
};

export default useAuth;
