import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Button, DatePicker, Upload, message } from 'antd';
import { useCreateBookMutation, useUpdateBookMutation } from '../redux/slices/apiSlice';
import { PlusOutlined } from '@ant-design/icons';
import * as moment from 'moment';

const CreateBookModal = ({ visible, onClose, mode, bookData }) => {
  const [createBook] = useCreateBookMutation();
  const [updateBook] = useUpdateBookMutation();
  const [form] = Form.useForm();
  const [imageBase64, setImageBase64] = useState(null);

  useEffect(() => {
    if (visible && mode === 'edit' && bookData) {
      form.setFieldsValue({
        id: bookData.id,
        title: bookData.title,
        author: bookData.author,
        publication_date: bookData.publication_date ? moment(bookData.publication_date) : null,
        isbn: bookData.isbn,
      });
      setImageBase64(bookData.cover_image || null);
    } else if (mode === 'create') {
      form.resetFields();
      setImageBase64(null);
    }
  }, [visible, mode, bookData, form]);

  const onFinish = async (values) => {
    try {
      const bookData = {
        ...values,
        cover_image: imageBase64 || values.cover_image,
        publication_date: values.publication_date ? values.publication_date.format('YYYY-MM-DD') : null,
      };

      if (mode === 'create') {
        await createBook(bookData).unwrap();
        message.success('Book created successfully!');
      } else if (mode === 'edit') {
        await updateBook({ id: values.id, ...bookData }).unwrap();
        message.success('Book updated successfully!');
      }

      onClose();
      form.resetFields();
    } catch (error) {
      message.error(`Failed to ${mode === 'create' ? 'create' : 'update'} book`);
    }
  };

  const handleImageUpload = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setImageBase64(e.target.result);
    };
    reader.readAsDataURL(file);
    return false; // Prevent upload
  };

  // Function to disable future dates
  const disableFutureDates = (current) => {
    return current && current.isAfter(moment().endOf('day')); // Disable dates after today
  };

  return (
    <Modal
      title={mode === 'create' ? "Create New Book" : "Edit Book"}
      visible={visible}
      onCancel={onClose}
      footer={null}
    >
      <Form form={form} layout="vertical" onFinish={onFinish}>
        {/* Hidden Field for ID */}
        {mode === 'edit' && (
          <Form.Item name="id" hidden>
            <Input type="hidden" />
          </Form.Item>
        )}

        {/* Title */}
        <Form.Item
          label="Title"
          name="title"
          rules={[{ required: true, message: 'Please input the title!' }]}
        >
          <Input placeholder="Enter the book title" />
        </Form.Item>

        {/* Author */}
        <Form.Item
          label="Author"
          name="author"
          rules={[{ required: true, message: 'Please input the author!' }]}
        >
          <Input placeholder="Enter the author name" />
        </Form.Item>

        {/* Publication Date */}
        <Form.Item label="Publication Date" name="publication_date">
          <DatePicker
            format="YYYY-MM-DD"
            placeholder="Select publication date"
            disabledDate={disableFutureDates}
          />
        </Form.Item>

        {/* ISBN */}
        <Form.Item
          label="ISBN"
          name="isbn"
          rules={[
            { pattern: /^\d{10}(\d{3})?$/, message: 'Please enter a valid ISBN number (10 or 13 digits)' },
          ]}
        >
          <Input placeholder="Enter the ISBN" />
        </Form.Item>

        {/* Cover Image */}
        <Form.Item label="Cover Image">
          <Upload
            listType="picture-card"
            showUploadList={false}
            beforeUpload={handleImageUpload}
          >
            {imageBase64 ? (
              <img src={imageBase64} alt="Cover" style={{ width: '100%' }} />
            ) : (
              <div>
                <PlusOutlined />
                <div style={{ marginTop: 8 }}>Upload</div>
              </div>
            )}
          </Upload>
        </Form.Item>

        {/* Submit Button */}
        <Form.Item>
          <Button type="primary" htmlType="submit">
            {mode === 'create' ? 'Create Book' : 'Update Book'}
          </Button>
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default CreateBookModal;
