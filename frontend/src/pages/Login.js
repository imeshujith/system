import React, { useState } from 'react';
import { useLoginMutation } from '../redux/slices/apiSlice';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../redux/slices/authSlice';
import { Link, useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, Typography } from 'antd';

const { Title } = Typography;

const LoginPage = () => {
  const [login] = useLoginMutation();
  const dispatch = useDispatch();
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      const { data } = await login(values);
      dispatch(setCredentials(data));
      navigate("/");
    } catch (err) {
      setError('Login failed. Please check your credentials.');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <Card
        title={<Title level={2}>Login</Title>}
        style={{ width: 400 }}
      >
        <Form onFinish={onFinish}>
          <Form.Item name="username" rules={[{ required: true, message: 'Please input your username!' }]}>
            <Input placeholder="Username" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: 'Please input your password!' }]}>
            <Input.Password placeholder="Password" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" style={{ width: '100%' }}>
              Login
            </Button>
          </Form.Item>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <p>
            Don't have an account? <Link to="/signup">Sign Up</Link>
          </p>
        </Form>
      </Card>
    </div>
  );
};

export default LoginPage;
