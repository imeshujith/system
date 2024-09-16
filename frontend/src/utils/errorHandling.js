import { clearCredentials } from '../redux/slices/authSlice';

export const handleUnauthorized = (api, navigate) => {
  api.dispatch(clearCredentials());
  navigate('/login');
};
