import React from 'react';
import { useSignupMutation } from '../redux/slices/apiSlice';
import { useDispatch } from 'react-redux';
import { setCredentials } from '../redux/slices/authSlice';
import { Link, useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, Typography, message } from 'antd';

const { Title } = Typography;

const SignupPage = () => {
  const [form] = Form.useForm();
  const [signup, { isLoading, isSuccess, isError, error }] = useSignupMutation();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    const { username, email, password } = values;

    try {
      const response = await signup({ username, email, password }).unwrap();
      dispatch(setCredentials(response));
      navigate("/");
      message.success('Signup successful!');
    } catch (err) {
      if (err.status !== 422) {
        message.error(err.data.detail);
      } else {
        if (err.data && err.data.detail) {
          const errors = err.data.detail;
          const formattedErrors = {};

          errors.forEach((error) => {
            const field = error.loc[1];
            if (field) {
              formattedErrors[field] = error.msg;
            }
          });

          form.setFields(
            Object.keys(formattedErrors).map((field) => ({
              name: field,
              errors: [formattedErrors[field]],
            }))
          );

          message.error('Signup failed. Please check the form for errors.');
        }
      }
    }
  };

  const validateConfirmPassword = (rule, value, callback) => {
    if (value && value !== form.getFieldValue('password')) {
      callback('Passwords do not match!');
    } else {
      callback();
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <Card
        title={<Title level={2}>Sign Up</Title>}
        style={{ width: 400 }}
      >
        <Form form={form} onFinish={onFinish}>
          <Form.Item name="username" rules={[{ required: true, message: 'Please input your username!' }]}>
            <Input placeholder="Username" />
          </Form.Item>
          <Form.Item name="email" rules={[{ required: true, type: 'email', message: 'Please input a valid email!' }]}>
            <Input placeholder="Email" />
          </Form.Item>
          <Form.Item name="password" rules={[{ required: true, message: 'Please input your password!' }]}>
            <Input.Password placeholder="Password" />
          </Form.Item>
          <Form.Item
            name="confirm"
            dependencies={['password']}
            hasFeedback
            rules={[
              { required: true, message: 'Please confirm your password!' },
              { validator: validateConfirmPassword }
            ]}
          >
            <Input.Password placeholder="Confirm Password" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={isLoading} style={{ width: '100%' }}>
              Sign Up
            </Button>
          </Form.Item>
          <p>
            Already have an account? <Link to="/login">Login</Link>
          </p>
        </Form>
      </Card>
    </div>
  );
};

export default SignupPage;
