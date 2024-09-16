import React from 'react';
import { Layout, Button } from 'antd';
import { Outlet, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { clearCredentials } from '../redux/slices/authSlice';

const { Header, Sider, Content } = Layout;

const DashboardLayout = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleLogout = () => {
    // Clear authentication data
    dispatch(clearCredentials());

    // Navigate to the login page
    navigate('/login');
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Layout>
        <Header className="header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div className="logo" />
          <Button type="link" onClick={handleLogout}>
            Logout
          </Button>
        </Header>
        <Content style={{ margin: '16px' }}>
          <div style={{ padding: 24, minHeight: 360 }}>
            <Outlet />
          </div>
        </Content>
      </Layout>
    </Layout>
  );
};

export default DashboardLayout;
